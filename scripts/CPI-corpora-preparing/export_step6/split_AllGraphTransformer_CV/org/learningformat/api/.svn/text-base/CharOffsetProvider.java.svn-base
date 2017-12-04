package org.learningformat.api;

public interface CharOffsetProvider {
	/**
	 * @return the character offsets in the original text. Should never be null;
	 *         if no char offset information is available, rather the
	 *         <code>{@link CharOffset#EMPTY_CHAR_OFFSET}</code> should be
	 *         returned.
	 */
	public CharOffset getCharOffset();

	/**
	 * @param charOffset
	 *            the character offsets in the original text. Should never be
	 *            null; if no char offset information is available, rather the
	 *            <code>{@link CharOffset#EMPTY_CHAR_OFFSET}</code> should be
	 *            used. If the char offset information needs to be parsed from a
	 *            string, the utility method {@link CharOffset#parse(String)}
	 *            method should be used.
	 */
	public void setCharOffset(CharOffset charOffset);

}
