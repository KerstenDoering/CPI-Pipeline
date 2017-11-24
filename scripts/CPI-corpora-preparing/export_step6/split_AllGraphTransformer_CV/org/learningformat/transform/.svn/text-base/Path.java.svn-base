/**
 * 
 */
package org.learningformat.transform;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashSet;
import java.util.Set;

import org.learningformat.api.Dependency;
import org.learningformat.api.DependencyToken;

public class Path implements Cloneable {
	
	private ArrayList<PathElement> edges = new ArrayList<PathElement>();

	private HashSet<String> tokenIds = new HashSet<String>();
	private Path() {
		super();
	}
	
	private DependencyToken firstToken;

	public Path(DependencyToken firstToken) {
		this.firstToken = firstToken;
		tokenIds.add(firstToken.getId());
	}
	public Path(DependencyToken t1, Dependency dependency) {
		addElement(t1, dependency);
	}
	
	public void addElement(DependencyToken t1, Dependency dependency) {
		
		if (firstToken != null) {
			if (!firstToken.getId().equals(t1.getId())) {
				throw new IllegalStateException();
			}
			firstToken = null;
		}
		
		int direction = PathBandExampleWriter.INVALID_DIRECTION;
		if (t1.getId().equals(dependency.getT1().getId())) {
			direction = PathBandExampleWriter.DIRECTION_UP_BOTTOM;
		}
		else if (t1.getId().equals(dependency.getT2().getId())) {
			direction = PathBandExampleWriter.DIRECTION_BOTTOM_UP;
		}
		else {
			throw new IllegalStateException();
		}
		
		PathElement pe = new PathElement(dependency, direction);
		if (tokenIds.contains(pe.getT2().getId())) {
			throw new IllegalStateException();
		}
		if (edges.size() > 0) {
			if (!lastToken().getId().equals(t1.getId())) {
				throw new IllegalStateException();
			}
		}
		else {
			tokenIds.add(pe.getT1().getId());
		}
		tokenIds.add(pe.getT2().getId());
		
		edges.add(pe);
	}

	public void addExpanded(Collection<Path> result) {
		if (!isExpandable()) {
			throw new IllegalStateException();
		}
		
		DependencyToken lastToken = lastToken();
		
		if (lastToken.getDependentsCount() > 0) {
			for (Dependency dep : lastToken.getDependents()) {
				if (!tokenIds.contains(dep.getT2().getId())) {
					Path newPath = this.clone();
					newPath.addElement(dep.getT1(), dep);
					result.add(newPath);
				}
			}
		}
		
		if (lastToken.getGovernorsCount() > 0) {
			for (Dependency dep : lastToken.getGovernors()) {
				if (!tokenIds.contains(dep.getT1().getId())) {
					Path newPath = this.clone();
					newPath.addElement(dep.getT2(), dep);
					result.add(newPath);
				}
			}
		}
		
		
	}
	
	@SuppressWarnings("unchecked")
	@Override
	public Path clone() {
		Path result = new Path();
		
		result.firstToken = this.firstToken;
		result.edges = (ArrayList<PathElement>) this.edges.clone();
		result.tokenIds = (HashSet<String>) this.tokenIds.clone();
		
		return result;
	}
	
	public DependencyToken firstToken() {
		if (edges.size() == 0) {
			return firstToken;
		}
		else {
			return edges.get(0).getT1();
		}
	}
	
	public int getTokenCount() {
		return edges.size() + 1;
	}
	
	public DependencyToken getTokenAt(int i) {
		if (edges.size() == 0) {
			if (i != 0) {
				throw new IndexOutOfBoundsException();
			}
			return firstToken;
		}
		else {
			if (i == 0) {
				return edges.get(0).getT1();
			}
			else {
				return edges.get(i-1).getT2();
			}
		}
	}
	
	public Set<String> getTokenIds() {
		return tokenIds;
	}

	public float governorScore() {
		if (edges.size() == 0) {
			return 0.0f;
		}
		int result = 0;
		for (PathElement e : edges) {
			if (e.isDirectionUpBottom()) {
				result++;
			}
		}
		return ((float)result)/((float)edges.size());
	}
	
	public boolean isExpandable() {
		DependencyToken lastToken = lastToken();
		
		if (lastToken.getDependentsCount() > 0) {
			for (Dependency dep : lastToken.getDependents()) {
				if (!tokenIds.contains(dep.getT2().getId())) {
					return true;
				}
			}
		}
		
		if (lastToken.getGovernorsCount() > 0) {
			for (Dependency dep : lastToken.getGovernors()) {
				if (!tokenIds.contains(dep.getT1().getId())) {
					return true;
				}
			}
		}
		return false;
	}
	
	public DependencyToken lastToken() {
		if (edges.size() == 0) {
			return firstToken;
		}
		else {
			return edges.get(edges.size() -1).getT2();
		}
	}
	
	@Override
	public String toString() {
		StringBuilder sb = new StringBuilder();
		if (edges.size() == 0) {
			sb.append(firstToken.getText());
			sb.append('/');
			sb.append(firstToken.getId());
		}
		else {
			int i = 0;
			PathElement pe = edges.get(i);
			sb.append(pe.toString());
			
			for (i = 1; i < edges.size(); i++) {
				pe = edges.get(i);
				sb.append(pe.toString(false));
			}
		}
		return sb.toString();
	}
}