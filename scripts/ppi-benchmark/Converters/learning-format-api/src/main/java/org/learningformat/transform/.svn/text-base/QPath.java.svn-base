/**
 * 
 */
package org.learningformat.transform;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Comparator;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import org.learningformat.api.LearningFormatConstants;

public class QPath implements Cloneable {
	
	public static final QPathComparator qPathComparatorSingleton = new QPathComparator();
	public static class QPathComparator implements Comparator<QPath> {

		@Override
		public int compare(QPath p1, QPath p2) {
			if (p1.getNodeCount() < p2.getNodeCount()) {
				return -1;
			}
			else if (p1.getNodeCount() > p2.getNodeCount()) {
				return 1;
			}
			else {
				/* p1.getNodeCount() == p2.getNodeCount() */
				int[] a1 = p1.getData();
				int[] a2 = p2.getData();
				for (int i = 0; i < a1.length; i++) {
					if (a1[i] < a2[i]) {
						return -1;
					}
					else if (a1[i] > a2[i]) {
						return 1;
					}
					else {
						/* a1[i] == a2[i] do nothing */
					}
				}
				return 0;
			}
		}
	}
	
	private int[] data;
	/**
	 */
	private int nodeCount = 0;
	
	private HashSet<String> tokenIds = new HashSet<String>();
	private QPath() {
	}
	
	/**
	 * @param firstToken
	 * @param qGramLength the number of nodes in the path
	 */
	public QPath(int qGramLength) {
		super();

		if (qGramLength > Integer.SIZE) {
			throw new IllegalArgumentException("QGrams supported only up to "+(Integer.SIZE - 1)+" qGramLength.");
		}
		this.data = new int[(qGramLength * 2) - 1];
		for (int i = 0; i < data.length; i++) {
			data[i] = QGramConstants.INVALID_INDEX;
		}
	}
	public QPath(int qGramLength, String firstTokenId, int firstTokenIndex) {
		this(qGramLength);
		data[0] = firstTokenIndex;
		tokenIds.add(firstTokenId);
		nodeCount++;
	}
	public void addDependency(String tokenId, int tokenIndex, int dependencyTypeIndex) {
		if (tokenIds.contains(tokenId)) {
			throw new IllegalStateException();
		}
		tokenIds.add(tokenId);
		
		data[(nodeCount*2) -1] = dependencyTypeIndex;
		 
		data[nodeCount*2] = tokenIndex; 
		
		nodeCount++;
	}
	
	public void addSubgrams(int subgramLength, Collection<QPath> result) {
		addSubgrams(subgramLength, result, false);
	}
	
	public void addSubgrams(int subgramLength, Collection<QPath> result, boolean normalize) {
		if (subgramLength >=  nodeCount) {
			throw new IllegalStateException();
		}
		for (int start = 0; start <= getNodeCount() - subgramLength; start++) {
			QPath subgram = subgram(start, subgramLength);
			if (normalize) {
				subgram.normalize();
			}
			result.add(subgram);
		}
	}

	@SuppressWarnings("unchecked")
	@Override
	public QPath clone() {
		QPath result = new QPath();
		result.nodeCount = this.nodeCount;
		result.data = this.data.clone();
		result.tokenIds = (HashSet<String>)this.tokenIds.clone();
		return result;
	}
	@Override
	public boolean equals(Object o) {
		if (o instanceof QPath) {
			QPath qGram = (QPath)o;
			return qGram.nodeCount == nodeCount
				&& Arrays.equals(qGram.data, data);
		}
		return false;
	}
	
	int[] getData() {
		return data;
	}
	
	private int getDataLength() {
		return (nodeCount * 2) -1;
	}
	
	public int getNodeCount() {
		return nodeCount;
	}
	
	public Set<String> getTokenIds() {
		return tokenIds;
	}
	
	@Override
	public int hashCode() {
		int hashCode = 1;
	    hashCode = 31*hashCode + nodeCount;
	    for (int i : data) {
		    hashCode = 31*hashCode + i;
		}
		return hashCode;
	}
	
	
	public boolean normalizationNeeded() {
		if (this.nodeCount > 1) {
			int dataLength = getDataLength();
			int halfDataCount = dataLength/2;
			
			
			
			for (int i = 0; i < halfDataCount; i++) {
				int lower = data[i];
				int higher = data[dataLength -1 - i];
				if (lower > higher) {
					return true;
				}
				else if (data[i] < data[dataLength -1 - i]) {
					return false;
				}
			}
			return false;
		}
		else {
			return false;
		}
	}
	
	private void normalizeEntities(List<Integer>[] occurences) {
		boolean e1 = occurences[LearningFormatConstants.PROT1_INDEX].size() > 0;
		boolean e2 = occurences[LearningFormatConstants.PROT2_INDEX].size() > 0;
		
		if (e1 && !e2) {
			/* nothing to do */
		}
		else if (!e1 && e2) {
			/* nothing to do */
		}
		else if (e1 && e2) {
			/* find the first occurrence and if it is not PROT1_INDEX, replace all occurrences */
			
			int i1 = occurences[LearningFormatConstants.PROT1_INDEX].get(0);
			int i2 = occurences[LearningFormatConstants.PROT2_INDEX].get(0);
			
			if (i1 > i2) {
				/* replace the indices */
				for (Integer i : occurences[LearningFormatConstants.PROT1_INDEX]) {
					data[i.intValue()] = LearningFormatConstants.PROT2_INDEX;
				}
			}

		}
		else if (!e1 && !e2) {
			/* nothing to do */
		}
		else {
			throw new IllegalStateException();
		}

	}
	@SuppressWarnings("unchecked")
	private List<Integer>[] prenormalizeEntities() {
		List<Integer>[] result = new ArrayList[2];
		result[LearningFormatConstants.PROT1_INDEX] = new ArrayList<Integer>();
		result[LearningFormatConstants.PROT2_INDEX] = new ArrayList<Integer>();
		
		int dataLength = getDataLength();
		for (int i  = 0; i  < dataLength; i += 2) {
			if (data[i] == LearningFormatConstants.PROT1_INDEX) {
				result[LearningFormatConstants.PROT1_INDEX].add(Integer.valueOf(i));
			}
			else if (data[i] == LearningFormatConstants.PROT2_INDEX) {
				data[i] = LearningFormatConstants.PROT1_INDEX;
				result[LearningFormatConstants.PROT2_INDEX].add(Integer.valueOf(i));
			}
		}
		
		return result;
	}
	
	public void normalize() {
		List<Integer>[] occurences = prenormalizeEntities();
		if (normalizationNeeded()) {
			revert();
		}
		normalizeEntities(occurences);
		if (normalizationNeeded()) {
			revert();
			if (normalizationNeeded()) {
				throw new IllegalStateException();
			}
		}
	}
	
	private void revert() {
		if (nodeCount > 1) {
			int dataLength = getDataLength();
			int halfDataCount = dataLength/2;
			for (int i = 0; i < halfDataCount; i++) {
				swap(i, dataLength -1 - i);
			}
		}
	}
	public QPath createRevertedQPath() {
		
		QPath result = clone();

		result.revert();
		
		return result;
	}
	
	public QPath subgram(int startNode, int length) {
		if (startNode + length > nodeCount) {
			throw new IllegalStateException();
		}
		
		QPath result = new QPath(length);
        int start = startNode * 2;
        System.arraycopy(this.data, start, result.data, 0, (length * 2) - 1);
		result.nodeCount = length;
		
		return result;	
	}
	
	private void swap(int i1, int i2) {
		int tmp = data[i1];
		data[i1] = data[i2];
		data[i2] = tmp;
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
		int n = getDataLength();
		for (int i = 0; i < n; i++) {
			if (i > 0){
				buffer.append(BracketingConstants.SPACE);
			}
			//buffer.append(getToken(data[i]));
			buffer.append(String.valueOf(data[i]));
		}
		
		buffer.append(BracketingConstants.RIGHT_BRACKET);
	}
	
}