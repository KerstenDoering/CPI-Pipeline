package org.learningformat.standoff;

import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.nio.charset.Charset;
import java.util.Collection;
import java.util.HashMap;
import java.util.Map;

import org.learningformat.api.CharOffset;
import org.learningformat.api.CharOffsetProvider;
import org.learningformat.api.Corpus;
import org.learningformat.api.Document;
import org.learningformat.api.Entity;
import org.learningformat.api.Sentence;
import org.learningformat.api.CharOffset.SingleCharOffset;
import org.learningformat.impl.DefaultCorpus;
import org.learningformat.impl.DefaultDocument;
import org.learningformat.impl.DefaultEntity;
import org.learningformat.impl.DefaultSentence;
import org.learningformat.impl.ErrorListener;
import org.learningformat.util.FileHelper;

import au.com.bytecode.opencsv.CSVReader;

/**
 * Class to construct an in-memory representation of a {@link Corpus} based on standoff files. 
 * @author illes
 *
 */
public class StandoffParser extends ErrorListener {

	private static final char CSV_NO_QUOTE = '\0'; 
	private static final char CSV_NO_ESCAPE = '\0';
	private static final char CSV_DELIMITER = '\t';
	
	/**
	 * Helper method.
	 * @return <code>null</code> if i is out of range
	 */
	public static <T> T get(T[] a, int i) {
	    return i < a.length ? a[i] : null;
	}
	
	public static <T> T get(T[] a, Map<String, Integer> name2idx, String name) {
	    return name2idx.containsKey(name) ? get(a, name2idx.get(name).intValue()) : null; 
	}

	public static <T> T coalesce(T a, T b) {
	    return a == null ? b : a;
	}
	
	public static <T> T coalesce(T a, T b, T c) {
	    return a != null ? a : coalesce(b, c);
	}
	
	public static <T> T coalesce(T a, T b, T c, T d) {
	    return a != null ? a : coalesce(b, c, d);
	}
	
	/**
	 * Character offsets in the  input files are one-based (starting from 1), instead of the C/Java-style zero-based (starting from 0) indexing.
	 */
	private boolean offsetOneBased;
	
	/**
	 * Character ranges' end position in the input files is inclusive, in contrast to the C/Java-style exclusive (character at end not included) range.
	 */
	private boolean offsetEndInclusive;


	/**
	 * @see #offsetOneBased
	 */
	public boolean isOffsetOneBased() {
		return offsetOneBased;
	}

	/**
	 * @see #offsetOneBased
	 */
	public void setOffsetOneBased(boolean offsetOneBased) {
		this.offsetOneBased = offsetOneBased;
	}

	/**
	 * @see #offsetEndInclusive
	 */
	public boolean isOffsetEndInclusive() {
		return offsetEndInclusive;
	}

	/**
	 * @see #offsetEndInclusive
	 */
	public void setOffsetEndInclusive(boolean offsetEndInclusive) {
		this.offsetEndInclusive = offsetEndInclusive;
	}
	
	// TODO externalize
	// TODO upgrade to CSVDictReader	
	private static final Map<String, Integer> sbColumns = toMap(new String[] {"begin","end","id"});
	private static final Map<String, Integer> entColumns = toMap( new String[] {"begin","end","id","confidence","text"});

	/** Convenience method
	 * 
	 * @param corpusName the name of the corpus, used as a prefix for the document identifier
	 * @param documentIndex a unique numerical identifier for the document in the corpus 
	 * @param baseDir the directory containing the standoff files
	 * @param prefix the filename prefix of the standoff files
	 * @param encoding the encoding of the standoff files
	 * @return
	 * @throws IOException
	 */
	Document fromStandoffFiles(String corpusName, int documentIndex, File baseDir, String prefix, Charset encoding) throws IOException
	{
		return fromStandoffFilesId(corpusName+".d"+ documentIndex, baseDir, prefix, encoding);
	}
	
	/** Convenience method
	 * 
	 * @param corpusName the name of the corpus, used as a prefix for the document identifier
	 * @param documentName a unique identifier for the document in the corpus 
	 * @param baseDir the directory containing the standoff files
	 * @param prefix the filename prefix of the standoff files
	 * @param encoding the encoding of the standoff files
	 * @return
	 * @throws IOException
	 */
	Document fromStandoffFiles(String corpusName, String documentName, File baseDir, String prefix, Charset encoding) throws IOException
	{
		return fromStandoffFilesId(corpusName+".d"+ documentName, baseDir, prefix, encoding);
	}

	/** Convenience method
	 * 
	 * @param corpus only the name of the corpus is used as a prefix for the document identifier
	 * @param documentIndex a unique numerical identifier for the document in the corpus 
	 * @param baseDir the directory containing the standoff files
	 * @param prefix the filename prefix of the standoff files
	 * @param encoding the encoding of the standoff files
	 * @return
	 * @throws IOException
	 */
	Document fromStandoffFiles(Corpus corpus, String documentName, File baseDir, String prefix, Charset encoding) throws IOException
	{
		return fromStandoffFiles(corpus.getSource(), documentName, baseDir, prefix, encoding);
	}
	
	/** Convenience method
	 * 
	 * @param corpusName the name of the corpus, used as a prefix for the document identifier
	 * @param baseDir the directory containing the standoff files
	 * @param prefix the filename prefix of the standoff files, should be unique
	 * @param encoding the encoding of the standoff files
	 * @return
	 * @throws IOException
	 */
	Document fromStandoffFiles(String corpusName, File baseDir, String prefix, Charset encoding) throws IOException
	{
		return fromStandoffFiles(corpusName, prefix, baseDir, prefix, encoding);
	}
	
	/**
	 * Driver method to construct a {@link Document} from standoff files.
	 * <ul>
	 * <li>&lt;<code>prefix</code>>.txt - a text file containing the raw {@link Document} text
	 * <li>&lt;<code>prefix</code>>.sb.tsv - a TSV (tab separated values) file containing the {@link Sentence} boundaries (character ranges)
	 * <li>&lt;<code>prefix</code>>.ent.tsv - a TSV (tab separated values) file containing the {@link Entity} annotations (character ranges with an identifier)
	 * </ul>
	 * @param documentId
	 * @param baseDir
	 * @param prefix
	 * @param encoding
	 * @return
	 * @throws IOException
	 */
	private Document fromStandoffFilesId(String documentId, File baseDir, String prefix, Charset encoding) throws IOException
	{
		Document doc = new DefaultDocument();
		doc.setOrigId(prefix);
		doc.setId(documentId);
		
		final String documentText = FileHelper.readFileAsString(new File(baseDir, prefix + ".txt"), encoding);
		doc.setText(documentText);

		final int currentErrors = getErrors();
	    int entSkip = 0;
	    int sbSkip = 0;
		CSVReader sbReader  = new CSVReader(new FileReader(new File(baseDir, prefix + ".sb.tsv" )), CSV_DELIMITER, CSV_NO_ESCAPE, CSV_NO_QUOTE, sbSkip, false);
		CSVReader entReader = new CSVReader(new FileReader(new File(baseDir, prefix + ".ent.tsv")), CSV_DELIMITER, CSV_NO_ESCAPE, CSV_NO_QUOTE, entSkip, false);
	    addSentencesFrom(doc, sbReader, sbColumns); // TODO upgrade to CSVDictReader
	    addEntitiesFrom(doc, entReader, entColumns); // TODO upgrade to CSVDictReader
	    
	    if (getErrors() > 0)
	    	System.err.println("WARNING: document " + documentId + "had " + (getErrors() - currentErrors) +" errors (total: " + getErrors() + ")");
	    
		return doc;
	}

	@Deprecated
	private static Map<String, Integer> toMap(String[] columns) {
	    Map<String, Integer> columnIndex = new HashMap<String, Integer>();
	    for (int i = 0; i < columns.length; i++)
			columnIndex.put(columns[i], i);
	    return columnIndex;
	}

	void addSentencesFrom(Document doc, CSVReader csv, Map<String, Integer> columns) throws NumberFormatException, IOException {
		String[] row;
		int lineNo = 0;
		while ((row = csv.readNext()) != null) {
			lineNo++;
			try {
				// parse
				int begin = Integer.parseInt(row[columns.get("begin")]);
				int end = Integer.parseInt(row[columns.get("end")]);
				String id = coalesce(get(row, columns, "id"), String.valueOf(lineNo));
				String text = get(row, columns, "text");
				//System.err.println("" + begin + "-" + end + ": " + id);
	
				//System.err.println("DEBUG: adding sentence to document " + doc.getId() + ": " + begin + "-" + end + " (" + id +")");
				
				// assign
				Sentence s = new DefaultSentence();
				s.setCharOffset(toCharOffset(begin, end)); 
				s.setId(doc.getId()+".s" + id);
				s.setOrigId(id);
				
				if (text != null)
					s.setText(text); // set from column 'text' 
				else 
					s.setText(toSingleCharOffset(s).substringOf(doc)); // set from columns 'begin','end' and document text
				
				// link
				s.setDocument(doc);
			}
			catch (RuntimeException e)
			{
				error(e);
			}
		}
		System.err.println("DEBUG: sentences in document " + doc.getId() + ": " + doc.getSentences().size());
	}
	
	private CharOffset toCharOffset(int begin, int end) {
		if (isOffsetOneBased())
			throw new InternalError("not implemented"); // TODO: adjust +0 OR -1
		if (isOffsetEndInclusive())
			end++;
		return new CharOffset(begin, end);  
	}
	
	private CharOffset shiftCharOffset(SingleCharOffset sco, int offset) {
		return new CharOffset(sco.getStart()-offset, sco.getEnd()-offset);  
	}
	

	void addEntitiesFrom(Document doc, CSVReader csv, Map<String, Integer> columns) throws NumberFormatException, IOException {
		String[] row;
		int lineNo = 0;
		while ((row = csv.readNext()) != null) {
			lineNo++;
			// parse
			int begin = Integer.parseInt(row[columns.get("begin")]);
			int end = Integer.parseInt(row[columns.get("end")]);
			String text = get(row, columns, "text");
			String label = doc.getId()+".e" + lineNo;
			String origId = get(row, columns, "id");
			String entityId = coalesce(get(row, columns, "entity"), label);
			//System.err.println("" + begin + "-" + end + ": " + id);
			
			// assign
			Entity e = new DefaultEntity();
			e.setCharOffset(toCharOffset(begin, end));
			e.setId(entityId);
			e.setOrigId(origId);
			e.setText(text);
			
			// link
			Sentence s = findContainer(doc.getSentences(), e);
			if (s == null)
				error(new IllegalStateException("No containing sentence found in doc\n" + doc.toString() +"\nfor entity\n" + e.toString()));
			else
			{
				s.addEntity(e);
				e.setCharOffset(shiftCharOffset(toSingleCharOffset(e), toSingleCharOffset(s).getStart()));
			}
		}
		
	}
	
	
	/**
	 * Try to convert a generic {@link CharOffsetProvider} to a {@link SingleCharOffset}.
	 * @param e
	 * @return
	 * @throws UnsupportedOperationException iff <code>e</code> does not have exactly one {@link CharOffset}
	 */
	public static SingleCharOffset toSingleCharOffset(CharOffsetProvider e) throws UnsupportedOperationException {
		if (e.getCharOffset().getCharOffsets().length != 1)
			throw new UnsupportedOperationException("Cannot handle CharOffset with " + e.getCharOffset().getCharOffsets().length + " parts");
		return e.getCharOffset().getCharOffsets()[0]; 
	}

	private static <T extends CharOffsetProvider> T findContainer(Collection<T> haystack, CharOffsetProvider needle) {
		return findContainer(haystack, toSingleCharOffset(needle));
	}

	private static <T extends CharOffsetProvider> T findContainer(Collection<T> haystack, SingleCharOffset needle) {
		if (needle == null)
			throw new NullPointerException();
		
		for (T container : haystack) {
			if (container.getCharOffset() == null)
				continue;
			for (SingleCharOffset sco : container.getCharOffset().getCharOffsets()) {
				if (sco.contains(needle))
					return container;
			}
		}
		return null;
	}

	public static void main(String[] args) throws IOException {
		StandoffParser p = new StandoffParser();
		Corpus corpus = new DefaultCorpus();
		corpus.setSource("test");
		Document d = p.fromStandoffFiles("TEST", new File("./test"), "1", Charset.forName("UTF-8"));
		d.setCorpus(corpus);

		System.err.println(new AirolaXmlWriter().toXml(corpus).toString(2));
		new AirolaXmlWriter().toXMLFile(corpus, new File("test.xml"), 2);
	}
}
