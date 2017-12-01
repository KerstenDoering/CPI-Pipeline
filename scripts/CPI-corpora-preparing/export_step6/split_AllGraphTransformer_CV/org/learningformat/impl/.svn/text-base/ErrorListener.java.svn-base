package org.learningformat.impl;

/**
 * Adds basic error handling/suppression functionality.
 * 
 * @author illes
 *
 */
public class ErrorListener {
	
	private boolean stopOnError;
	private int errors;
	
	public int getErrors() {
		return errors;
	}

	public boolean isStopOnError() {
		return stopOnError;
	}

	public void setStopOnError(boolean stopOnError) {
		this.stopOnError = stopOnError;
	}
	
	public void error(RuntimeException e) throws RuntimeException {
		if (stopOnError)
			throw e;
		
		errors++;
		System.err.println("ERROR: " + e.getMessage());
		e.printStackTrace();
		System.err.println("INFO: trying to continue after error");
	}
}
