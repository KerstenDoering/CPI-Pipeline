package org.learningformat.api;

import java.util.List;


/**
 * Most corpora contain one sentence per document
 * 
 * @author Peter Palaga
 *
 */
public interface Document extends Element, TextProvider {

	/**
	 * @return the id of the document in the source corpus
	 */
	public String getOrigId();

	/**
	 * @param origId the id of the document in the source corpus
	 */
	public void setOrigId(String origId);

	/**
	 * @return the corpus to which this document belogs
	 */
	public Corpus getCorpus();

	/**
	 * @param corpus the corpus to which this document belongs
	 */
	public void setCorpus(Corpus corpus);
		
	/**
	 * @return the corpus to which this document belogs
	 */
	public List<Sentence> getSentences();
	
	
	public void addSentence(Sentence s);
	
	

}