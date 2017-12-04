package org.learningformat.charite;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedHashSet;
import java.util.Locale;
import java.util.Map;
import java.util.Set;
import java.util.zip.GZIPInputStream;

import javax.xml.parsers.ParserConfigurationException;

import org.apache.commons.lang.StringEscapeUtils;
import org.learningformat.api.Corpus;
import org.learningformat.api.Document;
import org.learningformat.api.Pair;
import org.learningformat.api.Sentence;
import org.learningformat.impl.DefaultCorpus;
import org.learningformat.standoff.AirolaXmlWriter;
import org.learningformat.xml.CorpusListener;
import org.learningformat.xml.Parser;
import org.xml.sax.SAXException;

import au.com.bytecode.opencsv.CSVParser;
import au.com.bytecode.opencsv.CSVReader;

/**
 * Filter a corpus so that it contains only the pairs specified in a text file.
 * 
 * @author Illes Solt
 * 
 */
public class FilterCorpusListener implements CorpusListener {

    public static interface Annotator {
	/**
	 * Translate a standoff pair annotation to an interaction type.
	 * 
	 * @param annotation
	 * @return
	 */
	void annotate(Pair p);
    }

    private static class NoopAnnotator implements Annotator {

	@Override
	public void annotate(Pair p) {
	}

    }

    private static class ChariteAnnotationTranslator implements Annotator {
	/**
	 * Possible feedback are:
	 * 
	 * <pre>
	 * [Entrez_Gene_ID1 ? Entrez_Gene_ID1]: An alternative relation linked to the PMID had been found by reviewers from Oreganno or Transfac.
	 * --&gt;: Link found from Gene_1 to Gene_2 in Oreganno or Transfac
	 * &lt;--: Link found from Gene_2 to Gene_1 in Oreganno or Transfac
	 * &lt;-&gt;: Link found from Gene_1 to Gene_2 and vice versa in Oreganno or Transfac
	 * b: potential promoter binding
	 * c: potential cooperation in transcription
	 * e: potential direct influence on expression
	 * i: inhibition
	 * n: negative statement, no effect
	 * w: wrong recognition of transcription factors
	 * x: sentence with no meaning for our purpose
	 * p: best match: potential direct influence on expression and evidence for promoter binding
	 * </pre>
	 * 
	 */
	private enum Types {
	    DocumentKnown, InteractionKnown, PromoterBinding, CooperationInTranscription, DirectInfluenceOnExpression, Inhibition, Negation, NENError, Irrelevant;
	};

	private final Map<String, String> pairAnnotations;

	public ChariteAnnotationTranslator(Map<String, String> pairAnnotations) {
	    super();
	    this.pairAnnotations = pairAnnotations;
	}

	public void annotate(Pair p) {
	    // reset pair annotations
	    p.setInteraction(false);
	    p.setType("");

	    final String annotation = pairAnnotations.get(p.getId());
	    if (annotation == null)
		return;

	    if ("<--".equals(annotation) || "<->".equals(annotation)
		    || "-->".equals(annotation)) {
		p.setInteraction(true);
		p.setType(Types.InteractionKnown.name());
	    } else if ("b".equals(annotation)) {
		p.setInteraction(true);
		p.setType(Types.PromoterBinding.name());
	    } else if ("c".equals(annotation)) {
		p.setInteraction(true);
		p.setType(Types.CooperationInTranscription.name());
	    } else if ("e".equals(annotation)) {
		p.setInteraction(true);
		p.setType(Types.DirectInfluenceOnExpression.name());
	    } else if ("i".equals(annotation)) {
		p.setInteraction(true);
		p.setType(Types.Inhibition.name());
	    } else if ("n".equals(annotation)) {
		p.setInteraction(false);
		p.setType(Types.Negation.name());
	    } else if ("w".equals(annotation)) {
		p.setInteraction(false);
		p.setType(Types.NENError.name());
	    } else if ("x".equals(annotation)) {
		p.setInteraction(false);
		p.setType(Types.Irrelevant.name());
	    } else if ("p".equals(annotation)) {
		p.setInteraction(true);
		p.setType(Types.DirectInfluenceOnExpression.name() + "|"
			+ Types.PromoterBinding.name());
	    } else if ("e/i".equals(annotation)) {
		p.setInteraction(true);
		p.setType(Types.DirectInfluenceOnExpression.name() + "|"
			+ Types.Inhibition.name());
	    } else if ("e/c".equals(annotation)) {
		p.setInteraction(true);
		p.setType(Types.DirectInfluenceOnExpression.name() + "|"
			+ Types.CooperationInTranscription.name());
	    } else if ("x/c".equals(annotation)) {
		p.setInteraction(true);
		p.setType(Types.Irrelevant.name() + "|"
			+ Types.CooperationInTranscription.name());
	    } else if ("n/w".equals(annotation)) {
		p.setInteraction(false);
		p.setType(Types.NENError.name() + "|" + Types.Negation.name());
	    } else if (annotation.startsWith("[")) {
		p.setInteraction(false);
		p.setType(Types.DocumentKnown.name());
	    } else if(annotation.equals("True")){
	    	p.setInteraction(true);
	    } else if(annotation.equals("False")){
	    	p.setInteraction(false);
	    }else {
	    	System.err.println("[WARN] Unrecognized annotation '"
			+ annotation + "'");
	    }
	}
    }

    /**
     * The position of the manual annotations in the annotations file.
     */
    private static final int ANNOTATION_COLUMN = 2;

    /**
     * The position of the pair label in the annotations file.
     */
    private static final int PAIR_LABEL_COLUMN = 1;

    private static final String USAGE = "Usage: java ... "
	    + FilterCorpusListener.class.getCanonicalName()
	    + " [--help] [--delimiter '\\t'] [--out-file /path/to/file] [--annotator {noop|charite}] [--filter-empty(-{sentences|documents})] [] annotations.csv [corpus.xml ...]";
    private static char delimiter = CSVParser.DEFAULT_SEPARATOR;
    private static File outFile = null;
    private static File annotationFile;

    private static Annotator annotator;

    protected static boolean filterEmptySentences = false;
    protected static boolean filterEmptyDocuments = false;
    protected int docsProcessed = 0;
    protected int sentencesProcessed = 0;
    protected int pairsProcessed = 0;
    protected final long startMillis = System.currentTimeMillis();

    Corpus manualCorpus;
    Document currentDocument;

    Set<String> found = new HashSet<String>();

    public static void main(String[] args) {

	try {
	    if (args.length < 2) {
		System.err.println(USAGE);
		System.exit(1);
	    }
	    String annotatorName = "noop";
	    int i = 0;
	    while (args[i].startsWith("-")) {
		if (args[i].equals("--help")) {
		    System.out.println(USAGE);
		    System.exit(0);
		} else if (args[i].equals("--delimiter")
			|| args[i].equals("-d")) {

		    delimiter = StringEscapeUtils.unescapeJava(args[++i])
			    .charAt(0);
		} else if (args[i].equals("--out-file") || args[i].equals("-o")) {
		    outFile = new File(args[++i]);
		} else if (args[i].equals("--annotator")) {
		    annotatorName = args[++i].toLowerCase(Locale.ENGLISH)
			    .trim();
		} else if (args[i].equals("--filter-empty-sentences")) {
		    filterEmptySentences = true;
		} else if (args[i].equals("--filter-empty-documents")) {
		    filterEmptyDocuments = true;
		} else if (args[i].equals("--filter-empty")) {
		    filterEmptySentences = true;
		    filterEmptyDocuments = true;
		} else {
		    throw new IllegalArgumentException("Unrecognized option: "
			    + args[i]);
		}
		i++;
	    }

	    annotationFile = new File(args[i++]);
	    if (outFile == null)
		outFile = new File(annotationFile.getPath() + ".xml");
	    // info();
	    annotations = parseAnnotations(annotationFile, delimiter);

	    if (annotatorName == null || "noop".equals(annotatorName))
		annotator = new NoopAnnotator();
	    else if ("charite".equals(annotatorName))
		annotator = new ChariteAnnotationTranslator(annotations);
	    else
		throw new IllegalStateException("Unrecognized annotator: '"
			+ annotatorName + "'");

	    FilterCorpusListener conv = new FilterCorpusListener();
	    if (i == args.length) {
		// pipe mode
		conv.process(null);
	    } else {
		// file list mode
		for (; i < args.length; i++) {
		    conv.process(args[i]);
		}
	    }

	    conv.writeXML(outFile);
	    // debug
	    {
		for (String pairLabel : annotations.keySet())
		    if (!conv.found.contains(pairLabel)) {
			System.err.println("Pair not found: " + pairLabel);
		    }
		System.err.println("Found: " + conv.found.size());
		System.err.println("Not found: "
			+ (annotations.size() - conv.found.size()));
		System.err.println("Documents seen: " + conv.docsProcessed);
		System.err
			.println("Sentences seen: " + conv.sentencesProcessed);
		System.err.println("Pairs seen: " + conv.pairsProcessed);

	    }
	    System.err.println("INFO: Output written to: " + outFile.getPath());

	} catch (Exception e) {
	    e.printStackTrace();
	    System.err.println(USAGE);
	    System.exit(1);
	}
    }

    private void writeXML(File outFile2) throws IOException {
	AirolaXmlWriter w = new AirolaXmlWriter();
	w.toXMLFile(manualCorpus, outFile, 2);
    }

    public FilterCorpusListener() {
	manualCorpus = new DefaultCorpus();
	manualCorpus.setSource(FilterCorpusListener.class.getName());
    }

    /**
     * PairLabel vs assigned type
     */
    static Map<String, String> annotations;

    private static Map<String, String> parseAnnotations(File annotationsFile,
	    char delimiter) throws IOException {
	Map<String, String> annotations = new HashMap<String, String>();

	CSVReader csv = new CSVReader(new FileReader(annotationsFile),
		delimiter);
	String[] row;
	while ((row = csv.readNext()) != null) {
	    // skip empty rows
	    if (row.length == 0)
		continue;

	    try {
		// nextLine[] is an array of values from the line
		final String pairLabel = row[PAIR_LABEL_COLUMN - 1];
		final String annotation = row[ANNOTATION_COLUMN - 1];

		// TODO process annotation
		if (annotations.put(pairLabel, annotation) != null)
		    throw new RuntimeException("duplicate pair label: '"
			    + pairLabel + "'");

		// System.err.println("Pair: " + pairLabel);
	    } catch (Exception e) {
		throw new RuntimeException("Failed to parse row '"
			+ Arrays.toString(row) + "'", e);
	    }
	}
	System.err.println("Pairs: " + annotations.size());
	return annotations;
    }

    /**
     * 
     * Process corpus XML file or standard input.
     * 
     * @param path
     * @throws SAXException
     * @throws IOException
     * @throws ParserConfigurationException
     */
    private void process(String path) throws SAXException, IOException,
	    ParserConfigurationException {
	InputStream in = null;
	try {
	    if (path != null) {
		System.err.println("INFO: Processing '" + path + "'...");
				if(path.endsWith(".gz"))
					in = new GZIPInputStream(new FileInputStream(path));
				else
		in = new FileInputStream(path);
	    } else {
		System.err.println("INFO: Processing standard input...");
		in = System.in;
	    }

	    // Parse all linguistic information
	    Parser parser = new Parser(this);

	    // release documents immediately after processing
	    // for efficiency only
	    // parser.setImmediatelyRemoveDocuments(true);

	    // Try to recover from errors.
	    parser.setTryToRecoverFromErrors(true);

	    try {
		parser.process(in);
	    } catch (Exception e) {
		throw new RuntimeException("error processing: " + path, e);
	    }
	} finally {
	    if (in != null) {
		in.close();
	    }
	}
    }

    @Override
    public void startCorpus(Corpus corpus) {
	// do nothing
    }

    @Override
    public void startDocument(Document document) {
	currentDocument = document;
	docsProcessed++;
	if ((docsProcessed % 1000) == 0)
	    System.err
		    .println("processed "
			    + docsProcessed
			    + " docs, kept "
			    + manualCorpus.getDocuments().size()
			    + " ("
			    + (docsProcessed / ((System.currentTimeMillis() - startMillis) / 1000f))
			    + " docs/sec)");

	// System.err.println("Doc: " + document);
    }

    @Override
    public void processSentence(Sentence sentence) {
	sentencesProcessed++;
	// Set<Entity> keepEntities = new
	// LinkedHashSet<Entity>(sentence.getEntities().size());
	Set<Pair> keepPairs = new LinkedHashSet<Pair>(sentence.getAllPairs()
		.size());

	for (Pair pair : sentence.getAllPairs()) {
	    pairsProcessed++;
	    if (annotations.containsKey(pair.getId())) {
		// keepEntities.add(pair.getE1());
		// keepEntities.add(pair.getE2());
		keepPairs.add(pair);
		System.err.println("Keep: " + pair);
	    }
	}

	if (filterEmptySentences && keepPairs.isEmpty()) {
	    sentence.getDocument().getSentences().remove(sentence);
	} else {
	    for (Iterator<Pair> it = sentence.getAllPairs().iterator(); it
		    .hasNext();) {
		Pair pair = (Pair) it.next();
		if (!keepPairs.contains(pair))
		    it.remove();
		else {
		    found.add(pair.getId());

		    // Let the annotator modify pair annotations
		    annotator.annotate(pair);
		}
		// else
		// System.err.println("Kept: " + pair);

	    }
	}

	// for (Iterator<Entity> iterator = sentence.getEntities().iterator();
	// iterator.hasNext();) {
	// Pair pair = (Pair) iterator.next();
	// if (!keepPairs.contains(pair.getId()))
	// iterator.remove();
	// }
    }

    @Override
    public void endCorpus() {
	// do nothing
    }

    @Override
    public void endDocument() {
	// adopt document
	if (!filterEmptyDocuments || currentDocument.getSentences().size() > 0) {
	    currentDocument.setCorpus(null);
	    currentDocument.setCorpus(manualCorpus);
	}
	// System.err.println("Docs: " + manualCorpus.getDocuments().size());
	currentDocument = null;
    }

}
