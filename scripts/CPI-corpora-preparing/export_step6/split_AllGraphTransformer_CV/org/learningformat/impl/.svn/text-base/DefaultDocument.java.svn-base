package org.learningformat.impl;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import org.learningformat.api.Corpus;
import org.learningformat.api.Document;
import org.learningformat.api.Sentence;

public class DefaultDocument extends DefaultElement implements Document {
	protected Corpus corpus;
	protected List<Sentence> sentences;
	
	protected String text;
	
	
	@Override
	public void setText(String text) {
		this.text = text;
	}
	
	@Override
	public String getText() {
		return text;
	}
	
	/* (non-Javadoc)
	 * @see org.unifiedformat.impl.Document#getCorpus()
	 */
	public Corpus getCorpus() {
		return corpus;
	}
	
	/**
	 * Add/remove document to/from corpus.
	 * @param corpus if not <code>null</code>, add document to corpus; if <code>null</code>, remove document from previously associated corpus if any  
	 */
	public void setCorpus(Corpus corpus) {
		if (corpus == null) {
			if (this.corpus != null)
				this.corpus.getDocuments().remove(this);
			this.corpus = null;
		} else { /* corpus != null */
			if (this.corpus != null)
				throw new IllegalStateException("corpus already set");
			else
			{
				this.corpus = corpus;
				this.corpus.getDocuments().add(this);
			}
		}
	}
		
	@Override
	public List<Sentence> getSentences() {
		if (sentences != null)
			return sentences;
		return Collections.emptyList();
	}
	
	@Override
	public String toString() {
		return super.toString() + 
			"  origId = '" + origId + "'\n" +
			"  text = '" + text + "'\n" +
			"  corpus.source = " + (corpus == null ? "(none)" : corpus.getSource()) + "\n" +
			"  sentences = " + (sentences == null ? null : Arrays.toString(sentences.toArray())) +"\n"
			;
	}

	@Override
	public void addSentence(Sentence s) {
		if (s.getDocument() != this)
			throw new UnsupportedOperationException("use Sentence#setDocument() instead");
		if (sentences == null)
			sentences = new ArrayList<Sentence>(20);
		sentences.add(s);
	}
	
}
