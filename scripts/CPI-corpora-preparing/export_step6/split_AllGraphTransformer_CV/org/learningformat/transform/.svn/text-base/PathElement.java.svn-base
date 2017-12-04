/**
 * 
 */
package org.learningformat.transform;

import org.learningformat.api.Dependency;
import org.learningformat.api.DependencyToken;

public class PathElement {
	private Dependency dependency;

	private int direction;
	public PathElement(Dependency dependency, int direction) {
		super();
		this.dependency = dependency;
		this.direction = direction;
	}
	public Dependency getDependency() {
		return dependency;
	}
	public int getDirection() {
		return direction;
	}
	public DependencyToken getT1() {
		return isDirectionUpBottom() ? dependency.getT1() : dependency.getT2();
	}
	public DependencyToken getT2() {
		return !isDirectionUpBottom() ? dependency.getT1() : dependency.getT2();
	}
	public boolean isDirectionUpBottom() {
		return direction == PathBandExampleWriter.DIRECTION_UP_BOTTOM;
	}
	public void setDependency(Dependency dependency) {
		this.dependency = dependency;
	}
	
	public void setDirection(int direction) {
		this.direction = direction;
	}
	
	@Override
	public String toString() {
		return toString(true);
	}
	public String toString(boolean appendFirst) {
		StringBuilder sb = new StringBuilder();
		
		DependencyToken dt = null;
		if (appendFirst) {
			dt = getT1();
			sb.append(dt.getText());
			sb.append('/');
			sb.append(dt.getId());
		}
		
		sb.append(' ');
		sb.append(isDirectionUpBottom() ? "-" : "<-");
		
		sb.append(dependency.getType());

		sb.append(isDirectionUpBottom() ? "->" : "-");
		sb.append(' ');
		
		dt = getT2();
		sb.append(dt.getText());
		sb.append('/');
		sb.append(dt.getId());

		return sb.toString();
	}
	
}