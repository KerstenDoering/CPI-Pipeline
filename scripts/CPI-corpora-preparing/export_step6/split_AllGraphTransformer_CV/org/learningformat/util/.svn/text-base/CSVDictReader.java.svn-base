package org.learningformat.util;

import java.io.IOException;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import java.util.NoSuchElementException;

import au.com.bytecode.opencsv.CSVReader;

public class CSVDictReader {
	
	final CSVReader csvReader;
	private String[] columnMapping;
	private Map<String, Integer> invertedColumnMapping;
	
	final private DictRow cursor;
	
	public CSVDictReader(CSVReader reader) {
		this.csvReader = reader;
        this.invertedColumnMapping = Collections.emptyMap();
        this.columnMapping = new String[] {};
		this.cursor = new DictRow(); 
	}
	
	protected static <T> String arrayToString(T[] a)
	{
		return "ARRAY[" + a.length + "]=" + Arrays.toString(a);
	}

	/**
	 * Read column names from next row in CSV input
	 * @return
	 * @throws IOException
	 */
	public CSVDictReader captureHeader() throws IOException {
		String[] row = csvReader.readNext();
		
		if (row == null)
			throw new IOException("premature end of input", new NullPointerException());
		
		setColumnMapping(row);
		return this;
	}

	/**
	 * Setup a mapping from column names to column index.
	 * @return
	 * @throws IOException
	 */
    public void setColumnMapping(String[] columnMapping) {
    	if (columnMapping == null)
    		throw new NullPointerException();
        this.columnMapping = columnMapping.clone();
        this.invertedColumnMapping = toMap(this.columnMapping);
    }

	private static Map<String, Integer> toMap(String[] columns) {
	    Map<String, Integer> columnIndex = new HashMap<String, Integer>(columns.length);
	    for (int i = 0; i < columns.length; i++)
	    {
	    	if (columns[i] == null)	{
	    		System.err.println("WARNING: Skipping untitled column " + (i+1) +"");
	    		continue;
	    	}
	    	
	    	if (columnIndex.containsKey(columns[i])) {
				System.err.println("WARNING: " +
						"Skipping duplicate column name '" + columns[i] + "' " +
						"(current: " + i + ", first seen: " + columnIndex.get(columns[i]));
	    		continue;
	    	}
			columnIndex.put(columns[i], new Integer(i));
	    }
	    return columnIndex;
	}
	
	public static <T> T coalesce(T a, T b) {
	    return a == null ? b : a;
	}
	
	public static <T> T coalesce(T a, T b, T c) {
	    return a != null ? a : coalesce(b, c);
	}
	
	public static <T> T coalesce(T a, T b, T c, T d) {
	    return a != null ? a : coalesce(b, c, d);
	}
	
	
	public DictRow readNext() throws IOException
	{
		String[] row = csvReader.readNext();
		if (row == null)
			return null;
		cursor.setRow(row);
		return cursor;
	}
	
	/**
	 * Provides associative access to an underlying
	 * @author illes
	 *
	 */
	public class DictRow {
		
		private String[] csvRow;
		
		private void setRow(String[] row)
		{
			csvRow = row;
		}
		
		/**
		 * Get a copy of the underlying row.
		 * @return
		 */
		public String[] getRow()
		{
			return csvRow.clone();
		}
		
		/**
		 * Get the value of the column <code>col</code> from the current row.
		 * @param colName
		 * @return
		 */
		public String get(int col) {
			if (col < 0)
				throw new IllegalArgumentException();
			if (col >= csvRow.length)
				return null; //throw new NoSuchElementException();
//			System.err.println("Getting " + col);
			return csvRow[col];
		}
		
		/**
		 * Get the value of the column named <code>colName</code> from the current row.
		 * @param colName
		 * @return
		 */
		public String get(String colName) {
			if (colName == null)
				throw new NullPointerException();
			
			Integer col = invertedColumnMapping.get(colName);
			if (col == null)
				throw new NoSuchElementException();
			
			if (col.intValue() < 0)
				throw new IllegalStateException();
				
			return get(col.intValue());
		}
		
		/** 
		 * Convenience method.
		 * @param col
		 * @param defaultValue
		 * @return
		 */
		public String get(int col, String defaultValue) {
			return coalesce(get(col), defaultValue);
		}
		
		/** 
		 * Convenience method.
		 * @param colName
		 * @param defaultValue
		 * @return
		 */
		public String get(String colName, String defaultValue) {
			return coalesce(get(colName), defaultValue);
		}
		
		@Override
		public String toString() {
//			System.out.println(Arrays.toString(new String[] {}));
//			System.out.println(Arrays.toString(new String[] {""}));
			return arrayToString(csvRow);
		}
		
		
	}
}
