package org.learningformat.impl;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import org.learningformat.api.CharOffset;
import org.learningformat.api.Token;
import org.learningformat.api.Tokenization;

public class DefaultTokenization implements Tokenization {
	
	protected String tokenizer;

	protected List<Token> tokens;
	
	@Override
	public void addToken(Token token) {
		if (tokens == null) {
			tokens = new ArrayList<Token>(16);
		}
		tokens.add(token);
	}

	public String getTokenizer() {
		return tokenizer;
	}

	@Override
	public List<Token> getTokens() {
		if (tokens == null)
			return Collections.emptyList();
		return tokens;
		
	}

	@Override
	public void removeToken(Token token) {
		if (tokens != null) {
			tokens.remove(token);
		}
	}

	public void setTokenizer(String tokenizer) {
		this.tokenizer = tokenizer;
	}

	@Override
	public List<Token> findOverlappingTokens(CharOffset charOffset) {
		if (tokens == null)
			return Collections.emptyList();
		
		List<Token> result = new ArrayList<Token>(charOffset.getCharOffsets().length);
		
		for (Token t : tokens) {
			if (t.getCharOffset().overlaps(charOffset)) {
				result.add(t);
			}
		}
		
		return result;
	}

	@Override
	public Token getToken(String id) {
		if (tokens != null) {
			for (Token t : tokens) {
				if (id.equals(t.getId())) {
					return t;
				}
			}
		}
		return null;
	}


}
