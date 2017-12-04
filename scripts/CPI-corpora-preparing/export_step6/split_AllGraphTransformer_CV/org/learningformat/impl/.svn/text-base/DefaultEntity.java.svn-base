package org.learningformat.impl;

import org.learningformat.api.CharOffset;
import org.learningformat.api.Entity;

public class DefaultEntity extends DefaultElement implements Entity {
	protected CharOffset charOffset = CharOffset.EMPTY_CHAR_OFFSET;
	protected String text;
	/* (non-Javadoc)
	 * @see org.unifiedformat.impl.Entity#getCharOffset()
	 */
	public CharOffset getCharOffset() {
		return charOffset;
	}
	/* (non-Javadoc)
	 * @see org.unifiedformat.impl.Entity#setCharOffset(org.unifiedformat.api.CharOffset)
	 */
	public void setCharOffset(CharOffset charOffset) {
		this.charOffset = charOffset;
	}
	/* (non-Javadoc)
	 * @see org.unifiedformat.impl.Entity#getText()
	 */
	public String getText() {
		return text;
	}
	/* (non-Javadoc)
	 * @see org.unifiedformat.impl.Entity#setText(java.lang.String)
	 */
	public void setText(String text) {
		this.text = text;
	}
	
	@Override
	public String toString() {
			return super.toString() + 
			"  charOffset = '" + charOffset + "'\n" +
			"  type = '" + type + "'\n" +
			"  origId = '" + origId + "'\n" +
			"  text = '" + text + "'\n" ;
	}
}
