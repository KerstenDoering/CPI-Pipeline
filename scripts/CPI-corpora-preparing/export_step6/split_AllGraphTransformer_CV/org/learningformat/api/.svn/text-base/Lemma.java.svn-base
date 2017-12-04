package org.learningformat.api;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.util.HashMap;

public class Lemma {
	
	
	
	public static HashMap<String, String> readLemma(String filename){
		HashMap<String, String> lemmata = new HashMap<String, String>();
//		
		
		try{

		    FileInputStream fstream = new FileInputStream(filename);
		    DataInputStream in = new DataInputStream(fstream);
	        BufferedReader br = new BufferedReader(new InputStreamReader(in));
		    String strLine;

		    while ((strLine = br.readLine()) != null)   {	    	
		      String []line=strLine.split("\t");
		      if(line.length==2)
		    	  lemmata.put(line[0], line[1].split(" ")[0]);
		      
		    }

		    in.close();
		    }catch (Exception e){//Catch exception if any
		      System.err.println("Error: " + e.getMessage());
		    }
		
		
		return lemmata;		
	}

}
