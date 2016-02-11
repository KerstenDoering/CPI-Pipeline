/**
 * 
 */
package org.learningformat.transform;

import java.io.IOException;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

import org.learningformat.api.Dependency;
import org.learningformat.api.Pair;
import org.learningformat.api.Token;

public class QGram implements Cloneable {
	
	private int[] data;


	/**
	 */
	private int nodeCount = 0;
	private int pattern = 0;
	private StringIndexProvider stringIndexProvider;
	
	private HashSet<String> tokenIds = new HashSet<String>();
	
	private QGram() {
	}
	/**
	 * @param firstToken
	 * @param qGramLength the number of nodes in the path
	 */
	public QGram(Token firstToken, Pair pair, int qGramLength, StringIndexProvider stringIndexProvider) {
		super();
		this.stringIndexProvider = stringIndexProvider;
		if (qGramLength > Integer.SIZE) {
			throw new IllegalArgumentException("QGrams supported only up to "+(Integer.SIZE - 1)+" qGramLength.");
		}
		this.data = new int[(qGramLength * 2) - 1];
		for (int i = 0; i < data.length; i++) {
			data[i] = QGramConstants.INVALID_INDEX;
		}
		data[0] = stringIndexProvider.getTokenIndex(firstToken, pair);
		tokenIds.add(firstToken.getId());
		nodeCount++;
	}
	public void addDependency(Dependency dep, Pair pair, boolean isDirectionUpBottom) {
		String id = isDirectionUpBottom ? dep.getT2().getId() : dep.getT1().getId();
		if (tokenIds.contains(id)) {
			throw new IllegalStateException();
		}
		tokenIds.add(id);
		
		data[(nodeCount*2) -1] = stringIndexProvider.getTokenIndex(dep.getType(), true);
		 
		if (isDirectionUpBottom) {
			data[nodeCount*2] = stringIndexProvider.getTokenIndex(dep.getT2(), pair); 
		}
		else {
			data[nodeCount*2] = stringIndexProvider.getTokenIndex(dep.getT1(), pair);
		}
		
		setDirectionAt(nodeCount-1, isDirectionUpBottom);
		
		nodeCount++;
	}
	@Override
	public QGram clone() {
		QGram result = new QGram();
		result.pattern = this.pattern;
		result.nodeCount = this.nodeCount;
		result.data = this.data.clone();
		result.tokenIds = new HashSet<String>(this.tokenIds);
		result.stringIndexProvider = this.stringIndexProvider;
		return result;
	}
	
	@Override
	public boolean equals(Object o) {
		if (o instanceof QGram) {
			QGram qGram = (QGram)o;
			return qGram.pattern == pattern 
				&& qGram.nodeCount == nodeCount
				&& Arrays.equals(qGram.data, data);
		}
		return false;
	}
	
	private int getDataLength() {
		return (nodeCount * 2) -1;
	}
	
	public int getPattern() {
		return pattern & ~(Integer.MAX_VALUE << (nodeCount - 1));
	}
	
	public Set<String> getTokenIds() {
		return tokenIds;
	}
	
	@Override
	public int hashCode() {
		int hashCode = 1;
	    hashCode = 31*hashCode + pattern;
	    hashCode = 31*hashCode + nodeCount;
	    for (int i : data) {
		    hashCode = 31*hashCode + i;
		}
		return hashCode;
	}
	
	private boolean isDirectionUpBottom(int nodeIndex) {
		return ((pattern >> nodeIndex) & QGramConstants.DIRECTION_UP_BOTTOM) == QGramConstants.DIRECTION_UP_BOTTOM;
	}
	public QGram revert() {
		
		QGram result = clone();
		
		if (result.nodeCount > 1) {
			int dataLength = result.getDataLength();
			int halfDataCount = dataLength/2;
			
			for (int i = 0; i < halfDataCount; i++) {
				result.swap(i, dataLength -1 - i);
			}
			
			int halfCount = result.nodeCount/2;
			for (int i = 0; i < halfCount; i++) {
				result.swapDirections(i, result.nodeCount -2 - i);
			}
		}
		
		return result;
	}
	
	private void setDirectionAt(int nodeIndex, boolean isDirectionUpBottom) {
		if (isDirectionUpBottom) {
			/* set the bit at nodeIndex to one */
			pattern |= (1 << nodeIndex);
		}
		else {
			/* set the bit at nodeIndex to zero */
			pattern &= ~(1 << nodeIndex);
		}
	}
	
	private void swap(int i1, int i2) {
		int tmp = data[i1];
		data[i1] = data[i2];
		data[i2] = tmp;
	}
	
	private void swapDirections(int i1, int i2) {
		boolean tmp = isDirectionUpBottom(i1);
		setDirectionAt(i1, !isDirectionUpBottom(i2));
		setDirectionAt(i2, !tmp);
	}
	
	@Override
	public String toString() {
		StringBuilder sb = new StringBuilder();
		try {
			write(sb);
		} catch (IOException e) {
		}
		return sb.toString();
	}
	
	public void write(Appendable buffer) throws IOException {
		buffer.append(BracketingConstants.LEFT_BRACKET);
		
		//buffer.append(Integer.toBinaryString(getPattern()));
		buffer.append(String.valueOf(getPattern()));
		
		for (int i = 0; i < data.length; i++) {
			buffer.append(BracketingConstants.SPACE);
			buffer.append(String.valueOf(data[i]));
		}
		
		buffer.append(BracketingConstants.RIGHT_BRACKET);
	}
	
}