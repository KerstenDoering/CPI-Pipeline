package org.learningformat.impl;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.learningformat.api.Bracketing;
import org.learningformat.api.CharOffsetMapEntry;
import org.learningformat.api.Tokenization;
import org.learningformat.api.CharOffset.SingleCharOffset;

public class DefaultBracketing implements Bracketing {

	protected String bracketing;
	protected Map<SingleCharOffset, SingleCharOffset> bracketingSentenceMap;
	protected List<CharOffsetMapEntry> charOffsetMapEntries;
	protected String parser;
	protected Map<SingleCharOffset, SingleCharOffset> sentenceBracketingMap;

	protected Tokenization tokenization;

	@Override
	public void addCharOffsetMapEntry(CharOffsetMapEntry charOffsetMapEntry) {
		if (sentenceBracketingMap == null) {
			sentenceBracketingMap = new HashMap<SingleCharOffset, SingleCharOffset>(16);
		}
		if (bracketingSentenceMap == null) {
			bracketingSentenceMap = new HashMap<SingleCharOffset, SingleCharOffset>(16);
		}
		if (charOffsetMapEntries == null) {
			charOffsetMapEntries = new ArrayList<CharOffsetMapEntry>(16);
		}
		
		sentenceBracketingMap.put(charOffsetMapEntry.getSentenceTextCharOffset(), charOffsetMapEntry.getBracketingCharOffset());
		bracketingSentenceMap.put(charOffsetMapEntry.getBracketingCharOffset(), charOffsetMapEntry.getSentenceTextCharOffset());
		charOffsetMapEntries.add(charOffsetMapEntry);
	}
	public String getBracketing() {
		return bracketing;
	}

	@Override
	public List<CharOffsetMapEntry> getCharOffsetMapEntries() {
		return charOffsetMapEntries;
	}

	@Override
	public String getParser() {
		return parser;
	}

	@Override
	public Tokenization getTokenization() {
		return tokenization;
	}

	@Override
	public void removeCharOffsetMapEntry(CharOffsetMapEntry charOffsetMapEntry) {
		if (sentenceBracketingMap != null) {
			sentenceBracketingMap.remove(charOffsetMapEntry.getSentenceTextCharOffset());
		}
		if (bracketingSentenceMap != null){
			bracketingSentenceMap.remove(charOffsetMapEntry.getBracketingCharOffset());
		}
		if (charOffsetMapEntries != null) {
			charOffsetMapEntries.remove(charOffsetMapEntry);
		}
		
	}

	public void setBracketing(String bracketing) {
		this.bracketing = bracketing;
	}

	@Override
	public void setParser(String parser) {
		this.parser = parser;
	}

	@Override
	public void setTokenization(Tokenization tokenization) {
		this.tokenization = tokenization;
	}

	@Override
	public SingleCharOffset toBracketingCharOffset(SingleCharOffset sentenceTextCharOffset) {
		if (sentenceBracketingMap != null) {
			return sentenceBracketingMap.get(sentenceTextCharOffset);
		}
		return null;
	}

	@Override
	public SingleCharOffset toSentenceTextCharOffset(
			SingleCharOffset bracketingCharOffset) {
		if (bracketingSentenceMap != null){
			return bracketingSentenceMap.get(bracketingCharOffset);
		}
		return null;
	}

}
