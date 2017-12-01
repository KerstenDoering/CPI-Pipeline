package org.learningformat.impl;

import org.learningformat.api.CharOffsetMapEntry;
import org.learningformat.api.CharOffset.SingleCharOffset;

public class DefaultCharOffsetMapEntry implements CharOffsetMapEntry {
	
	public static final char COLON = ':';
	protected SingleCharOffset sentenceTextCharOffset;
	protected SingleCharOffset bracketingCharOffset;
	
	

	@Override
	public boolean equals(Object o) {
		if (o instanceof CharOffsetMapEntry) {
			CharOffsetMapEntry en = (CharOffsetMapEntry) o;
			return en.getBracketingCharOffset().equals(bracketingCharOffset) && en.getSentenceTextCharOffset().equals(sentenceTextCharOffset);
		}
		return false;
	}

	@Override
	public int hashCode() {
		return 31*sentenceTextCharOffset.hashCode() + bracketingCharOffset.hashCode();
	}

	@Override
	public String toString() {
		return append(new StringBuilder(15)).toString();
	}

	public StringBuilder append(StringBuilder sb) {
		return bracketingCharOffset.append(sentenceTextCharOffset.append(sb).append(COLON));
	}

	@Override
	public SingleCharOffset getSentenceTextCharOffset() {
		return sentenceTextCharOffset;
	}

	@Override
	public SingleCharOffset getBracketingCharOffset() {
		return bracketingCharOffset;
	}

	@Override
	public void setSentenceTextCharOffset(SingleCharOffset charOffset) {
		this.sentenceTextCharOffset = charOffset;
	}

	@Override
	public void setBracketingCharOffset(SingleCharOffset charOffset) {
		this.bracketingCharOffset = charOffset;
	}

}
