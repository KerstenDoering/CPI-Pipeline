package org.learningformat.api;

import java.util.Collection;
import java.util.List;

import org.learningformat.api.CharOffset.SingleCharOffset;

/**
 * One sentence of text.
 * 
 * @author Peter Palaga
 *
 */
public interface Sentence extends Element, CharOffsetProvider, TextProvider {

	/**
	 * @return the id of the sentence in the source corpus.
	 */
	public String getOrigId();

	/**
	 * @param origId the id of the sentence in the source corpus.
	 */
	public void setOrigId(String origId);

	/**
	 * @return untokenized original text of the sentence.
	 */
	public String getText();

	/**
	 * @param text untokenized original text of the sentence.
	 */
	public void setText(String text);

	/**
	 * @return the document to which this sentence belongs.
	 */
	public Document getDocument();

	/**
	 * @param document the document to which this sentence belongs.
	 */
	public void setDocument(Document document);
	
	/**
	 * @return Interactions annotated in this sentence.
	 */
	public List<Pair> getAllPairs();
	
	/**
	 * @return Interactions annotated in this sentence.
	 */
	public List<Pair> getPositivePairs();
	
	/**
	 * @return Named entities annotated in this sentence.
	 */
	public List<Entity> getEntities();

	public Entity findEntity(String id);

	/**
	 * @param interaction
	 */
	public void addInteraction(Pair interaction);
	
	/**
	 * @param entity
	 */
	public void addEntity(Entity entity);
	
	public void addTokenization(Tokenization tokenization);
	public Collection<Tokenization> getTokenizations();
	public Tokenization getTokenization(String tokenizer);
	public void removeTokenization(String tokenizer);

	public void addParse(Parse parse);
	public Collection<Parse> getParses();
	public Parse getParse(String parser);
	public void removeParse(String parser);

	public void addBracketing(Bracketing bracketing);
	public Collection<Bracketing> getBracketings();
	public Bracketing getBracketing(String parser);
	public void removeBracketing(String parser);
	
	public String substring(SingleCharOffset singleCharOffset);
	
}