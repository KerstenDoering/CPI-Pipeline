package org.learningformat.impl;

import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

import org.learningformat.api.CharOffset;
import org.learningformat.api.Entity;
import org.learningformat.api.Token;

public class DefaultToken extends DefaultElement implements Token {

	protected CharOffset charOffset;
	protected boolean entity = false;
	Set<Entity> entities  = new HashSet<Entity>();
	
	protected String pos;

	protected String text;
	@Override
	public CharOffset getCharOffset() {
		return charOffset;
	}

	@Override
	public String getPos() {
		return pos;
	}

	@Override
	public String getText() {
		return text;
	}

	@Override
	public boolean isEntity() {
		return entity;
	}

	@Override
	public void setCharOffset(CharOffset charOffset) {
		this.charOffset = charOffset;
	}

//	@Override
//	public void setEntity(boolean entity) {
//		this.entity = entity;
//	}
	@Override
	public void setEntity(Entity entities) {
		this.entities.add(entities);
		this.entity=true;		
	}
	@Override
	public Set<Entity> getEntity() {		
		return entities;
	}

	@Override
	public void setPos(String pos) {
		this.pos = pos;
	}

	@Override
	public void setText(String text) {
		this.text = text;
	}
	
	@Override
	public String toString() {
	    return "'" + getText() +"'/" + getPos() +Arrays.toString(getCharOffset().getCharOffsets()); 
	}



}
