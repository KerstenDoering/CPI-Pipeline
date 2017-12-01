package org.learningformat.impl;

import java.util.Collection;
import java.util.HashSet;
import java.util.Set;

import org.learningformat.api.Corpus;
import org.learningformat.api.Document;

public class DefaultCorpus extends DefaultElement implements Corpus {
	protected String source;
	protected Set<Document> documents = new HashSet<Document>();

	/* (non-Javadoc)
	 * @see org.unifiedformat.impl.Corpus#getSource()
	 */
	public String getSource() {
		return source;
	}

	/* (non-Javadoc)
	 * @see org.unifiedformat.impl.Corpus#setSource(java.lang.String)
	 */
	public void setSource(String source) {
		this.source = source;
	}

	@Override
	public Collection<Document> getDocuments() {
		return documents;
	}
	
}
