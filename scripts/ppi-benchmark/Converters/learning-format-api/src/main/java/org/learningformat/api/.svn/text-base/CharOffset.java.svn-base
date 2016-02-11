package org.learningformat.api;

import java.util.ArrayList;

public class CharOffset {

	public static class CharOffsetParser {
		private ArrayList<SingleCharOffset> charOffsets = new ArrayList<SingleCharOffset>(4);
		private char currentChar = 0;
		private int currentIndex = 0;
		private String rawCharOffset;

		public CharOffsetParser(String rawCharOffset) {
			super();
			this.rawCharOffset = rawCharOffset;

			charOffsets.add(consumeSingleCharOffset());

			while (isCurrentIndexValid()
					&& rawCharOffset.charAt(currentIndex) == ',') {
				consumeComma();
				charOffsets.add(consumeSingleCharOffset());
			}

		}

		private void consumeComma() {
			currentChar = rawCharOffset.charAt(currentIndex);
			if (currentChar == COMMA) {
				currentIndex++;
			} else {
				throw new CharOffsetParserException("Unexpected character '"
						+ currentChar + "' at offset " + currentIndex
						+ "; ',' expected.");
			}
		}

		private void consumeMinus() {
			currentChar = rawCharOffset.charAt(currentIndex);
			if (currentChar == MINUS) {
				currentIndex++;
			} else {
				throw new CharOffsetParserException("Unexpected character '"
						+ currentChar + "' at offset " + currentIndex
						+ "; '-' expected.");
			}
		}

		private int consumeNumber() {
			int oldIndex = currentIndex;
			if (!isCurrentIndexValid()) {
				throw new CharOffsetParserException(
						"Unexpected end of input at offset " + currentIndex
								+ "; digit expected.");
			}
			currentChar = rawCharOffset.charAt(currentIndex);
			if (currentChar >= 48 && currentChar <= 57) {
				currentIndex++;
			} else {
				throw new CharOffsetParserException("Unexpected character '"
						+ currentChar + "' at offset " + currentIndex
						+ "; digit expected.");
			}
			while (isCurrentIndexValid()) {
				currentChar = rawCharOffset.charAt(currentIndex);
				if (currentChar >= 48 && currentChar <= 57) {
					currentIndex++;
				} else {
					break;
				}
			}
			return Integer.parseInt(rawCharOffset.substring(oldIndex,
					currentIndex));
		}

		private SingleCharOffset consumeSingleCharOffset() {
			int start = consumeNumber();
			consumeMinus();

			/* we add 1 to the end to follow the java end offset practice */
			int end = (int) (consumeNumber() + 1);
			return new SingleCharOffset(start, end);
		}

		public SingleCharOffset[] getCharOffsets() {
			return charOffsets
					.toArray(new SingleCharOffset[charOffsets.size()]);
		}

		private boolean isCurrentIndexValid() {
			return currentIndex < rawCharOffset.length() && currentIndex >= 0;
		}

	}

	public static class CharOffsetParserException extends RuntimeException {

		/**
		 * 
		 */
		private static final long serialVersionUID = 5634475675684553999L;

		public CharOffsetParserException() {
			super();
		}

		public CharOffsetParserException(String message) {
			super(message);
		}

		public CharOffsetParserException(String message, Throwable cause) {
			super(message, cause);
		}

		public CharOffsetParserException(Throwable cause) {
			super(cause);
		}

	}

	public static class SingleCharOffset implements Comparable<SingleCharOffset> {
		protected int end = INVALID_OFFSET;
		protected int start = INVALID_OFFSET;

		public SingleCharOffset(int start, int end) {
			super();
			setStartEnd(start, end);
		}

		@Override
		public boolean equals(Object o) {
			if (o instanceof SingleCharOffset) {
				SingleCharOffset so = (SingleCharOffset) o;
				return so.start == start && so.end == end;
			}
			return false;
		}

		public int getEnd() {
			return end;
		}

		public int getStart() {
			return start;
		}
		
		public void setStartEnd(int start, int end) {
		    	if (start > end || start < 0)
		    	    throw new IllegalArgumentException("Illegal begin-end: '" + start +'-' + end+"'");
		    	
			this.start = start;
			this.end = end;
		}


		@Override
		public int hashCode() {
			return (start << Short.SIZE) | end;
		}

		public boolean overlaps(SingleCharOffset anotherOffset) {
			return anotherOffset.end > start && anotherOffset.start < end;
		}
	    /**
	     * Sort by {@link #getBegin()} ascending and by {@link #getEnd()} descending.
	     */
	    @Override
	    public int compareTo(SingleCharOffset o) {
			int d;
			d = getStart() - o.getStart(); 	if ( d != 0 ) return d;
			d = o.getEnd() - getEnd(); 		if ( d != 0 ) return d;
			// we can't do more comparisons
			return 0;
	    }
	    
	    public boolean contains(SingleCharOffset o)
	    {
	    	return getStart() <= o.getStart()  && getEnd() >= o.getEnd();
	    }
	    
	    

		@Override
		public String toString() {
			return append(new StringBuilder(11)).toString();
		}

		public StringBuilder append(StringBuilder sb) {
			/* -1 because here we turn back to the learning format convention */
			return sb.append(start).append(MINUS).append(end -1);
		}
		
		public String substringOf(TextProvider textProvider)
		{
			if (textProvider == null)
				throw new NullPointerException();
			return substringOf(textProvider.getText());
		}
		
		private String substringOf(String text) {
			if (text == null)
				throw new NullPointerException();
			return text.substring(getStart(), getEnd());
		}		

	}

	public static final char COMMA = ',';
	public static final CharOffset EMPTY_CHAR_OFFSET = new CharOffset(
			(String) null);
	public static final int INVALID_OFFSET = -1;
	public static final char MINUS = '-';

	public static CharOffset parse(String charOffset) {
		return charOffset == null || charOffset.length() == 0 ? EMPTY_CHAR_OFFSET
				: new CharOffset(charOffset);
	}
	public static SingleCharOffset parseSingle(String charOffset) {
		if (charOffset == null || charOffset.length() == 0) {
			return null;
		}
		CharOffset co = new CharOffset(charOffset);
		if (co.getCharOffsets().length == 1) {
			return co.getCharOffsets()[0];
		}
		throw new IllegalStateException("Single charOffset expected in '"+ charOffset +"'.");
	}

	protected SingleCharOffset[] charOffsets;

	/**
	 * Convenience method.
	 * @see SingleCharOffset#SingleCharOffset(int, int)
	 */
	public CharOffset(int start, int end) {
		this(new SingleCharOffset(start, end));
	}
	
	/**
	 * Convenience method.
	 */
	public CharOffset(SingleCharOffset charOffset) {
		this(new SingleCharOffset[] {charOffset});
	}

	public CharOffset(SingleCharOffset[] charOffsets) {
		this.charOffsets = charOffsets;
	}

	public CharOffset(String charOffset) {
		super();
		if (charOffset == null || charOffset.length() == 0) {
			charOffsets = new SingleCharOffset[0];
		} else {
			charOffsets = parseRaw(charOffset);
		}
	}

	public SingleCharOffset[] getCharOffsets() {
		return charOffsets;
	}

	protected SingleCharOffset[] parseRaw(String rawCharOffset) {
		return new CharOffsetParser(rawCharOffset).getCharOffsets();
	}

	@Override
	public String toString() {
		if (charOffsets == null || charOffsets.length == 0) {
			return "";
		} else {
			StringBuilder sb = new StringBuilder();
			for (int i = 0; i < charOffsets.length; i++) {
				if (i > 0) {
					sb.append(COMMA);
				}
				sb.append(charOffsets[i].toString());
			}
			return sb.toString();
		}
	}
	
	public boolean overlaps(CharOffset anotherOffset) {
		if (charOffsets != null && charOffsets.length > 0) {
			SingleCharOffset[] anotherOffsets = anotherOffset.getCharOffsets();
			if (anotherOffsets != null && anotherOffsets.length > 0) {
				for (SingleCharOffset thisOffsetElement : charOffsets) {
					for (SingleCharOffset thatOffsetElement : anotherOffsets) {
						if (thisOffsetElement.overlaps(thatOffsetElement)) {
							return true;
						}
					}
				}
			}
		}
		return false;
	}

	private int hashCode = 0;
	
	@Override
	public int hashCode() {
		if (hashCode == 0) {
			int h = 0;
			if (charOffsets != null && charOffsets.length > 0) {
				for (SingleCharOffset thisOffsetElement : charOffsets) {
	                h = 31*h + thisOffsetElement.hashCode();
				}
			}
		}
		return hashCode;
	}

	@Override
	public boolean equals(Object o) {
		if (this == o) {
			return true;
		}
		if (o instanceof CharOffset) {
			SingleCharOffset[] anotherOffsets = ((CharOffset)o).getCharOffsets();
			
			if (anotherOffsets == this.charOffsets) {
				return true;
			}
			int l1 = this.charOffsets.length;
			int l2 = anotherOffsets.length;
			if (l1 == 0 && l2 == 0) {
				return true;
			}
			else if (l1 != l2) {
				return false;
			}
			else {
				/* l1 != 0 && l2 != 0 && l1 == l2 */
				for (int i = 0; i < anotherOffsets.length; i++) {
					if (!charOffsets[i].equals(anotherOffsets[i])) {
						return false;
					}
				}
				/* all of them are equal */
				return true;
			}
		}
		return false;
	}
	
	
}
