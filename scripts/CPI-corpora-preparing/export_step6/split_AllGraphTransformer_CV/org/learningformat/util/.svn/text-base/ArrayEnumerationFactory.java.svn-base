package org.learningformat.util;
import java.util.Enumeration;
import java.util.NoSuchElementException;

final public class ArrayEnumerationFactory {
  static public <T> Enumeration<T> makeEnumeration(final T[] obj) {
      return (new Enumeration<T>() {
        final int size = obj.length;
        int cursor;

        public boolean hasMoreElements() {
          return (cursor < size);
        }

		public T nextElement() {
			if (hasMoreElements())
				return obj[cursor++];
			else 
				throw new NoSuchElementException();
        }
      });
  }

  public static void main(String args[]) {
    Enumeration<String> e = makeEnumeration(args);
    while (e.hasMoreElements()) {
      System.out.println(e.nextElement());
    }
  }
}