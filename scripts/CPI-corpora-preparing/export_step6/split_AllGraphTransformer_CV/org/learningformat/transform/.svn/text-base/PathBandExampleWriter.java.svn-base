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
import java.util.TreeSet;

import org.learningformat.api.Dependency;
import org.learningformat.api.DependencyToken;
import org.learningformat.api.Entity;
import org.learningformat.api.LearningFormatConstants;
import org.learningformat.api.Pair;
import org.learningformat.api.Parse;
import org.learningformat.api.Sentence;
import org.learningformat.api.Token;
import org.learningformat.api.Tokenization;
import org.learningformat.transform.EntityContextExampleWriter.LengthsPolicy;
import org.learningformat.transform.EntityContextExampleWriter.Stemming;
import org.learningformat.transform.SvmLightDependencyTreeKernelTransformer.DependencyTypeGeneralization;
import org.learningformat.util.PorterStemmer;

public class PathBandExampleWriter extends AbstractExampleWriter implements ExampleWriter {

	private static class StringIndexProvider_ implements StringIndexProvider {
		public int getTokenIndex(String token, boolean isDependencyType) {
			String lower = null;
			if (isDependencyType) {
				if (!SvmLightDependencyTreeKernelTransformer.dependencyTypeGeneralization.equals(DependencyTypeGeneralization.none)) {
					token = StanfordDependencyTypes.dependencyGeneralizer.get(token);
					if (token == null) {
						throw new IllegalStateException();
					}
				}
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
		
		@Override
		public int getTokenIndex(Token token, Entity thisEntity, Entity otherEntity) {
			throw new UnsupportedOperationException();
		}

		public int getTokenIndex(Token token, Pair pair) {
			boolean e1 = pair.getE1().getCharOffset().overlaps(token.getCharOffset());
			boolean e2 = pair.getE2().getCharOffset().overlaps(token.getCharOffset());
			if (e1 && e2) {
				return getTokenIndex(LearningFormatConstants.PROT1_AND_PROT2, false);
			}
			else if (e1) {
				return getTokenIndex(LearningFormatConstants.PROT1, false);
			}
			else if (e2) {
				return getTokenIndex(LearningFormatConstants.PROT2, false);
			}
			else if (token.isEntity()) {
				return getTokenIndex(LearningFormatConstants.PROT, false);
			}
			else {
				return getTokenIndex(token.getText(), false);
			}
		}
		
	}
	
	private static int currentIndex = 0; 
	public static final int DIRECTION_BOTTOM_UP = -1;
	
	public static final int DIRECTION_UP_BOTTOM = 1;

	private static final Map<Integer, String> indexToken = new HashMap<Integer, String>();
	public static final int INVALID_DIRECTION = 0;
	
	private static PorterStemmer stemmer = new PorterStemmer();
	private static StringIndexProvider_ stringIndexProvider_Inst = new StringIndexProvider_();
	private static final Map<String, Integer> tokenIndex = new HashMap<String, Integer>();
	
	
	static {
		stringIndexProvider_Inst.getTokenIndex(LearningFormatConstants.PROT1, false);
		stringIndexProvider_Inst.getTokenIndex(LearningFormatConstants.PROT2, false);
		stringIndexProvider_Inst.getTokenIndex(LearningFormatConstants.PROT1_AND_PROT2, false);
		stringIndexProvider_Inst.getTokenIndex(LearningFormatConstants.PROT, false);
	}
	public static String getToken(int index) {
		return indexToken.get(Integer.valueOf(index));
	}
	
//	public static int getTokenIndex(String token, boolean isDependencyType) {
//		String lower = null;
//		if (isDependencyType) {
//			lower = token.toUpperCase();
//		}
//		else {
//			if (SvmLightDependencyTreeKernelTransformer.stemming.equals(Stemming.STEM)) {
//				String stem = stemmer.stem(token);
//				//System.out.println(token +" => "+ stem);
//				lower = stem;
//			}
//			else {
//				lower = token.toLowerCase();
//			}
//		}
//		Integer i = tokenIndex.get(lower);
//		if (i == null) {
//			i = Integer.valueOf(currentIndex++);
//			tokenIndex.put(lower, i);
//			indexToken.put(i, lower);
//		}
//		return i.intValue();
//	}
//
//	public static int getTokenIndex(Token token, Entity thisEntity, Entity otherEntity) {
//		boolean isThis = thisEntity.getCharOffset().overlaps(token.getCharOffset());
//		boolean isOther = otherEntity.getCharOffset().overlaps(token.getCharOffset());
//		if (isThis && isOther) {
//			return getTokenIndex(LearningFormatConstants.PROT1_AND_PROT2, true);
//		}
//		else if (isThis) {
//			return getTokenIndex(LearningFormatConstants.PROT1, true);
//		}
//		else if (isOther) {
//			return getTokenIndex(LearningFormatConstants.PROT2, true);
//		}
//		else if (token.isEntity()) {
//			return getTokenIndex(LearningFormatConstants.PROT, true);
//		}
//		else {
//			return getTokenIndex(token.getText(), false);
//		}
//	};
	protected final int kBand;
	protected final LengthsPolicy lengthsPolicy;
	protected final String parser;

	protected final int qGramLengthMax;
	protected final int qGramLengthMin;

	
	
	public PathBandExampleWriter(String parser, int qGramLengthMin, int gramLengthMax, int kBand, LengthsPolicy lengthsPolicy) {
		super();
		this.parser = parser;
		this.qGramLengthMin = qGramLengthMin;
		this.qGramLengthMax = gramLengthMax;
		this.lengthsPolicy = lengthsPolicy;
		this.kBand = kBand;
	}
	
	protected List<QPath> addQPaths(Dependency dep, boolean isDirectionUpBottom, int lengthRest, List<QPath> qGrams, Pair pair, Set<String> allowedTokenIds) {
		
		DependencyToken currentToken = isDirectionUpBottom ? dep.getT2() : dep.getT1();
		
		if (!allowedTokenIds.contains(currentToken.getId())) {
			throw new IllegalStateException();
		}
		
		List<QPath> newQPaths = new ArrayList<QPath>();
		
			/* prolog the available qGrams */
			for (QPath qg : qGrams) {
				if (!qg.getTokenIds().contains(currentToken.getId())) {
					/* only add if the node is not there yet */
					QPath newQPath = qg.clone();
					newQPath.addDependency(
							currentToken.getId(), 
							stringIndexProvider_Inst.getTokenIndex(currentToken, pair),
							stringIndexProvider_Inst.getTokenIndex(dep.getType(), true)
					);
					newQPaths.add(newQPath);
				}
			}
			
			if (lengthRest <= 1) {
				return newQPaths;
			}
			else {
				List<QPath> result = new ArrayList<QPath>();
				/* dependents */
				if (currentToken.getDependentsCount() > 0) {
					for (Dependency d : currentToken.getDependents()) {
						if (allowedTokenIds.contains(d.getT2().getId())) {
							result.addAll(addQPaths(d, true, lengthRest -1, newQPaths, pair, allowedTokenIds));
						}
					}
				}
				/* governors */
				if (currentToken.getGovernorsCount() > 0) {
					for (Dependency d : currentToken.getGovernors()) {
						if (allowedTokenIds.contains(d.getT1().getId())) {
							result.addAll(addQPaths(d, false, lengthRest -1, newQPaths, pair, allowedTokenIds));
						}
					}
				}
				return result;
			}
			
	}
	
	protected void addQPaths(DependencyToken dt, int length, Pair pair, Set<String> allowedTokenIds, Collection<QPath> result) {
		if (length == 0) {
			throw new IllegalStateException();
		}
		
		QPath firstQPath = new QPath(qGramLengthMax, dt.getId(), stringIndexProvider_Inst.getTokenIndex(dt, pair));
		
		if (length == 1) {
			firstQPath.normalize();
			result.add(firstQPath);
		}
		else {
			List<QPath> initialList = new ArrayList<QPath>();
			initialList.add(firstQPath);
			
			/* expand */
			if (dt.getDependentsCount() > 0) {
				for (Dependency dep : dt.getDependents()) {
					if (allowedTokenIds.contains(dep.getT2().getId())) {
						List<QPath> list = addQPaths(dep, true, length - 1, initialList, pair, allowedTokenIds);
						for (QPath path : list) {
							path.normalize();
							result.add(path);
						}
					}
				}
			}
			if (dt.getGovernorsCount() > 0) {
				for (Dependency dep : dt.getGovernors()) {
					if (allowedTokenIds.contains(dep.getT1().getId())) {
						List<QPath> list = addQPaths(dep, false, length - 1, initialList, pair, allowedTokenIds);
						for (QPath path : list) {
							path.normalize();
							result.add(path);
						}
					}
				}
			}
			
		}
	}
	
	protected void addQPaths(DependencyToken dt, Pair pair, Set<String> allowedTokenIds, Collection<QPath> result) {
		List<QPath> initialList = new ArrayList<QPath>();
		initialList.add(new QPath(qGramLengthMax, dt.getId(), stringIndexProvider_Inst.getTokenIndex(dt, pair)));
		
		if (dt.getDependentsCount() > 0) {
			for (Dependency dep : dt.getDependents()) {
				if (allowedTokenIds.contains(dep.getT2().getId())) {
					List<QPath> list = addQPaths(dep, true, qGramLengthMax - 1, initialList, pair, allowedTokenIds);
					for (QPath path : list) {
						path.normalize();
						result.add(path);
					}
				}
			}
		}
		if (dt.getGovernorsCount() > 0) {
			for (Dependency dep : dt.getGovernors()) {
				if (allowedTokenIds.contains(dep.getT1().getId())) {
					List<QPath> list = addQPaths(dep, false, qGramLengthMax - 1, initialList, pair, allowedTokenIds);
					for (QPath path : list) {
						path.normalize();
						result.add(path);
					}
				}
			}
		}
	}
	
	private void addReachableTokenIds(DependencyToken token, int k, Set<String> result) {
		
		if (k > 0) {
			
			if (token.getGovernorsCount() > 0) {
				for (Dependency dep : token.getGovernors()) {
					DependencyToken dt = dep.getT1();
					result.add(dt.getId());
					addReachableTokenIds(dt, k - 1, result);
				}
			}

			if (token.getDependentsCount() > 0) {
				for (Dependency dep : token.getDependents()) {
					DependencyToken dt = dep.getT2();
					result.add(dt.getId());
					addReachableTokenIds(dt, k - 1, result);
				}
			}

		}
		
	}
	
	@SuppressWarnings("unused")
	private void addSubgramsUpTo(Collection<QPath> qGrams, int qGramLength, Set<QPath> result) {
		int minSubgramLength = 2;
		int maxSubgramLength = qGramLength -1;
		for (QPath qGram : qGrams) {
			for (int i = minSubgramLength; i <= maxSubgramLength; i++) {
				qGram.addSubgrams(i, result, true);
			}
		}
	}
	
	private Set<String> allowedTokenIds(Path shortestPath) {
		Set<String> result = new HashSet<String>();

		/* path elements themselves */
		
		result.addAll(shortestPath.getTokenIds());
		
		/* reachable tokens */
		int tokenCnt = shortestPath.getTokenCount();
		for (int i = 0; i < tokenCnt; i++) {
			addReachableTokenIds(shortestPath.getTokenAt(i), kBand, result);
		}
		
		return result;
	}

	protected DependencyToken findRootEntityOccurence(Set<String> entityTokenIds, Tokenization tokenization) {
		//Set<String> entityTokenIds = getTokenIds(entity, tokenization);
//		System.out.println("------");
//		System.out.println(entityId);
//		for (String id : entityTokenIds) {
//			Token t = tokenization.getToken(id);
//			System.out.println(" - "+ t.getId() + "/"+ t.getText());
//		}
		if (entityTokenIds == null || entityTokenIds.size() == 0) {
			throw new IllegalStateException();
		}
		else if (entityTokenIds.size() == 1) {
			Token t = tokenization.getToken(entityTokenIds.iterator().next());
			if (t instanceof DependencyToken) {
				return (DependencyToken) t;
			}
			else {
				throw new IllegalStateException();
			}
		}
		else {
			/* find the "highest" one in the hierarchy */
			Map<String, Float> scoresMap = new HashMap<String, Float>();
			for (String id1 : entityTokenIds) {
				DependencyToken dt1 = (DependencyToken) tokenization.getToken(id1);
				scoresMap.put(dt1.getId(), Float.valueOf(Float.MIN_VALUE));
				for (String id2 : entityTokenIds) {
					if (!id1.equals(id2)) {
						/* check only not self-paths */
						DependencyToken dt2 = (DependencyToken) tokenization.getToken(id2);
						
						Path shortestPath = findShortestPath(dt1, dt2, tokenization.getTokens().size() -1);
						if (shortestPath != null) {
							float score = shortestPath.governorScore();
							float oldScore = scoresMap.get(dt1.getId()).floatValue();
							if (oldScore == Float.MIN_VALUE) {
								oldScore = 0;
							}
							score += oldScore;
							scoresMap.put(dt1.getId(), Float.valueOf(score));
						}
					}
				}
			}
			
			float maxScore = Float.MIN_VALUE;
			for (Map.Entry<String, Float> en : scoresMap.entrySet()) {
				float val = en.getValue().floatValue();
				if (val > maxScore) {
					maxScore = val;
				}
			}
			/* test if something changed */
			if (maxScore == Float.MIN_VALUE) {
				/* suspect: nothing changed */
				throw new IllegalStateException();
			}
			
			
			TreeSet<String> winners = new TreeSet<String>();
			for (Map.Entry<String, Float> en : scoresMap.entrySet()) {
				if (en.getValue().floatValue() == maxScore) {
					winners.add(en.getKey());
				}
			}
			if (winners.size() == 0) {
				throw new IllegalStateException();
			}
			else if(winners.size() == 1){
				/* there is a clear winner */
				return (DependencyToken)tokenization.getToken(winners.first());
			}
			else {
				/* more winner candidates */
				return (DependencyToken)tokenization.getToken(winners.first());
			}
			
			
		}
		
	}
	protected Path findShortestPath(DependencyToken dt1, DependencyToken dt2, int maxLength) {
		/* start from dt1 and incrementally build QPathes 
		 * until the last QPath element is dt2 */
		
		if (dt1.getId().equals(dt2.getId())) {
			return new Path(dt1);
		}
		
		List<Path> initialPathes = new ArrayList<Path>();
		if (dt1.getDependentsCount() > 0) {
			for (Dependency dep : dt1.getDependents()) {
				Path newPath = new Path(dt1, dep);
				initialPathes.add(newPath);
			}
		}
		
		if (dt1.getGovernorsCount() > 0) {
			for (Dependency dep : dt1.getGovernors()) {
				Path newPath = new Path(dt1, dep);
				initialPathes.add(newPath);
			}
		}
		
		
		while (true) {
			
			if (initialPathes.size() == 0) {
				return null;
			}
			
			int tokenCnt = -1;
			for (Path path : initialPathes) {
				if (dt2.getId().equals(path.lastToken().getId())) {
					return path;
				}
				if (tokenCnt != -1) {
					/* length valid, check if it is constant 
					 * across the initialPathes elements */
					if (tokenCnt != path.getTokenCount()) {
						throw new IllegalStateException();
					}
				}
				tokenCnt = path.getTokenCount();
			}
			
			if (tokenCnt > maxLength) {
				return null;
			}
			
			List<Path> expanded = new ArrayList<Path>();
			
			for (Path path : initialPathes) {
				if (path.isExpandable()) {
					path.addExpanded(expanded);
				}
			}
			
			initialPathes = expanded;
			
		}
	}
	
	
	protected Entity getEntity(boolean isFirstEntity, Pair pair) {
		return isFirstEntity ? pair.getE1() : pair.getE2();
	}
	
	
	protected Set<String> getTokenIds(Entity entity, Tokenization tokenization) {
		Set<String> result = new HashSet<String>();
		List<Token> tokens = tokenization.getTokens();
		for (Token t : tokens) {
			if (entity.getCharOffset().overlaps(t.getCharOffset())) {
				result.add(t.getId());
			}
		}
		return result;
	}

	
	@SuppressWarnings("unused")
	private void printQPath(QPath path) {
		int[] d = path.getData();
		for (int i = 0; i < d.length; i++) {
			if (i > 0) {
				System.out.print(' ');
			}
			System.out.print(d[i] + "/"+ getToken(d[i]));
		}
		System.out.println();
	}
	
	private void removeUnreachableTokens(Set<String> entityTokenIds1, Set<String> entityTokenIds2, Tokenization tokenization) {
		Iterator<String> it = entityTokenIds1.iterator();
		while (it.hasNext()) {
			String id1 = it.next();
			DependencyToken dt1 = (DependencyToken)tokenization.getToken(id1);
			boolean isReachable = false;
			for (String id2 : entityTokenIds2) {
				if (id1.equals(id2)) {
					isReachable = true;
					break;
				}
				DependencyToken dt2 = (DependencyToken)tokenization.getToken(id2);
				if (findShortestPath(dt1, dt2, tokenization.getTokens().size() -1) != null) {
					isReachable = true;
					break;
				}
			}
			if (!isReachable) {
				it.remove();
			}
		}
		it = entityTokenIds2.iterator();
		while (it.hasNext()) {
			String id2 = it.next();
			DependencyToken dt2 = (DependencyToken)tokenization.getToken(id2);
			boolean isReachable = false;
			for (String id1 : entityTokenIds1) {
				if (id1.equals(id2)) {
					isReachable = true;
					break;
				}
				DependencyToken dt1 = (DependencyToken)tokenization.getToken(id1);
				if (findShortestPath(dt1, dt2, tokenization.getTokens().size() -1) != null) {
					isReachable = true;
					break;
				}
			}
			if (!isReachable) {
				it.remove();
			}
		}
	}

	@Override
	public void write(Pair pair, Sentence sentence, Appendable out) throws IOException {
//		System.out.println(pair.getId());
//		StringBuffer out = new StringBuffer();
//		if (pair.getId().equals("AIMed.d11.s88.p0")) {
//			System.out.println();
//		}
		
		out.append(pair.isInteraction() ? SvmLightTreeKernelConstants.POSITIVE_EXAMPLE : SvmLightTreeKernelConstants.NEGATIVE_EXAMPLE);
		out.append(SvmLightTreeKernelConstants.SPACE);
		out.append(SvmLightTreeKernelConstants.HASH);

		Parse parse = sentence.getParse(parser);
		if (parse == null)
		{
			List<String> ps = new ArrayList<String>();
			if (sentence.getParses() != null)
				for (Parse p : sentence.getParses())
					ps.add(p.getParser());
			throw new IllegalStateException("no dependency parse '" + parser +"' found [" + ps.toString() +"]");
		}
		Tokenization tokenization = parse.getTokenization();
		if (tokenization == null)
		{
			List<String> ts = new ArrayList<String>();
			if (sentence.getTokenizations() != null)
				for (Tokenization t : sentence.getTokenizations())
					ts.add(t.getTokenizer());
			throw new IllegalStateException("no tokenization '" + tokenization +"' found [" + ts.toString() +"]");
		}
		
		Set<String> entityTokenIds1 = getTokenIds(pair.getE1(), tokenization);
		Set<String> entityTokenIds2 = getTokenIds(pair.getE2(), tokenization);

		removeUnreachableTokens(entityTokenIds1, entityTokenIds2, tokenization);

		
		if (entityTokenIds1.size() > 0 && entityTokenIds2.size() > 0) {

			DependencyToken dt1 = findRootEntityOccurence(entityTokenIds1, tokenization);
			DependencyToken dt2 = findRootEntityOccurence(entityTokenIds2, tokenization);
			Path shortestPath = findShortestPath(dt1, dt2, tokenization.getTokens().size() -1);
			if (shortestPath != null) {
				write(shortestPath, pair, tokenization, out);
			}
		}
		
		out.append(SvmLightTreeKernelConstants.HASH);
		out.append(pair.getId());

		out.append(SvmLightTreeKernelConstants.EOL);
		
	}
	
	private void write(Path shortestPath, Pair pair, Tokenization tokenization, Appendable out) throws IOException {
		
		Set<String> allowedTokenIds = allowedTokenIds(shortestPath);
		
		Set<QPath> qGrams = new TreeSet<QPath>(QPath.qPathComparatorSingleton);
		
		for (String tokenId : allowedTokenIds) {
			DependencyToken dt = (DependencyToken)tokenization.getToken(tokenId);
			for (int length = qGramLengthMin; length <= qGramLengthMax; length++) {
				addQPaths(dt, length, pair, allowedTokenIds, qGrams);
			}
		}
		
		for (QPath path : qGrams) {
			//printQPath(path);
			path.write(out);
		}

		
	}
}
