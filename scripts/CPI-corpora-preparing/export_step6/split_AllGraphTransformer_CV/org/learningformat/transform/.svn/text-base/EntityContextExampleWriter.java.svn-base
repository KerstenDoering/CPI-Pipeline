package org.learningformat.transform;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.learningformat.api.Dependency;
import org.learningformat.api.DependencyToken;
import org.learningformat.api.Entity;
import org.learningformat.api.LearningFormatConstants;
import org.learningformat.api.Pair;
import org.learningformat.api.Parse;
import org.learningformat.api.Sentence;
import org.learningformat.api.Token;
import org.learningformat.api.Tokenization;
import org.learningformat.util.PorterStemmer;

public class EntityContextExampleWriter extends AbstractExampleWriter implements ExampleWriter {

	public static enum Stemming {STEM, NSTEM}
	public static enum EntityPosition {ANYWHERE, BEGINNING, OUTSIDE}
	public static enum LengthsPolicy {FIXED, UP_TO}
	public static enum SelfReferences {NO_SELF_REF, WITH_SELF_REF}
	public static enum TokenType {ANYTHING, OTHER_ENTITY, SOME_ENTITY, THIS_AND_OTHER_ENTITY, THIS_ENTITY}
	
	private static class StringIndexProvider_ implements StringIndexProvider {
		
		
		public StringIndexProvider_() {
			super();
			getTokenIndex(LearningFormatConstants.PROT1, true);
			getTokenIndex(LearningFormatConstants.PROT2, true);
			getTokenIndex(LearningFormatConstants.PROT1_AND_PROT2, true);
			getTokenIndex(LearningFormatConstants.PROT, true);
		}

		public int getTokenIndex(String token, boolean isDependencyType) {
			String lower = null;
			if (isDependencyType) {
				lower = token.toUpperCase();
			}
			else {
				if (SvmLightDependencyTreeKernelTransformer.stemming.equals(Stemming.STEM)) {
					String stem = stemmer.stem(token);
					//System.out.println(token +" => "+ stem);
					lower = stem;
				}
				else {
					lower = token.toLowerCase();
				}
			}
			Integer i = tokenIndex.get(lower);
			if (i == null) {
				i = Integer.valueOf(currentIndex++);
				tokenIndex.put(lower, i);
				indexToken.put(i, lower);
			}
			return i.intValue();
		}

		public int getTokenIndex(Token token, Entity thisEntity, Entity otherEntity) {
			boolean isThis = thisEntity.getCharOffset().overlaps(token.getCharOffset());
			boolean isOther = otherEntity.getCharOffset().overlaps(token.getCharOffset());
			if (isThis && isOther) {
				return getTokenIndex(LearningFormatConstants.PROT1_AND_PROT2, true);
			}
			else if (isThis) {
				return getTokenIndex(LearningFormatConstants.PROT1, true);
			}
			else if (isOther) {
				return getTokenIndex(LearningFormatConstants.PROT2, true);
			}
			else if (token.isEntity()) {
				return getTokenIndex(LearningFormatConstants.PROT, true);
			}
			else {
				return getTokenIndex(token.getText(), false);
			}
		}

		@Override
		public int getTokenIndex(Token token, Pair pair) {
			throw new UnsupportedOperationException();
		}
	}

	private static int currentIndex = 0;

	private static final Map<String, Integer> tokenIndex = new HashMap<String, Integer>();
	private static final Map<Integer, String> indexToken = new HashMap<Integer, String>();
	private static PorterStemmer stemmer = new PorterStemmer();
	
	public static String getToken(int index) {
		return indexToken.get(Integer.valueOf(index));
	}
	
	protected EntityPosition entityPosition;;
	protected LengthsPolicy lengthsPolicy;;
	protected SelfReferences selfReferences;
	protected String parser;
	protected int qGramLength;

	private static StringIndexProvider_ stringIndexProvider_Inst = new StringIndexProvider_();
	
	public EntityContextExampleWriter(String parser, int gramLength,
			LengthsPolicy lengthsPolicy, EntityPosition entityPosition, SelfReferences selfReferences) {
		super();
		this.parser = parser;
		this.qGramLength = gramLength;
		this.lengthsPolicy = lengthsPolicy;
		this.entityPosition = entityPosition;
		this.selfReferences = selfReferences;
	}

	protected List<QPath> addQGrams(Dependency dep, boolean isDirectionUpBottom, int lengthRest, Entity thisEntity, Entity otherEntity, List<QPath> qGrams) {
		
		DependencyToken currentToken = isDirectionUpBottom ? dep.getT2() : dep.getT1();
		
		List<QPath> newQGrams = new ArrayList<QPath>();
		
			/* prolog the available qGrams */
			for (QPath qg : qGrams) {
				if (!qg.getTokenIds().contains(currentToken.getId())) {
					/* only add if the node is not there yet */
					QPath newQGram = qg.clone();
					newQGram.addDependency(
							currentToken.getId(), 
							stringIndexProvider_Inst.getTokenIndex(currentToken, thisEntity, otherEntity), 
							stringIndexProvider_Inst.getTokenIndex(dep.getType(), true));
					newQGrams.add(newQGram);
				}
			}
			
			if (lengthRest <= 1) {
				return newQGrams;
			}
			else {
				List<QPath> result = new ArrayList<QPath>();
				/* dependents */
				if (currentToken.getDependentsCount() > 0) {
					for (Dependency d : currentToken.getDependents()) {
						result.addAll(addQGrams(d, true, lengthRest -1, thisEntity, otherEntity, newQGrams));
					}
				}
				/* governors */
				if (currentToken.getGovernorsCount() > 0) {
					for (Dependency d : currentToken.getGovernors()) {
						result.addAll(addQGrams(d, false, lengthRest -1, thisEntity, otherEntity, newQGrams));
					}
				}
				return result;
			}
	
	
			
	}

	protected Entity getEntity(boolean isFirstEntity, Pair pair) {
		return isFirstEntity ? pair.getE1() : pair.getE2();
	}
	
	protected Collection<QPath> listQGrams(int qGramLength, DependencyToken dt, Entity thisEntity, Entity otherEntity) {
		HashSet<QPath> result = new HashSet<QPath>();
		List<QPath> initialList = new ArrayList<QPath>();
		int firstTokenIndex = stringIndexProvider_Inst.getTokenIndex(dt, thisEntity, otherEntity);
		String firstTokenId = dt.getId();
		initialList.add(new QPath(qGramLength, firstTokenId, firstTokenIndex));
		
		if (dt.getDependentsCount() > 0) {
			for (Dependency dep : dt.getDependents()) {
				result.addAll(addQGrams(dep, true, qGramLength - 1, thisEntity, otherEntity, initialList));
			}
		}
		if (dt.getGovernorsCount() > 0) {
			for (Dependency dep : dt.getGovernors()) {
				result.addAll(addQGrams(dep, false, qGramLength - 1, thisEntity, otherEntity, initialList));
			}
		}
		return result;
	}
	
	@Override
	public void write(Pair pair, Sentence sentence, Appendable out) throws IOException {
//		System.out.println(pair.getId());
//		StringBuffer out = new StringBuffer();
		
		out.append(pair.isInteraction() ? SvmLightTreeKernelConstants.POSITIVE_EXAMPLE : SvmLightTreeKernelConstants.NEGATIVE_EXAMPLE);
		out.append(SvmLightTreeKernelConstants.SPACE);
		out.append(SvmLightTreeKernelConstants.HASH);

		Parse parse = sentence.getParse(parser);

		Entity thisEntity = getEntity(true, pair); 
		Entity otherEntity = getEntity(false, pair); 
		writeEntity(thisEntity, otherEntity, parse.getTokenization(), out);
		writeEntity(otherEntity, thisEntity, parse.getTokenization(), out);
		
		out.append(SvmLightTreeKernelConstants.HASH);
		out.append(pair.getId());

		out.append(SvmLightTreeKernelConstants.EOL);
		
		//System.out.println(out.toString());
		
	}
	
	protected void writeEntity(Entity thisEntity, Entity otherEntity, Tokenization tokenization, Appendable out) throws IOException {
		
		Set<String> occurences = new HashSet<String>();
		for (Token t : tokenization.getTokens()) {
			if (t instanceof DependencyToken) {
				DependencyToken dt = (DependencyToken) t;
				if (thisEntity.getCharOffset().overlaps(dt.getCharOffset())) {
					addEntityOccurence(dt, thisEntity, otherEntity, occurences);
				}
			}
			else {
				throw new IllegalStateException();
			}
		}
		out.append(QGramConstants.LEFT_BRACKET);
		for (String occ : occurences) {
			out.append(occ);
		}
		out.append(QGramConstants.RIGHT_BRACKET);
		
	}
	
	private void removeSelfDependencies(Collection<QPath> qGrams) {
		
		if (qGrams.size() > 0) {
			Iterator<QPath> it = qGrams.iterator();
			while (it.hasNext()) {
				QPath qGram = it.next();
				if (qGram.getData()[0] == qGram.getData()[2]) {
					it.remove();
				}
			}
		}
		
	}
	
	protected void addEntityOccurence(DependencyToken dt, Entity thisEntity, Entity otherEntity, Set<String> occurences) throws IOException {
		
		
		
		if (EntityPosition.BEGINNING.equals(entityPosition) 
				&& LengthsPolicy.FIXED.equals(lengthsPolicy)) {
			
			Collection<QPath> qGrams = listQGrams(qGramLength, dt, thisEntity, otherEntity);
			
			switch (selfReferences) {
			case NO_SELF_REF:
				removeSelfDependencies(qGrams);
				break;
			default:
				break;
			}
			
			StringBuilder out = new StringBuilder();
			if (qGrams != null && qGrams.size() > 0) {
				out.append(QGramConstants.LEFT_BRACKET);
				for (QPath qGram : qGrams) {
					qGram.write(out);
				}
				out.append(QGramConstants.RIGHT_BRACKET);
			}
			occurences.add(out.toString());
		}
		else if (EntityPosition.OUTSIDE.equals(entityPosition) 
				&& LengthsPolicy.UP_TO.equals(lengthsPolicy)) {
			
			Collection<QPath> qGrams = listQGrams(qGramLength, dt, thisEntity, otherEntity);
			
			
			switch (selfReferences) {
			case NO_SELF_REF:
				removeSelfDependencies(qGrams);
				break;
			default:
				break;
			}
			
			
			StringBuilder out = new StringBuilder();
			if (qGrams != null && qGrams.size() > 0) {
				HashSet<QPath> allSubgrams = new HashSet<QPath>();
				allSubgrams.addAll(qGrams);
				addSubgramsUpTo(qGrams, qGramLength, allSubgrams);
				
				out.append(QGramConstants.LEFT_BRACKET);
				for (QPath qGram : allSubgrams) {
					qGram.write(out);
				}
				out.append(QGramConstants.RIGHT_BRACKET);
			}
			occurences.add(out.toString());
		}
		else {
			throw new IllegalStateException();
		}
		
	}
	
	private void addSubgramsUpTo(Collection<QPath> qGrams, int qGramLength, Set<QPath> result) {
		int minSubgramLength = 2;
		int maxSubgramLength = qGramLength -1;
		for (QPath qGram : qGrams) {
			for (int i = minSubgramLength; i <= maxSubgramLength; i++) {
				qGram.addSubgrams(i, result);
			}
		}
		
	}
	
}
