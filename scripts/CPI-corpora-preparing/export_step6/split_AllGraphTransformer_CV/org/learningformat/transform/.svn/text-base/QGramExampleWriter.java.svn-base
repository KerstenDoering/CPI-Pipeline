package org.learningformat.transform;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;

import org.learningformat.api.Dependency;
import org.learningformat.api.Entity;
import org.learningformat.api.LearningFormatConstants;
import org.learningformat.api.Pair;
import org.learningformat.api.Parse;
import org.learningformat.api.DependencyToken;
import org.learningformat.api.Sentence;
import org.learningformat.api.Token;
import org.learningformat.api.Tokenization;
import org.learningformat.transform.SvmLightTreeKernelConstants.LineStyle;

public class QGramExampleWriter implements BracketingConstants, ExampleWriter {
	
	private static class StringIndexProvider_ implements StringIndexProvider {
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
		
		public int getTokenIndex(String token, boolean isDependencyType) {
			String lower = isDependencyType ? token.toUpperCase() : token.toLowerCase();
			Integer i = tokenIndex.get(lower);
			if (i == null) {
				i = Integer.valueOf(currentIndex++);
				tokenIndex.put(lower, i);
			}
			return i.intValue();
		}

		@Override
		public int getTokenIndex(Token token, Entity thisEntity,
				Entity otherEntity) {
			throw new UnsupportedOperationException();
		}
	}
	
	private static StringIndexProvider_ stringIndexProvider_Inst = new StringIndexProvider_(); 
	
	public static class RankedDependency {
		private Dependency dependency;
		private int rank = Integer.MIN_VALUE;
		private boolean rootReachable = false;
		public RankedDependency(Dependency dependency, int rank,
				boolean rootReachable) {
			super();
			this.dependency = dependency;
			this.rank = rank;
			this.rootReachable = rootReachable;
		}
		public Dependency getDependency() {
			return dependency;
		}
		public int getRank() {
			return rank;
		}
		public boolean isRootReachable() {
			return rootReachable;
		}
		public void setDependency(Dependency dependency) {
			this.dependency = dependency;
		}
		public void setRank(int rank) {
			this.rank = rank;
		}
		public void setRootReachable(boolean rootReachable) {
			this.rootReachable = rootReachable;
		}
		
	}
	public static class RankedDependencyComparator implements Comparator<RankedDependency> {

		@Override
		public int compare(RankedDependency o1, RankedDependency o2) {
			if (o1 == o2) {
				return 0;
			}
			else {
				if (o1.isRootReachable() != o2.isRootReachable()) {
					/* the one with root reachable is better */
					if (o1.isRootReachable()) {
						return -1;
					}
					else {
						return 1;
					}
				}
				else {
					/* root reachable does not help as it is the same on both 
					 * so the lower rank is better */
					if (o1.getRank() < o2.getRank()) {
						return -1;
					}
					else {
						return 1;
					}
				}
			}
		}
	}
	private static int currentIndex = 0;
	
	private static final Map<String, Integer> tokenIndex = new HashMap<String, Integer>();
	
	protected LineStyle lineStyle;
	protected String parser;
	protected int qGramLength;

	
	protected String tokenizer;

	public QGramExampleWriter(String tokenizer, String parser, LineStyle lineStyle, int qGramLength) {
		super();
		this.tokenizer = tokenizer;
		this.parser = parser;
		this.lineStyle = lineStyle;
		this.qGramLength = qGramLength;
	}
	
	protected List<QGram> addQGrams(Dependency dep, boolean isDirectionUpBottom, int lengthRest, List<QGram> qGrams, Pair pair) {
		
		DependencyToken currentToken = isDirectionUpBottom ? dep.getT2() : dep.getT1();
		
		List<QGram> newQGrams = new ArrayList<QGram>();
		
			/* prolog the available qGrams */
			for (QGram qg : qGrams) {
				if (!qg.getTokenIds().contains(currentToken.getId())) {
					/* only add if the node is not there yet */
					QGram newQGram = qg.clone();
					newQGram.addDependency(dep, pair, isDirectionUpBottom);
					newQGrams.add(newQGram);
				}
			}
			
			if (lengthRest <= 1) {
				return newQGrams;
			}
			else {
				List<QGram> result = new ArrayList<QGram>();
				/* dependents */
				if (currentToken.getDependentsCount() > 0) {
					for (Dependency d : currentToken.getDependents()) {
						result.addAll(addQGrams(d, true, lengthRest -1, newQGrams, pair));
					}
				}
				/* governors */
				if (currentToken.getGovernorsCount() > 0) {
					for (Dependency d : currentToken.getGovernors()) {
						result.addAll(addQGrams(d, false, lengthRest -1, newQGrams, pair));
					}
				}
				return result;
			}


			
	}
	
	protected RankedDependency findPreferedGovernor(DependencyToken root, DependencyToken dt, Map<String, RankedDependency> prefs, Set<String> visiting) {

		RankedDependency result = prefs.get(dt.getId());
		
		if (result != null) {
			return result;
		}
		
		visiting.add(dt.getId());
		
		/* find it */
		if (dt.getGovernorsCount() > 0) {
			List<Dependency> govs = dt.getGovernors();
			
			TreeSet<RankedDependency> orderedRanks = new TreeSet<RankedDependency>(new RankedDependencyComparator());

			for (Dependency gd : govs) {
				DependencyToken gov = gd.getT1();
				if (!visiting.contains(gov.getId())) {
					/* avoid cycles */
					RankedDependency govsRank = findPreferedGovernor(root, gov, prefs, visiting);
					
					boolean rootReachable = gov == root || (govsRank != null && govsRank.isRootReachable());
					int bestRank = Integer.MAX_VALUE;
					Integer i = StanfordDependencyTypes.DEPENDENCY_TYPE_ORDER_MAP.get(gd.getType());
					if (i != null) {
						bestRank = i.intValue();
					}
					orderedRanks.add(new RankedDependency(gd, bestRank, rootReachable));
				}
			}

			if (orderedRanks.size() > 0){
				result = orderedRanks.first();
				prefs.put(dt.getId(), result);
			}

		}
		visiting.remove(dt.getId());

		return result;
	}
	
	protected Map<String, RankedDependency> findPreferedGovernors(DependencyToken root, Tokenization tokenization) {
		Map<String, RankedDependency> prefs = new HashMap<String, RankedDependency>();
		Set<String> visited = new HashSet<String>();
		for (Token t : tokenization.getTokens()) {
			if (t instanceof DependencyToken) {
				DependencyToken dt = (DependencyToken) t;
				RankedDependency rd = prefs.get(dt.getId());
				if (rd == null) {
					/* try to find it */
					findPreferedGovernor(root, dt, prefs, visited);
				}
			}
			else {
				throw new IllegalStateException();
			}
		}
		return prefs;
	}
	protected List<QGram> listQGrams(DependencyToken dt, Pair pair) {
		List<QGram> result = new ArrayList<QGram>();
		List<QGram> initialList = new ArrayList<QGram>();
		initialList.add(new QGram(dt, pair, qGramLength, stringIndexProvider_Inst));
		
		if (dt.getDependentsCount() > 0) {
			for (Dependency dep : dt.getDependents()) {
				result.addAll(addQGrams(dep, true, qGramLength - 1, initialList, pair));
			}
		}
		if (dt.getGovernorsCount() > 0) {
			for (Dependency dep : dt.getGovernors()) {
				result.addAll(addQGrams(dep, false, qGramLength - 1, initialList, pair));
			}
		}
		return result;
	}
	protected Map<QGram, Integer> listQGrams(Tokenization tokenization, Pair pair) {
		Map<QGram, Integer> result = new HashMap<QGram, Integer>();
		
		for (Token token : tokenization.getTokens()) {
			if (token instanceof DependencyToken) {
				DependencyToken dt = (DependencyToken) token;
				List<QGram> list = listQGrams(dt, pair);
				for (QGram qg : list) {
					
					QGram key = qg;
					Integer i = result.get(key);
					
					if (i == null) {
						QGram rev = qg.revert();
						i = result.get(rev);
						if (i != null) {
							key = rev;
						}
					}
					
					if (i == null) {
						i = Integer.valueOf(0);
					}
					
					result.put(key, Integer.valueOf(i.intValue() + 1));
				}
			}
		}
		return result;
	}
	
	public void write(Pair pair, Sentence sentence, Appendable out) throws IOException {
		
		out.append(pair.isInteraction() ? SvmLightTreeKernelConstants.POSITIVE_EXAMPLE : SvmLightTreeKernelConstants.NEGATIVE_EXAMPLE);
		out.append(SvmLightTreeKernelConstants.SPACE);
		switch (lineStyle) {
		case MOSCHITTI:
			out.append(SvmLightTreeKernelConstants.BT);
			out.append(SvmLightTreeKernelConstants.SPACE);
			break;
		case CUSTOM_KERNEL:
			out.append(SvmLightTreeKernelConstants.HASH);
			break;

		default:
			throw new IllegalStateException("Unexpected lineStyle '"+ lineStyle +"'");
		}

		
		Parse parse = sentence.getParse(parser);
		
		Map<QGram, Integer> qGrams = listQGrams(parse.getTokenization(), pair);
		
		System.out.println(parse.getTokenization().getTokens().size() +"\t"+ qGrams.size());
		
		for (Map.Entry<QGram, Integer> en : qGrams.entrySet()) {
			en.getKey().write(out);
			out.append(':');
			/* we have counted each one twice */
			out.append(String.valueOf(en.getValue().intValue() / 2));
			out.append(SvmLightTreeKernelConstants.SPACE);
			
			if (en.getValue().intValue() % 2 != 0) {
				throw new IllegalStateException("Assertion failed");
			}
		}
		
		switch (lineStyle) {
		case MOSCHITTI:
			out.append(SvmLightTreeKernelConstants.SPACE);
			out.append(SvmLightTreeKernelConstants.ET);
			break;
		case CUSTOM_KERNEL:
			break;
		default:
			throw new IllegalStateException("Unexpected lineStyle '"+ lineStyle +"'");
		}
		out.append(SvmLightTreeKernelConstants.EOL);

	}
	
	protected void writeEscapedLabel(String label, Appendable writer) throws IOException {
		
		for (int i = 0; i < label.length(); i++) {
			char ch = label.charAt(i);
			switch (ch) {
			case SPACE:
			case LEFT_BRACKET:
			case RIGHT_BRACKET:
			case LEFT_SQUARE_BRACKET:
			case RIGHT_SQUARE_BRACKET:
			case TAB:
			case CR:
			case LF:
				writer.append(UNDERSCORE);
				break;
			default:
				writer.append(ch);
				break;
			}
		}
	}
//	
//	protected void writeToken(Pair pair, DependencyToken token, Sentence sentence, Appendable writer, Map<String, RankedDependency> prefs, Set<String> visited) throws IOException {
//		visited.add(token.getId());
//		
//		writeTokenLabel(pair, token, sentence, writer);
//		
//		if (token.getDependentsCount() > 0) {
//			List<Dependency> children = token.getDependents();
//			
//			boolean first = true;
//			for (Dependency child : children) {
//				String childId = child.getT2().getId();
//				RankedDependency rd = prefs.get(childId);
//				if (rd != null && rd.getDependency() == child) {
//					/* this is the preferred parent */
//					if (!visited.contains(childId)) {
//						/* we have not visited the child yet */
//						if (first) {
//							writer.append(SPACE);
//							writer.append(LEFT_BRACKET);
//							first = false;
//						}
//						else {
//							writer.append(SPACE);
//						}
//						writeToken(pair, child.getT2(), sentence, writer, prefs, visited);
//					}
//				}
//			}
//			
//			if (!first){
//				/* close only if necessary */
//				writer.append(RIGHT_BRACKET);
//			}
//		}
//		
//	}
	
//	protected void writeTokenLabel(Pair pair, DependencyToken token, Sentence sentence, Appendable writer) throws IOException {
//		
//		if (pair.getE1().getCharOffset().overlaps(token.getCharOffset())) {
//			writer.append(LearningFormatConstants.PROT1);
//		}
//		else if (pair.getE2().getCharOffset().overlaps(token.getCharOffset())) {
//			writer.append(LearningFormatConstants.PROT2);
//		}
//		else if (token.isEntity()) {
//			writer.append(LearningFormatConstants.PROT);
//		}
//		else {
//			writeEscapedLabel(token.getText(), writer);
//		}
//	}
	
}
