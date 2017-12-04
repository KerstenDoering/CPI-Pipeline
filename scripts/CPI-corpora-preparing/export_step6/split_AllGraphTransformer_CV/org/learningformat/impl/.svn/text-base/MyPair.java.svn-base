package org.learningformat.impl;

import org.learningformat.api.CharOffset;

public class MyPair implements Comparable<MyPair>{

	int start;
	int end;
	
	
	public MyPair(int start, int end) {
		super();
		this.start = start;
		this.end = end;
	}
	
	public CharOffset getCharoffsets(){
		return (new CharOffset(start+"-"+end));
	}


	public int getStart() {
		return start;
	}


	public void setStart(int start) {
		this.start = start;
	}


	public int getEnd() {
		return end;
	}


	public void setEnd(int end) {
		this.end = end;
	}


	@Override
	public int compareTo(MyPair arg0) {
		return  arg0.start - this.start;
	}
	
	
}
