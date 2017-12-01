package org.learningformat.impl;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.Vector;

import org.learningformat.api.CharOffset;
import org.learningformat.api.Dependency;
import org.learningformat.api.DependencyToken;
import org.learningformat.api.Parse;
import org.learningformat.api.Token;
import org.learningformat.api.Tokenization;

public class DefaultParse implements Parse {

	private static final String _ROOT_ = "_ROOT_";
	protected List<Dependency> dependencies;
	protected String parser;

	protected DependencyToken rootToken;
	
	protected Tokenization tokenization;

//	protected void ensureNoCycles(ParseToken parseToken, Set<String> visitedTokens) {
//		System.out.println(" ensureNoCycles for parseToken.getId() = "+ parseToken.getId());
//		if (visitedTokens.contains(parseToken.getId())) {
//			throw new IllegalStateException("Cycle found at token "+ parseToken.getId());
//		}
//		visitedTokens.add(parseToken.getId());
//		List<Dependency> deps = parseToken.getChildren();
//		if (deps != null) {
//			for (Dependency dep : deps) {
//				ensureNoCycles(dep.getT2(), visitedTokens);
//			}
//		}
//		
//	}

//	@Override
//	public void ensureNoCycles() {
//		ParseToken root = getRootToken();
//		if (root == null) {
//			throw new IllegalStateException("root not set yet.");
//		}
//		Set<String> visitedTokens = new HashSet<String>();
//		ensureNoCycles(root, visitedTokens);
//	}

	@Override
	public void addDependency(Dependency dependency) {
		if (dependencies == null)
			dependencies = new ArrayList<Dependency>(16);
		dependencies.add(dependency);
	}
	protected int countReachableTokens(DependencyToken token) {
		return countReachableTokens(token, new HashSet<String>());
	}
	protected int countReachableTokens(DependencyToken token, Set<String> visited) {
		/* 1 for this particular one */
		int result = 1;
		
		visited.add(token.getId());
		
		if (token.getDependentsCount() > 0) {
			for (Dependency dep : token.getDependents()) {
				DependencyToken child = dep.getT2();
				if (!visited.contains(child.getId())) {
					result += countReachableTokens(child, visited);
				}
			}
		}
		return result;
	}
	
	protected List<DependencyToken> findRootCandidates() {
		Collection<Token> tokens = getTokenization().getTokens();
		if (tokens.size() == 0)
			return Collections.emptyList();
		
		Vector<DependencyToken> result = new Vector<DependencyToken>();
		int max = 0;
		for (Token t : tokens) {
			if (t instanceof DependencyToken) {
				DependencyToken dt = (DependencyToken) t;
				int cnt = countReachableTokens(dt);
				if (cnt > max) {
					result.removeAllElements();
					max = cnt;
					result.add(dt);
				}
				else if (cnt == max) {
					result.add(dt);
				}
			}
			else {
				throw new IllegalStateException();
			}
		}
		return result;
	}
	
	protected DependencyToken findRootToken() {
		List<DependencyToken> roots = new ArrayList<DependencyToken>(4); 
		
		for (Token token : tokenization.getTokens()) {
			
			if (!(token instanceof DependencyToken)) {
				throw new IllegalStateException("Token not an instance of DependencyToken.");
			}
			
			//System.out.println(token.getText());
			
			DependencyToken dt = (DependencyToken) token;
			if (dt.getGovernorsCount() == 0 && dt.getDependentsCount() > 0) {
				/* root =def empty parent and at least one child
				 * check if it is the only one root 
				 * one child is important as there are tokens 
				 * which do not hang anywhere, i.e are not a part of the 'main' graph. */
				
				roots.add(dt);
//				
//				if (result != null) {
//					System.out.println("old root = "+ result.getText() +" id = "+ result.getId());
//					for (Dependency dep : result.getDependents()) {
//						System.out.println(" - dependent: "+ dep.getId() +" "+ dep.getType() + " "+ dep.getT2().getId() +" "+dep.getT2().getId());
//					}
//					System.out.println("new root = "+ dt.getText() +" id = "+ dt.getId());
//					for (Dependency dep : dt.getDependents()) {
//						System.out.println(" - dependent: "+ dep.getId() +" "+ dep.getType() + " "+ dep.getT2().getId() +" "+dep.getT2().getId());
//					}
//					throw new IllegalStateException("Multiple roots");
//				}
//				else {
//					result = dt;
//				}
			}
		}
		
		if (roots.size() == 0) {
			roots = findRootCandidates();
		}
		
		if (roots.size() == 1) {
			return roots.get(0);
		}
		else {
			/* return a special token which is a parent of all found roots */
			DependencyToken result = new DefaultDependencyToken();
			result.setCharOffset(CharOffset.EMPTY_CHAR_OFFSET);
			result.setId(roots.get(0).getId() + ".root");
			result.setPos(_ROOT_);
			result.setText(_ROOT_);
			
			int i = 0;
			for (DependencyToken dt : roots) {
				DefaultDependency dep = new DefaultDependency();
				dep.setId(result.getId() + "."+ i);
				dep.setT1(result);
				dep.setT2(dt);
				dep.setType(_ROOT_);
				
				result.addDependent(dep);
				dt.addGovernor(dep);
				
				i++;
			}
			
			return result;
		}
	}

	public List<Dependency> getDependencies() {
		if (dependencies == null)
			return Collections.emptyList();
		return dependencies;
	}

	public String getParser() {
		return parser;
	}

	public DependencyToken getRootToken() {
		if (rootToken == null) {
			rootToken = findRootToken();
		}
		return rootToken;
	}

	public Tokenization getTokenization() {
		return tokenization;
	}

	@Override
	public void removeDependency(Dependency dependency) {
		if (dependencies != null) {
			dependencies.remove(dependency);
		}
		
	}

	public void setParser(String parser) {
		this.parser = parser;
	}

	public void setRootToken(DependencyToken rootToken) {
		this.rootToken = rootToken;
	}

	public void setTokenization(Tokenization tokenization) {
		this.tokenization = tokenization;
	}
}
