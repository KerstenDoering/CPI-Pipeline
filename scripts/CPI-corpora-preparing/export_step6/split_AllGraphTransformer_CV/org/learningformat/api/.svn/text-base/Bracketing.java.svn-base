package org.learningformat.api;

import java.util.List;

import org.learningformat.api.CharOffset.SingleCharOffset;

public interface Bracketing {
	
	public String getParser();
	public void setParser(String parser);
	
	public Tokenization getTokenization();
	public void setTokenization(Tokenization tokenization);
	
	public String getBracketing();
	public void setBracketing(String bracketing);
	
	
	
	public SingleCharOffset toBracketingCharOffset(SingleCharOffset sentenceTextCharOffset);
	public SingleCharOffset toSentenceTextCharOffset(SingleCharOffset bracketingCharOffset);
	
	public void addCharOffsetMapEntry(CharOffsetMapEntry charOffsetMapEntry);
	public void removeCharOffsetMapEntry(CharOffsetMapEntry charOffsetMapEntry);
	public List<CharOffsetMapEntry> getCharOffsetMapEntries();
}
