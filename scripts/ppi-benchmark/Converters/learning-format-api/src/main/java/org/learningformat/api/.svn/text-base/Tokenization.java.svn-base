package org.learningformat.api;

import java.util.List;

public interface Tokenization {
	public String getTokenizer();
	public void setTokenizer(String tokenizer);
	
	public List<Token> getTokens();
	public Token getToken(String id); 
	
	public void addToken(Token token);
	public void removeToken(Token token);
	
	public List<Token> findOverlappingTokens(CharOffset charOffset);

}
