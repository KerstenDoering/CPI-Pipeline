package org.learningformat.transform.bionlp;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Pattern;

import javax.xml.parsers.ParserConfigurationException;

import org.learningformat.api.CharOffset.SingleCharOffset;
import org.learningformat.api.Corpus;
import org.learningformat.api.Document;
import org.learningformat.api.Entity;
import org.learningformat.api.Pair;
import org.learningformat.api.Sentence;
import org.learningformat.impl.DefaultElementFactory;
import org.learningformat.transform.bionlp.BioNLP.AnnotatorNote;
import org.learningformat.transform.bionlp.BioNLP.BioNLPDocument;
import org.learningformat.transform.bionlp.BioNLP.Equiv;
import org.learningformat.transform.bionlp.BioNLP.Relation;
import org.learningformat.transform.bionlp.BioNLP.Term;
import org.learningformat.xml.CorpusListener;
import org.learningformat.xml.Parser;
import org.xml.sax.SAXException;

/**
 * Convert corpora in Airola-style XML to {@link BioNLP} challenge-style
 * stand-off annotated corpus.
 * 
 * @see org.learningformat.xml
 * 
 * @author Illes Solt
 * 
 */
public class BioNLPExampleWriter implements CorpusListener {

	private static final String USAGE = "Usage: java ... "
			+ BioNLPExampleWriter.class.getCanonicalName()
			+ " [--help] [--directory /out/dir] [--all-pairs] [--equiv] [--notes] corpus.xml ...";
	static File outDir = new File("./bionlp/");

	/**
	 * Also add negative pairs to the output.
	 */
	static boolean writeAllPairs = false;

	/**
	 * Derive entity co-reference ("Equiv") annotations for entities having the
	 * same origId attribute.
	 */
	static boolean deriveEquivs = false;

	/**
	 * Derive notes for entities from origId.
	 */
	static boolean deriveEntityNotes = false;

	/**
	 * Use a constant term type instead of type attribute.
	 */
	static String termType = null;

	/**
	 * Use a constant relation type instead of type attribute.
	 */
	static String relationType = null;

	State state;
	
	public static final String DEFAULT_TYPE = "Interaction";

	static void info() {
		System.err.println("INFO: Output directory: " + outDir.getPath());
		System.err.println("INFO: Derive equivalents from origId [-e]: "
				+ (deriveEquivs ? "yes" : "no"));
		System.err.println("INFO: Derive notes from origId [-n]: "
				+ (deriveEntityNotes ? "yes" : "no"));
		System.err.println("INFO: Include negative pairs [-a]: "
				+ (writeAllPairs ? "yes" : "no"));
		System.err.println("INFO: Override term type [-T]: "
				+ (termType == null ? "no" : "yes (" + termType + ")"));
		System.err.println("INFO: Override relation type [-R]: "
				+ (relationType == null ? "no" : "yes (" + relationType + ")"));
	}

	public static void main(String[] args) {

		try {
			if (args.length < 1) {
				info();
				// pipe mode
				transform(null);
			} else {
				int i = 0;
				while (args[i].startsWith("-")) {
					if (args[i].equals("--help")) {
						System.out.println(USAGE);
						System.exit(0);
					} else if (args[i].equals("--all-pairs")
							|| args[i].equals("-a")) {
						writeAllPairs = true;
					} else if (args[i].equals("--equiv")
							|| args[i].equals("-e")) {
						deriveEquivs = true;
					} else if (args[i].equals("--notes")
							|| args[i].equals("-n")) {
						deriveEntityNotes = true;
					} else if (args[i].equals("--directory")
							|| args[i].equals("-d")) {
						outDir = new File(args[++i]);
					} else if (args[i].equals("--relation-type")
							|| args[i].equals("-R")) {
						relationType = args[++i];
					} else if (args[i].equals("--term-type")
							|| args[i].equals("-T")) {
						termType = args[++i];
					} else {
						throw new IllegalArgumentException(
								"Unrecognized option: " + args[i]);
					}
					i++;
				}
				info();
				for (; i < args.length; i++) {
					transform(args[i]);
				}
				System.err.println("INFO: Output written to: "
						+ outDir.getPath());
			}
		} catch (Exception e) {
			e.printStackTrace();
			System.err.println(USAGE);
			System.exit(1);
		}

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
	private static void transform(String path) throws SAXException,
			IOException, ParserConfigurationException {
		InputStream in = null;
		try {
			if (path != null) {
				System.err.println("INFO: Processing '" + path + "'...");
				in = new FileInputStream(path);
			} else {
				System.err.println("INFO: Processing standard input...");
				in = System.in;
			}

			BioNLPExampleWriter mapper = new BioNLPExampleWriter();

			// Ignore all linguistic information
			Parser parser = new Parser(Collections.<String> emptySet(),
					Collections.<String> emptySet(),
					Collections.<String> emptySet(),
					new DefaultElementFactory(), mapper);

			// release documents immediately after processing
			// for efficiency only
			parser.setImmediatelyRemoveDocuments(true);

			parser.process(in);
		} finally {
			if (in != null) {
				in.close();
			}
		}
	}

	private class State {
		int sentenceBeginOffset;
		BioNLPDocument bionlpDoc;
		Map<String, String> entityLabel2id;
		Map<String, String> pairLabel2id;
		Map<String, String> label2noteId;
		String corpus;

		/**
		 * Entities to be searched for equivalents.
		 */
		public List<Entity> equivCache;

		void newDocument(Document d) {
			sentenceBeginOffset = 0;
			bionlpDoc = new BioNLPDocument();

			entityLabel2id = new HashMap<String, String>();
			pairLabel2id = new HashMap<String, String>();
			label2noteId = new HashMap<String, String>();

			bionlpDoc.id = d.getId();
			corpus = d.getCorpus().getSource();

			equivCache = new ArrayList<Entity>();

			System.err.println("DEBUG: Doc " + bionlpDoc.id + " in " + corpus);
		}

		void newSentence(String text) {
			// first sentence?
			if (bionlpDoc.plainText == null
					|| bionlpDoc.plainText.length() == 0)
				bionlpDoc.plainText = text;
			else {
				bionlpDoc.plainText += "\n";
				// save cursor position at beginning of line
				sentenceBeginOffset = bionlpDoc.plainText.length();
				// append
				bionlpDoc.plainText += text;
			}
		}

		String toTermId(final String label) {
			String id = entityLabel2id.get(label);
			if (id == null) {
				id = "T" + (entityLabel2id.size() + 1);
				entityLabel2id.put(label, id);
			}
			return id;
		}

		@SuppressWarnings("unused")
		String toEventId(String label) {
			String id = pairLabel2id.get(label);
			if (id == null) {
				id = "E" + (pairLabel2id.size() + 1);
				pairLabel2id.put(label, id);
			}
			return id;
		}

		String toRelationId(String label) {
			String id = pairLabel2id.get(label);
			if (id == null) {
				id = "R" + (pairLabel2id.size() + 1);
				pairLabel2id.put(label, id);
			}
			return id;
		}

		String toAnnotatorNoteId(String label) {
			String id = label2noteId.get(label);
			if (id == null) {
				id = "#" + (label2noteId.size() + 1);
				label2noteId.put(label, id);
			}
			return id;
		}

		public void addEntity(Entity e) {
			final SingleCharOffset sco = e.getCharOffset().getCharOffsets()[0];

			final Term t = new Term();
			t.setId(toTermId(e.getId()));
			t.setBegin(sentenceBeginOffset + sco.getStart());
			t.setEnd(sentenceBeginOffset + sco.getEnd());
			try {
			t.setText(bionlpDoc.plainText.substring(t.getBegin(), t.getEnd()));
			} catch (Exception ex) {
			    System.err.println("ERR: " + e.getId() + ", '" + bionlpDoc.plainText +"', " + bionlpDoc.plainText.length());
			    throw new RuntimeException(ex);
			}
			if (termType == null)
				t.setType(e.getType());
			else
				t.setType(termType);

			bionlpDoc.annotations.add(t);

			if (deriveEntityNotes)
				addNote(e);
		}
		
		public void addNote(Entity e) {
			final AnnotatorNote an = new AnnotatorNote();
			an.setId(toAnnotatorNoteId(toTermId(e.getId())));
			an.setReferredId(e.getId());
			an.setNoteText(e.getOrigId());
			bionlpDoc.annotations.add(an);
		}

		/**
		 * Add a {@link Relation}s for each type specified for the given
		 * {@link Pair}. Multiple types can be defined by using the literal pipe
		 * character '|' as a delimiter.
		 * 
		 * @param p
		 */
		public void addPair(Pair p) {

			final String types;
			if (relationType != null) { 
			    types = relationType;
			} else if (p.getType() != null) {
			    types = p.getType();
			} else { 
			    types = DEFAULT_TYPE ;
			}
			    

			int i = 0;
			for (String type : types.split(Pattern.quote("|"))) {
				Relation r = new Relation();
				r.setId(toRelationId(p.getId() + ":" + (i++)));
				r.addArgument("Arg1", toTermId(p.getE1().getId()));
				r.addArgument("Arg2", toTermId(p.getE2().getId()));
				r.setType(type);

				// // append true/false to indicate interaction
				// if (writeAllPairs)
				// r.setType(r.getType() + "_" + p.isInteraction());

				bionlpDoc.annotations.add(r);
			}
		}

		public void addEquiv(Entity e1, Entity e2) {
			Equiv e = new Equiv();
			e.setId(null);
			e.setTerm1(toTermId(e1.getId()));
			e.setTerm2(toTermId(e2.getId()));

			bionlpDoc.annotations.add(e);
		}

		public void store() throws IOException {
			File dir = new File(outDir, corpus);
			dir.mkdir();
			bionlpDoc.store(dir);
		}

	}

	public void startCorpus(Corpus corpus) {
		outDir.mkdir();
		state = new State();
		state.corpus = corpus.getId();
	}

	public void startDocument(Document document) {
		state.newDocument(document);
	}

	public void processSentence(Sentence sentence) {
		state.newSentence(sentence.getText());
		for (Entity e : sentence.getEntities()) {
			state.addEntity(e);
		}

		for (Pair e : (writeAllPairs ? sentence.getAllPairs() : sentence
				.getPositivePairs())) {
			state.addPair(e);
		}

		if (deriveEquivs)
			state.equivCache.addAll(sentence.getEntities());
	}

	void searchEquivalents(List<Entity> entities) {
		for (int i = 0; i < entities.size(); i++) {
			Entity e1 = entities.get(i);
			if (e1.getOrigId() == null)
				continue;
			for (int j = i + 1; j < entities.size(); j++) {
				Entity e2 = entities.get(j);
				if (e2.getOrigId() == null)
					continue;
				if (e1.getOrigId().equals(e2.getOrigId()))
					state.addEquiv(e1, e2);

			}
		}
	}

	public void endCorpus() {
		state = null;
	}

	public void endDocument() {

		if (deriveEquivs)
			searchEquivalents(state.equivCache);

		try {
			state.store();
		} catch (Exception e) {
			throw new RuntimeException(e);
		}
	}

}
