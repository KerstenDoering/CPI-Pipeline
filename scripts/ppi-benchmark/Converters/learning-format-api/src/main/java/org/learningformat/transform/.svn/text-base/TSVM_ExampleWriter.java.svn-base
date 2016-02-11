package org.learningformat.transform;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;

import org.learningformat.api.Entity;
import org.learningformat.api.Pair;
import org.learningformat.api.Sentence;
import org.learningformat.api.Token;
import org.learningformat.api.Tokenization;
import org.learningformat.impl.MyPair;

public class TSVM_ExampleWriter  implements ExampleWriter, BracketingConstants{
	protected String tokenizer;
	protected String parser;
	
	public TSVM_ExampleWriter(String tokenizer, String parser){
		super();
		this.tokenizer = tokenizer;
		this.parser = parser;
	}
	
	@Override
	public void write(Pair pair, Sentence sentence, Appendable writer) throws IOException {
		// TODO Auto-generated method stub
		
	}
	public String[] getOutput(Pair pair, Sentence sentence, String tokenizer){
		StringBuilder outSentence= new StringBuilder();
		StringBuilder outProtein = new StringBuilder();
		
		
		Tokenization tokenization = sentence.getTokenization(tokenizer);
		List<Entity>entities=sentence.getEntities();		
//		Parse p = sentence.getParse(tokenizer);
		
//		if(pair.getE1().getCharOffset().overlaps(pair.getE2().getCharOffset()))
//			return new String []{"", "", ""};

		
		//Extract Sentence and a offset map...
		HashMap<Integer, Integer> mapping = new HashMap<Integer, Integer>(); //Mapping between original offsets and new ones 		
		int endLast=-2;//End of the previous token
		int offset=0;
		for(Iterator <Token> it= tokenization.getTokens().iterator(); it.hasNext(); ){
			
			Token token= it.next();
			outSentence.append(token.getText());
			outSentence.append(" "); //Generate String
			
			String original []=token.getCharOffset().getCharOffsets()[0].toString().split("-");
			
			if((endLast+1)==Integer.parseInt(original[0])){
				offset++;
			}
			endLast=Integer.parseInt(original[1]);
			
			for(int i=Integer.parseInt(original[0]); i <= Integer.parseInt(original[1]); i++){
//				System.out.println(i +"<->" +(i+offset));
				mapping.put(i, i+offset);
			}

//			System.out.println(sentence.getText().substring(Integer.parseInt(original[0]), Integer.parseInt(original[1])+1));
//			System.out.println(outSentence.substring(mapping.get(Integer.parseInt(original[0])), (mapping.get(Integer.parseInt(original[1]))+1)));
		}
		

		//Iterate over the entites, but backwards..
		ArrayList<MyPair> al= new ArrayList<MyPair>();
		for(Entity e : entities){
			String []temp=e.getCharOffset().getCharOffsets()[0].toString().split("-");
			al.add(new MyPair(Integer.parseInt(temp[0]),Integer.parseInt(temp[1])));
		}
		Collections.sort(al);
		
		for(MyPair mp : al){
			int start=mapping.get(mp.getStart());
			int end= mapping.get(mp.getEnd());
			
			if(pair.getE1().getCharOffset().getCharOffsets()[0].toString().equals(mp.getCharoffsets().getCharOffsets()[0].toString())){
				outSentence.replace(start, end+1 , "PROTA");
			}	
			
			else if(pair.getE2().getCharOffset().getCharOffsets()[0].toString().equals(mp.getCharoffsets().getCharOffsets()[0].toString())){
				outSentence.replace(start, end+1 , "PROTB");
			}
			else {
				outSentence.replace(start, end+1 , "PROT1");
			}
//			System.out.println(outSentence);

		}


		//OutSentence, may look like: "PROTA-dependant" --> Remove -dependant
		String returnString=outSentence.toString();
		int index= returnString.indexOf("PROTA");	
		if((index+5) != returnString.length() && returnString.charAt(index+"PROTA".length())!=' '){
			returnString= returnString.substring(0,index+"PROTA".length()) +" " +returnString.substring(index+"PROTA".length(), index+"PROTA".length()+1) +" " +returnString.substring(index+"PROTA".length()+1);
		}


		index= returnString.indexOf("PROTB");	
		if((index+5) != returnString.length() &&  returnString.charAt(index+"PROTB".length())!=' '){
			returnString= returnString.substring(0,index+"PROTB".length()) +" " +returnString.substring(index+"PROTB".length(), index+"PROTB".length()+1) +" " +returnString.substring(index+"PROTB".length()+1);			
		}

		//OutSentence, may look like: "Bla-PROTA" -remove first -
		index= returnString.indexOf("PROTA");	
		System.out.println(returnString);
		if(index != 0 && returnString.charAt(index-1) != ' ')
			System.out.println("Laoso");
		
		returnString+="\n";
		
		//Generate the outProtein		
		outProtein.append("PROTA|#|PROTB\n");
		outSentence.append("\n");
//		System.out.println(outSentence);
		
		String[] value=  {returnString, outProtein.toString()};
		
		return value;	
	}
}
