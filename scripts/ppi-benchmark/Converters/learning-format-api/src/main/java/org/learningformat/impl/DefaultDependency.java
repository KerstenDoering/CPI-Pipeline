package org.learningformat.impl;

import org.learningformat.api.Dependency;
import org.learningformat.api.DependencyToken;

public class DefaultDependency extends DefaultElement implements Dependency {

	protected DependencyToken t1;

	protected DependencyToken t2;

	public DependencyToken getT1() {
		return t1;
	}
	public DependencyToken getT2() {
		return t2;
	}

	public void setT1(DependencyToken t1) {
		this.t1 = t1;
	}

	public void setT2(DependencyToken t2) {
		this.t2 = t2;
	}

}
