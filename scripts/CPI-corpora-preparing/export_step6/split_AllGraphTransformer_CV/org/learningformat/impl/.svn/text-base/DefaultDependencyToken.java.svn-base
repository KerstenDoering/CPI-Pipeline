package org.learningformat.impl;

import java.util.ArrayList;
import java.util.List;

import org.learningformat.api.Dependency;
import org.learningformat.api.DependencyToken;

public class DefaultDependencyToken extends DefaultToken implements DependencyToken {

	protected List<Dependency> dependents;
	protected List<Dependency> governors;
	
	@Override
	public void addGovernor(Dependency governor) {
		if (governors == null) {
			governors = new ArrayList<Dependency>(4);
		}
		governors.add(governor);
	}
	@Override
	public void addDependent(Dependency child) {
		if (dependents == null) {
			dependents = new ArrayList<Dependency>(4);
		}
		dependents.add(child);
	}

	@Override
	public List<Dependency> getDependents() {
		return dependents;
	}

	@Override
	public List<Dependency> getGovernors() {
		return governors;
	}

	@Override
	public void removeDependent(Dependency child) {
		if (dependents != null) {
			dependents.remove(child);
		}
	}
	@Override
	public void removeGovernor(Dependency governor) {
		if (governors != null) {
			governors.remove(governor);
		}
	}
	@Override
	public int getDependentsCount() {
		return dependents == null ? 0 : dependents.size();
	}
	@Override
	public int getGovernorsCount() {
		return governors == null ? 0 : governors.size();
	}


}
