package org.learningformat.transform;

import java.io.IOException;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;

import org.learningformat.api.Dependency;
import org.learningformat.api.LearningFormatConstants;
import org.learningformat.api.Pair;
import org.learningformat.api.Parse;
import org.learningformat.api.DependencyToken;
import org.learningformat.api.Sentence;
import org.learningformat.api.Token;
import org.learningformat.api.Tokenization;
import org.learningformat.transform.SvmLightTreeKernelConstants.LineStyle;

public class DependencyToBracketingExampleWriter implements BracketingConstants, ExampleWriter {
	
	
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
	protected LineStyle lineStyle;
	protected String parser;

	
	protected String tokenizer;

	public DependencyToBracketingExampleWriter(String tokenizer, String parser, LineStyle lineStyle) {
		super();
		this.tokenizer = tokenizer;
		this.parser = parser;
		this.lineStyle = lineStyle;
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
		
		out.append(LEFT_BRACKET);
		
		//System.out.println("sent = "+ sentence.getText());
		
		out.append(sentence.getId());
		out.append(" ");
		
		if (parse.getRootToken() == null) {
			throw new IllegalStateException();
		}
		Map<String, RankedDependency> prefs = findPreferedGovernors(parse.getRootToken(), parse.getTokenization());
		
		writeToken(pair, parse.getRootToken(), sentence, out, prefs, new HashSet<String>());

		out.append(RIGHT_BRACKET);
		
		
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
	
	protected void writeToken(Pair pair, DependencyToken token, Sentence sentence, Appendable writer, Map<String, RankedDependency> prefs, Set<String> visited) throws IOException {
		visited.add(token.getId());
		
		writeTokenLabel(pair, token, sentence, writer);
		
		if (token.getDependentsCount() > 0) {
			List<Dependency> children = token.getDependents();
			
			boolean first = true;
			for (Dependency child : children) {
				String childId = child.getT2().getId();
				RankedDependency rd = prefs.get(childId);
				if (rd != null && rd.getDependency() == child) {
					/* this is the preferred parent */
					if (!visited.contains(childId)) {
						/* we have not visited the child yet */
						if (first) {
							writer.append(SPACE);
							writer.append(LEFT_BRACKET);
							first = false;
						}
						else {
							writer.append(SPACE);
						}
						writeToken(pair, child.getT2(), sentence, writer, prefs, visited);
					}
				}
			}
			
			if (!first){
				/* close only if necessary */
				writer.append(RIGHT_BRACKET);
			}
		}
		
	}
	
	protected void writeTokenLabel(Pair pair, DependencyToken token, Sentence sentence, Appendable writer) throws IOException {
		
		if (pair.getE1().getCharOffset().overlaps(token.getCharOffset())) {
			writer.append(LearningFormatConstants.PROT1);
		}
		else if (pair.getE2().getCharOffset().overlaps(token.getCharOffset())) {
			writer.append(LearningFormatConstants.PROT2);
		}
		else if (token.isEntity()) {
			writer.append(LearningFormatConstants.PROT);
		}
		else {
			writeEscapedLabel(token.getText(), writer);
		}
	}
	
}
