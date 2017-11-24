package org.learningformat.api;

import java.util.List;


public interface DependencyToken extends Token {

	public int getGovernorsCount();
	public List<Dependency> getGovernors();
	
	public void addGovernor(Dependency governor);

	public void removeGovernor(Dependency governor);
	
	public int getDependentsCount();
	public List<Dependency> getDependents();
	
	public void addDependent(Dependency child);

	public void removeDependent(Dependency child);

}
