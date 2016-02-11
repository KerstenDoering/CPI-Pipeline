package org.learningformat.transform.bionlp;

import java.io.File;
import java.io.IOException;
import java.io.Writer;
import java.util.ArrayList;
import java.util.Collection;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

import org.apache.commons.lang.StringEscapeUtils;
import org.learningformat.util.FileHelper;

/**
 * 
 * 
 * Example BioNLP format stand-off annotations (stored in *.a1 or *.a2):
 * 
 * <pre>
 * T4      CellType 150 166        OCT-4+ cell type
 * T1      CellType 169 181        crater cells
 * *       Equiv T1 T4
 * T10     GeneProtein 449 455     nestin
 * T11     CellType 483 490        neurons
 * R1      Expression Arg1:T10 Arg2:T9
 * #1      AnnotatorNote T4        some comment
 * </pre>
 * 
 * @author Illes Solt
 */
public abstract class BioNLP {

	private final static String fieldDelimiter = "\t";
	private final static String itemDelimiter = " ";
	private final static String keyValueDelimiter = ":";

	public static class BioNLPDocument {
		String id;
		String plainText;
		Collection<Annotation> annotations;

		public BioNLPDocument() {
			annotations = new ArrayList<Annotation>();
		}

		public void store(File directory) throws IOException {
		    	final String prefix = id.replaceAll("\\W", "_"); 
			// All annotations -- *.ann
			{
				File f = new File(directory, prefix + ".ann");
				if (f.exists())
				    throw new IOException("File already exists: " + f);
				Writer w = FileHelper.getBufferedFileWriter(f.getAbsolutePath());
				for (Annotation a : annotations) {
					w.write(a.toBioNLPString() + "\n");
				}
				w.close();
			}
			// Text -- *.txt
			{
				File f = new File(directory, prefix + ".txt");
				if (f.exists())
				    throw new IOException("File already exists: " + f);
				Writer w = FileHelper.getBufferedFileWriter(f.getAbsolutePath());
				if (plainText != null)
					w.write(plainText);
				w.close();
			}
		}
	}

	/**
	 * Heuristically decide which type of entry is described in the sentence,
	 * the call the respective parser method.
	 * 
	 * @param line
	 * @return
	 */
	Annotation parseBioNLPString(String line) {
		Annotation x;
		if (line.startsWith("E")) {
			x = new Event();
		} else if (line.startsWith("R")) {
			x = new Relation();
		} else if (line.startsWith("*")) {
			x = new Equiv();
		} else if (line.startsWith("T")) {
			x = new Term();
		} else {
			throw new IllegalStateException("Unrecognized line: '" + line);
		}
		x.fromBioNLPString(line);
		return x;
	}

	public static abstract class Annotation {
		protected String id;

		abstract String toBioNLPString();

		abstract void fromBioNLPString(String line);

		public String getId() {
			return id;
		}

		public void setId(String id) {
			this.id = id;
		}

		@Override
		public int hashCode() {
			return id.hashCode();
		}

		@Override
		public String toString() {
			return toBioNLPString();
		}
		
		protected final static String joinItems(String... items) {
			return join(itemDelimiter, items);
		}
		
		protected final static String joinItems(List<String> items) {
			return join(itemDelimiter, items);
		}
		
		protected final static String joinFields(String... fields) {
			return join(fieldDelimiter, fields);
		}
		protected final static String joinFields(List<String> fields) {
			return join(fieldDelimiter, fields);
		}
	}

	public static class Term extends Annotation {
		protected int begin;
		protected int end;
		protected String text;
		protected String type;

		public int getBegin() {
			return begin;
		}

		public void setBegin(int begin) {
			this.begin = begin;
		}

		public int getEnd() {
			return end;
		}

		public void setEnd(int end) {
			this.end = end;
		}

		public String getText() {
			return text;
		}

		public void setText(String text) {
			this.text = text;
		}

		public String getType() {
			return type;
		}

		public void setType(String type) {
			this.type = type;
		}

		@Override
		String toBioNLPString() {
			String data = joinItems(type, String.valueOf(begin),
					String.valueOf(end));
			if (text == null)
				return joinFields(id, data);
			else
				return joinFields(id, data, text);
		}

		@Override
		void fromBioNLPString(String line) {
			throw new InternalError("not implemented");
		}
	}
	
	public static class Equiv extends Annotation {
		protected String term1;
		protected String term2;

		public String getTerm1() {
			return term1;
		}

		public void setTerm1(String term1) {
			this.term1 = term1;
		}

		public String getTerm2() {
			return term2;
		}

		public void setTerm2(String term2) {
			this.term2 = term2;
		}

		@Override
		String toBioNLPString() {
			return joinFields("*",
					joinItems("Equiv", term1, term2));
		}

		@Override
		void fromBioNLPString(String line) {
			throw new InternalError("not implemented");
		}
	}
	
	public static class AnnotatorNote extends Annotation {
		protected String referredId;
		protected String noteText;

		public String getReferredId() {
			return referredId;
		}

		public void setReferredId(String id1) {
			this.referredId = id1;
		}
		
		public String getNoteText() {
			return noteText;
		}
		
		public void setNoteText(String noteText) {
			this.noteText = noteText;
			
		}		

		@Override
		String toBioNLPString() {
			return joinFields(getId(),
					joinItems("AnnotatorNote", referredId), 
					StringEscapeUtils.escapeJava(noteText));
		}

		@Override
		void fromBioNLPString(String line) {
			throw new InternalError("not implemented");
		}

	}
	

	public static class Relation extends Annotation {

		protected String type;
		protected Map<String, String> arguments = new LinkedHashMap<String, String>();

		public String getType() {
			return type;
		}

		public void setType(String type) {
			this.type = type;
		}

		public Map<String, String> getArguments() {
			return arguments;
		}

		public void addArgument(String key, String value) {
			if (arguments.containsKey(key))
				throw new IllegalStateException("Duplicate key: " + key);
			arguments.put(key, value);
		}

		@Override
		String toBioNLPString() {
			List<String> items = new ArrayList<String>(arguments.size() + 1);
			items.add(type);
			for (Entry<String, String> arg : arguments.entrySet()) {
				items.add(arg.getKey() + keyValueDelimiter + arg.getValue());
			}
			return joinFields(id, joinItems(items));
		}

		@Override
		void fromBioNLPString(String line) {
			throw new InternalError("not implemented");
		}
	}

	public static class Event extends Relation {

		protected String triggerTerm;

		public String getTriggerTerm() {
			return triggerTerm;
		}

		public void setTriggerTerm(String triggerTerm) {
			this.triggerTerm = triggerTerm;
		}

		@Override
		String toBioNLPString() {
			throw new InternalError("not implemented");
		}

		@Override
		void fromBioNLPString(String line) {
			throw new InternalError("not implemented");
		}

	}

	/**
	 * Join strings with given glue.
	 * 
	 * @param fields
	 * @param glue
	 * @return
	 */
	static private final String join(String glue, String... fields) {
		if (fields.length == 0)
			return "";
		if (fields.length == 1)
			return fields[0];
		StringBuilder sb = new StringBuilder();
		for (String field : fields) {
			if (sb.length() > 0)
				sb.append(glue);
			sb.append(field);
		}
		return sb.toString();
	}

	/**
	 * Join strings with given glue.
	 * 
	 * @param fields
	 * @param glue
	 * @return
	 */
	static private final String join(String glue, List<String> fields) {
		if (fields.isEmpty())
			return "";
		if (fields.size() == 1)
			return fields.get(0);
		StringBuilder sb = new StringBuilder();
		for (String field : fields) {
			if (sb.length() > 0)
				sb.append(glue);
			sb.append(field);
		}
		return sb.toString();
	}

}
