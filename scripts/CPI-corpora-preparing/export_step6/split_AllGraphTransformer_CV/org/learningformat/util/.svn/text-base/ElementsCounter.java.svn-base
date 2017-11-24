package org.learningformat.util;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.Reader;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import org.learningformat.api.Corpus;
import org.learningformat.api.Document;
import org.learningformat.api.Pair;
import org.learningformat.api.Sentence;
import org.learningformat.impl.DefaultElementFactory;
import org.learningformat.xml.CorpusListener;
import org.learningformat.xml.Parser;

public class ElementsCounter implements CorpusListener {
	
	public static void main(String[] args) {
		try {
			
			if (args.length < 1) {
				throw new IllegalArgumentException("Min. 1 argument needed.");
			}
			
			OutputStreamWriter out = null;
			try {
				for (int i = 0; i < args.length; i++) {
					
					File inputFile = new File(args[i]);
					
					out = new OutputStreamWriter(new FileOutputStream(new File(inputFile.getParent() + File.separator + "svm-light-tk" + File.separator + inputFile.getName()+".txt")), "utf-8");
					
					Set<String> emptySet = Collections.emptySet();
					ElementsCounter tf = new ElementsCounter();
					org.learningformat.xml.Parser parser = new Parser(emptySet, emptySet, emptySet, new DefaultElementFactory(), tf);
					
					Reader in = null;
					try {
						
						System.out.println(inputFile.getName());
						
						in = new InputStreamReader(new FileInputStream(inputFile), "utf-8");
						parser.process(in);
						
						System.out.println("positivePairs="+ tf.positivePairs);
						System.out.println("negativePairs="+ tf.negativePairs);
						System.out.println("docs="+ tf.docs.size());
					} finally {
						if (in != null) {
							in.close();
						}
					}
				}
			} finally {
				if (out != null) {
					out.close();
				}
			}

		} catch (Exception e) {
			e.printStackTrace();
		}

	}
	protected StringBuilder buffer = new StringBuilder(512);

	protected Set<String> docs = new HashSet<String>();
	protected int negativePairs = 0;
	protected int positivePairs = 0;

	public ElementsCounter() {
		super();
	}

	@Override
	public void endCorpus() {
	}

	
	
	@Override
	public void endDocument() {
		
	}

	public int getDocumentsCount() {
		return docs.size();
	}

	public int getNegativePairs() {
		return negativePairs;
	}

	public int getPositivePairs() {
		return positivePairs;
	}

	@Override
	public void processSentence(Sentence sentence) {
		
		List<Pair> pairs = sentence.getAllPairs();
		
		if (pairs != null) {
			Set<String> uniquePairs = new HashSet<String>(pairs.size());
			for (Pair pair : pairs) {
				
				String e1Id = pair.getE1().getId();
				String e2Id = pair.getE2().getId();
				
				if (!e1Id.equals(e2Id)) {
					/* no self-interactions */
					
					/* check if this pair is unique */
					/* create a key in which the e1 and e2 ids are ordered alphabetically */
					String key = e1Id.compareTo(e2Id) > 0 ? e1Id +'|'+ e2Id : e2Id +'|'+ e1Id;
					if (!uniquePairs.contains(key)) {
						uniquePairs.add(key);
						
						if (pair.isInteraction()) {
							positivePairs++;
						}
						else {
							negativePairs++;
						}
						
						docs.add(sentence.getDocument().getId());
					}
				}
			}
		}
		
	}
	
	public void setNegativePairs(int negativePairs) {
		this.negativePairs = negativePairs;
	}

	@Override
	public void startCorpus(Corpus corpus) {
	}

	@Override
	public void startDocument(Document document) {
	}

}
