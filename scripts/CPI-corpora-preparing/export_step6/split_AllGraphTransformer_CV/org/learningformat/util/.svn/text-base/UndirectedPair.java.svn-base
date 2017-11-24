package org.learningformat.util;

/**
 * Ensures that (1,2) == (2,1) through {@link #hashCode()} and {@link #equals(Object)}. 
 * @author illes
 *
 * @param <T>
 */
public class UndirectedPair<T> implements Comparable<UndirectedPair<T>> {
	protected final T id1;
	protected final T id2;
	
	public UndirectedPair(T id1, T id2) {
		if (id1 == null || id2 == null)
			throw new NullPointerException();
		
		this.id1 = id1;
		this.id2 = id2;
	}
		
	@SuppressWarnings("unchecked")
	@Override
	public boolean equals(Object obj) {
		UndirectedPair<T> other = (UndirectedPair<T>) obj;
		return (other.id1.equals(id1) && other.id2.equals(id2))
		|| (other.id1.equals(id2) && other.id2.equals(id1));
	}

	/**
	 * Returns a value independent of the order of elements.
	 */
	@Override
	public int hashCode() {
		return id1.hashCode() ^ id2.hashCode();
	}

	@Override
	public int compareTo(UndirectedPair<T> o) {
		return o.hashCode() - this.hashCode();
	}
}
