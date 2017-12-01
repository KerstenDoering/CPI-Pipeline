package org.learningformat.transform;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;

import javax.xml.parsers.ParserConfigurationException;

import org.learningformat.api.Corpus;
import org.learningformat.api.Document;
import org.learningformat.api.Entity;
import org.learningformat.api.Sentence;
import org.learningformat.xml.CorpusListener;
import org.learningformat.xml.Parser;
import org.xml.sax.SAXException;

/**
 * Perform basic consistency check on XML corpus.
 * 
 * @author Illes Solt
 * 
 */
public class ConsistencyChecker implements CorpusListener {

	private static final String USAGE = "Usage: java ... "
			+ ConsistencyChecker.class.getCanonicalName()
			+ " [--help] [corpus.xml ...]";

	protected int docsProcessed = 0;
	protected int sentencesProcessed = 0;
	protected final long startMillis = System.currentTimeMillis();

	public static void main(String[] args) {

		try {
			if (args.length < 1) {
				System.err.println(USAGE);
				System.exit(1);
			}
			int i = 0;
			while (args[i].startsWith("-")) {
				if (args[i].equals("--help")) {
					System.out.println(USAGE);
					System.exit(0);
				} else {
					throw new IllegalArgumentException("Unrecognized option: "
							+ args[i]);
				}
				i++;
			}

			ConsistencyChecker lint = new ConsistencyChecker();
			if (i == args.length) {
				// pipe mode
				lint.process(null);
			} else {
				// file list mode
				for (; i < args.length; i++) {
					lint.process(args[i]);
				}
			}
			// debug
			{
				System.err.println("Documents seen: " + lint.docsProcessed);
				System.err.println("Sentences seen: " + lint.sentencesProcessed);
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
	private void process(String path) throws SAXException, IOException,
			ParserConfigurationException {
		InputStream in = null;
		try {
			if (path != null) {
				System.err.println("INFO: Processing '" + path + "'...");
				in = new FileInputStream(path);
			} else {
				System.err.println("INFO: Processing standard input...");
				in = System.in;
			}

			// Parse all linguistic information
			Parser parser = new Parser(this);

			// release documents immediately after processing
			// for efficiency only
			parser.setImmediatelyRemoveDocuments(true);

			// Do not try to recover from errors.
			parser.setTryToRecoverFromErrors(false);
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
	    System.err.println("Processing corpus '" + corpus.getSource() + "' ...");
	}

	@Override
	public void startDocument(Document document) {
		docsProcessed++;
		if ((docsProcessed % 1000) == 0)
			System.err
					.println("processed "
							+ docsProcessed
							+ " docs ("
							+ (docsProcessed / ((System.currentTimeMillis() - startMillis) / 1000f))
							+ " docs/sec)");

		// System.err.println("Doc: " + document);
	}

	@Override
	public void processSentence(Sentence sentence) {
		sentencesProcessed++;
		for (Entity e : sentence.getEntities()) {
			if (e.getText() == null) {
			    throw new NullPointerException("entity lacking text: " + e.getId());  
			} else {
			    final String coveredText = sentence.substring(e.getCharOffset().getCharOffsets()[0]);
			    if (!coveredText.equals(e.getText()))
				throw new IllegalStateException("Entity text '" + e.getText() + "'[" + e.getText().length()+ "] " +
						"does not match covered sentence text '" + coveredText +"'["+coveredText.length()+"]");
			}
		}
	}

	@Override
	public void endCorpus() {
	}

	@Override
	public void endDocument() {
	}

}
