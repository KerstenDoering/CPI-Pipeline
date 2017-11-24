package org.learningformat.api;

import java.util.Set;


public interface Token extends Element, CharOffsetProvider, TextProvider {

	/**
	 * @return POS tag of this token.
	 */
	public String getPos();
	
	/**
	 * @param pos POS tag of this token.
	 */
	public void setPos(String pos);
	
	public boolean isEntity();

	public void setEntity(Entity entity);
	public Set<Entity> getEntity();
	
}
