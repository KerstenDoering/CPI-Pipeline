package org.learningformat.impl;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.Hashtable;
import java.util.List;
import java.util.Map;

import org.learningformat.api.Bracketing;
import org.learningformat.api.CharOffset;
import org.learningformat.api.Document;
import org.learningformat.api.Entity;
import org.learningformat.api.Pair;
import org.learningformat.api.Parse;
import org.learningformat.api.Sentence;
import org.learningformat.api.Tokenization;
import org.learningformat.api.CharOffset.SingleCharOffset;

public class DefaultSentence extends DefaultElement implements Sentence {
	protected String origId;
	protected String text;
	protected Document document;
	protected List<Pair> allPairs;
	protected List<Pair> positivePairs;
	protected boolean positivePairsFiltered = false;
	protected List<Entity> entities;
	protected Map<String, Tokenization> tokenizations;
	protected Map<String, Parse> parses;
	protected Map<String, Bracketing> bracketings;
	protected CharOffset charOffset = CharOffset.EMPTY_CHAR_OFFSET;
	protected String type;
	
	/* (non-Javadoc)
	 * @see org.unifiedformat.impl.Entity#getCharOffset()
	 */
	@Override
	public CharOffset getCharOffset() {
		return charOffset;
	}
	/* (non-Javadoc)
	 * @see org.unifiedformat.impl.Entity#setCharOffset(org.unifiedformat.api.CharOffset)
	 */
	@Override
	public void setCharOffset(CharOffset charOffset) {
		this.charOffset = charOffset;
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see org.unifiedformat.impl.Sentence#getText()
	 */
	public String getText() {
		return text;
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see org.unifiedformat.impl.Sentence#setText(java.lang.String)
	 */
	public void setText(String text) {
		this.text = text;
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see org.unifiedformat.impl.Sentence#getDocument()
	 */
	public Document getDocument() {
		return document;
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see
	 * org.unifiedformat.impl.Sentence#setDocument(org.unifiedformat.impl.Document
	 * )
	 */
	public void setDocument(Document document) {
		if (this.document != null)
			throw new IllegalStateException();
		this.document = document;
		this.document.addSentence(this);
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see org.unifiedformat.api.Sentence#getInteractions()
	 */
	public List<Pair> getAllPairs() {
		if (allPairs != null)
			return allPairs;
		return Collections.emptyList();
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see org.unifiedformat.api.Sentence#setInteractions(java.util.List)
	 */
	public void addInteraction(Pair interaction) {
		if (allPairs == null) {
			allPairs = new ArrayList<Pair>(2);
		}
		allPairs.add(interaction);
		positivePairsFiltered = false;
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see org.unifiedformat.api.Sentence#getEntities()
	 */
	public List<Entity> getEntities() {
		if (entities != null)
			return entities;
		return Collections.emptyList();
	}

	public Entity findEntity(String id) {
		for (Entity en : entities) {
			if (id.equals(en.getId())) {
				return en;
			}
		}
		return null;
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see org.unifiedformat.api.Sentence#setEntities(java.util.List)
	 */
	public void addEntity(Entity entity) {
		if (entities == null)
			entities = new ArrayList<Entity>(6);
		this.entities.add(entity);
	}

	@Override
	public List<Pair> getPositivePairs() {
		if (!positivePairsFiltered) {
			filterPositivePairs();
		}
		if (positivePairs != null)
			return positivePairs;
		return Collections.emptyList();
	}

	private void filterPositivePairs() {
		if (allPairs != null) {
			for (Pair p : allPairs) {
				if (p.isInteraction()) {
					if (positivePairs == null) {
						positivePairs = new ArrayList<Pair>(2);
					}
					positivePairs.add(p);
				}
			}
		}
		positivePairsFiltered = true;
	}

	@Override
	public void addParse(Parse parse) {
		if (parses == null) {
			parses = new Hashtable<String, Parse>();
		}
		parses.put(parse.getParser(), parse);
	}

	@Override
	public void addTokenization(Tokenization tokenization) {
		if (tokenizations == null) {
			tokenizations = new Hashtable<String, Tokenization>();
		}
		tokenizations.put(tokenization.getTokenizer(), tokenization);
	}

	@Override
	public Parse getParse(String parser) {
		if (parses != null) {
			return parses.get(parser);
		}
		return null;
	}

	@Override
	public Collection<Parse> getParses() {
		if (parses != null) {
			return parses.values();
		}
		return Collections.<Parse>emptySet();
	}

	@Override
	public Tokenization getTokenization(String tokenizer) {
		if (tokenizations != null) {
			return tokenizations.get(tokenizer);
		}
		return null;
	}

	@Override
	public Collection<Tokenization> getTokenizations() {
		if (tokenizations != null) {
			return tokenizations.values();
		}
		return Collections.<Tokenization>emptySet();
	}

	@Override
	public void removeParse(String parser) {
		if (parses != null) {
			parses.remove(parser);
		}
	}

	@Override
	public void removeTokenization(String tokenizer) {
		if (tokenizations != null)
			if (tokenizations.remove(tokenizer) != null)
				return;
		throw new IllegalStateException("Attempted to remove absent tokenization '" + tokenizer +"'");
	}

	@Override
	public void addBracketing(Bracketing bracketing) {
		if (bracketings == null) {
			bracketings = new Hashtable<String, Bracketing>();
		}
		bracketings.put(bracketing.getParser(), bracketing);
	}

	@Override
	public Bracketing getBracketing(String parser) {
		if (bracketings != null) {
			return bracketings.get(parser);
		}
		return null;
	}

	@Override
	public Collection<Bracketing> getBracketings() {
		if (bracketings != null) {
			return bracketings.values();
		}
		return Collections.emptySet();
	}

	@Override
	public void removeBracketing(String parser) {
		if (bracketings != null)
			if (bracketings.remove(parser) != null)
				return;
		throw new IllegalStateException("Attempted to remove absent bracketing '" + parser + "'");
	}

	@Override
	public String substring(SingleCharOffset singleCharOffset) {
		return text.substring(singleCharOffset.getStart(), singleCharOffset.getEnd());
	}
	
	@Override
	public String toString() {
		return super.toString() + 
		"  charOffset = '" + charOffset + "'\n" +
		"  text = '" + text + "'\n" 
		//"  corpus.source = " + (corpus == null ? "(none)" : corpus.getSource()) + "\n" +
		;
	}

}
