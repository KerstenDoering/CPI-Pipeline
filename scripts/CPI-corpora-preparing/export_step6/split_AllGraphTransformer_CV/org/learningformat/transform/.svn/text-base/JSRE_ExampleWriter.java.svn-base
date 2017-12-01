package org.learningformat.transform;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.learningformat.api.CharOffset;
import org.learningformat.api.Entity;
import org.learningformat.api.Pair;
import org.learningformat.api.Sentence;
import org.learningformat.api.Token;
import org.learningformat.api.Tokenization;
import org.learningformat.api.JSRE_Tranformer.Lemmatizer;

public class JSRE_ExampleWriter implements ExampleWriter, BracketingConstants{
	private final String tokenizer;

	public JSRE_ExampleWriter(String tokenizer){
		super();
		this.tokenizer = tokenizer;
	}
	
	public String getOutput(Pair pair, Sentence sentence, Lemmatizer lemmatizer){
		
		StringBuilder out= new StringBuilder();
		
//		Bracketing b = sentence.getBracketing(parser);
//		String bracketingTree = b.getBracketing();
		Tokenization tokenization = sentence.getTokenization(tokenizer);
		if (tokenization == null)
		{
			List<String> ts = new ArrayList<String>();
			if (sentence.getTokenizations() != null)
				for (Tokenization t : sentence.getTokenizations())
					ts.add(t.getTokenizer());
			throw new IllegalStateException("no tokenization '" + tokenizer +"' (found: " + ts.toString() +")");
		}

		//Pos/Neg-Example
		out.append(pair.isInteraction() ? SvmLightTreeKernelConstants.JSRE_ONE : SvmLightTreeKernelConstants.JSRE_ZERO);
		out.append(SvmLightTreeKernelConstants.TAB);
		
		//Unique-Id
		out.append(pair.getId());
		out.append(SvmLightTreeKernelConstants.TAB);

		List<Entity> entities=sentence.getEntities();

		//Iterate over the specific token
		int counter=0;	
		boolean protA=false, protB=false; //Both proteins are not found sofar
//		int protA=0;
		for (Token t : tokenization.getTokens()) {
			
			CharOffset tokenCharOffset = t.getCharOffset();
			
			boolean ovelapsE1 = tokenCharOffset.overlaps(pair.getE1().getCharOffset()); 
			boolean ovelapsE2 = tokenCharOffset.overlaps(pair.getE2().getCharOffset()); 

			
			//This part checks if the current entity has been already visited
			boolean cont=false;
			//The entities are overlapping
//			if(ovelapsE1 || ovelapsE2 || t.isEntity()){				
				
				
//			}
					
			
			//Approach is unable to handle this..
			if (ovelapsE1 && ovelapsE2) {
//				System.out.println("Pair: " +pair.getId() +" is overlapping");
				out.append(Integer.toString(counter++)); //Id
				out.append(BracketingConstants.JSRE_SEP);
				
				out.append(BracketingConstants.PROT_A);	//Text
				out.append(BracketingConstants.JSRE_SEP);
				
				out.append(BracketingConstants.PROT_A);	//Lemma
				out.append(BracketingConstants.JSRE_SEP);
				
				out.append(t.getPos());					//POS
				out.append(BracketingConstants.JSRE_SEP);
				
				out.append(BracketingConstants.PROT_ENTITY); //Entity Type
				out.append(BracketingConstants.JSRE_SEP);
				
				out.append(BracketingConstants.LABEL_TARGET); //Entity Label
				out.append(BracketingConstants.SPACE); //Seperate each token with a space
				
				
				out.append(Integer.toString(counter++)); //Id
				out.append(BracketingConstants.JSRE_SEP);
				
				out.append(BracketingConstants.PROT_A);	//Text
				out.append(BracketingConstants.JSRE_SEP);
				
				out.append(BracketingConstants.PROT_A);	//Lemma
				out.append(BracketingConstants.JSRE_SEP);
				
				out.append(t.getPos());					//POS
				out.append(BracketingConstants.JSRE_SEP);
				
				out.append(BracketingConstants.PROT_ENTITY); //Entity Type
				out.append(BracketingConstants.JSRE_SEP);
				
				out.append(BracketingConstants.LABEL_TARGET); //Entity Label
				out.append(BracketingConstants.SPACE); //Seperate each token with a space
				
				protA=true; protB=true;
//				return "";
			}		
			
			
			//First entity
			else if (ovelapsE1 || ovelapsE2) {
				
				//This assures, that each entity is only printed out once
				if(ovelapsE1 && (protA==false)){
					protA=true;
					cont=true;
				}
				
				if(ovelapsE2 && (protB==false)){
					protB=true;
					cont=true;
				}

				if(cont==true){			
					out.append(Integer.toString(counter++)); //Id
					out.append(BracketingConstants.JSRE_SEP);
					
					out.append(BracketingConstants.PROT_A);	//Text
					out.append(BracketingConstants.JSRE_SEP);
					
					out.append(BracketingConstants.PROT_A);	//Lemma
					out.append(BracketingConstants.JSRE_SEP);
					
					out.append(t.getPos());					//POS
					out.append(BracketingConstants.JSRE_SEP);
					
					out.append(BracketingConstants.PROT_ENTITY); //Entity Type
					out.append(BracketingConstants.JSRE_SEP);
					
					out.append(BracketingConstants.LABEL_TARGET); //Entity Label
					
					out.append(BracketingConstants.SPACE); //Seperate each token with a space
					
//					protA++;
				}
			}
			
			//Irelevant entity
			else if (t.isEntity()) {
				
				//Dont print Entity twice for example for Proteinname [seperator] Proteinname
				for(Entity entity: entities){
					if(entity.getCharOffset().getCharOffsets()[0].getStart()==t.getCharOffset().getCharOffsets()[0].getStart())
							cont=true;
				}
				
				if(cont==true){				
				
					out.append(Integer.toString(counter++)); //Id
					out.append(BracketingConstants.JSRE_SEP);
					
					out.append(BracketingConstants.PROT_B);	//Text
					out.append(BracketingConstants.JSRE_SEP);
					
					out.append(BracketingConstants.PROT_B);	//Lemma
					out.append(BracketingConstants.JSRE_SEP);
					
					out.append(t.getPos());					//POS
					out.append(BracketingConstants.JSRE_SEP);
					
					out.append(BracketingConstants.PROT_ENTITY); //Entity Type
					out.append(BracketingConstants.JSRE_SEP);
					
					out.append(BracketingConstants.EMPTY); //Entity Label
					
					out.append(BracketingConstants.SPACE); //Seperate each token with a space
				}
			}
			//No entity
			else {
				out.append(Integer.toString(counter++)); //Id
				out.append(BracketingConstants.JSRE_SEP);
				
				out.append(t.getText());	//Text
				out.append(BracketingConstants.JSRE_SEP);
				
				out.append(lemmatizer.lemmatize(t.getText()));	//Lemma!!#@todo
				out.append(BracketingConstants.JSRE_SEP);
				
				out.append(t.getPos());					//POS
				out.append(BracketingConstants.JSRE_SEP);
				
				out.append(BracketingConstants.EMPTY); //Entity Type
				out.append(BracketingConstants.JSRE_SEP);
				
				out.append(BracketingConstants.EMPTY); //Entity Label
				
				out.append(BracketingConstants.SPACE); //Seperate each token with a space
			}			
			
			
		}

		out.append(SvmLightTreeKernelConstants.EOL);

		String textEntityA="";
		String textEntityB="";
		try{
			textEntityA=sentence.getText().substring(pair.getE1().getCharOffset().getCharOffsets()[0].getStart(), pair.getE1().getCharOffset().getCharOffsets()[0].getEnd());
			textEntityB= sentence.getText().substring(pair.getE2().getCharOffset().getCharOffsets()[0].getStart(), pair.getE2().getCharOffset().getCharOffsets()[0].getEnd());			
		}
		catch(Exception e){
			System.err.println("Index out of bounds for " +pair.getId());
		}
		
		if(protA && protB)
			return out.toString();
		else 
			System.err.println("ERROR: Some entities not found in pair " + pair.getId() + ", sentence " + sentence.getId() + " (" +
					pair.getE1().getId() + ": span=" + pair.getE1().getCharOffset() +" text='" +pair.getE1().getText() +"'<->'" +textEntityA + "'; " + 
					pair.getE2().getId() + ": span=" + pair.getE2().getCharOffset() +" text='" +pair.getE2().getText() +"'<->'" +textEntityB 
					+" pairA=" +protA +" pairB=" +protB + "')");
			
		return "";
		
	}
	
	
	public void write(Pair pair, Sentence sentence, Appendable out)	throws IOException {
	
//		HashMap<String, String > lemmata=Lemma.readLemma("/home/philippe/Desktop/svm/otherMethods/jsre/corpus/out/tst.txt.txp");
//		
//
//		
////		Bracketing b = sentence.getBracketing(parser);
////		String bracketingTree = b.getBracketing();
//		Tokenization tokenization = sentence.getTokenization(tokenizer);
//		
//		//Generate the specific output
//		//Pos/Neg-Example
//		out.append(pair.isInteraction() ? SvmLightTreeKernelConstants.JSRE_ONE : SvmLightTreeKernelConstants.JSRE_ZERO);
//		out.append(SvmLightTreeKernelConstants.TAB);
//		
//		//Unique-Id
//		out.append(sentence.getId() + pair.getId());
//		out.append(SvmLightTreeKernelConstants.TAB);
//
//		//Body
//		int end = 0;
//		//Iterate over the specific token
//		int counter=0;
//		loop:for (Token t : tokenization.getTokens()) {
//			CharOffset tokenCharOffset = t.getCharOffset();
//			
//			boolean ovelapsE1 = tokenCharOffset.overlaps(pair.getE1().getCharOffset()); 
//			boolean ovelapsE2 = tokenCharOffset.overlaps(pair.getE2().getCharOffset()); 
//			
//			if (ovelapsE1 && ovelapsE2) {
//				continue loop;
//			}
//			
//			
//			
//			else if (ovelapsE1 || ovelapsE2) {
//				out.append(Integer.toString(counter++)); //Id
//				out.append(BracketingConstants.JSRE_SEP);
//				
//				out.append(BracketingConstants.PROT_A);	//Text
//				out.append(BracketingConstants.JSRE_SEP);
//				
//				out.append(BracketingConstants.PROT_A);	//Lemma
//				out.append(BracketingConstants.JSRE_SEP);
//				
//				out.append(t.getPos());					//POS
//				out.append(BracketingConstants.JSRE_SEP);
//				
//				out.append(BracketingConstants.PROT_ENTITY); //Entity Type
//				out.append(BracketingConstants.JSRE_SEP);
//				
//				out.append(BracketingConstants.LABEL_TARGET); //Entity Label
//				out.append(BracketingConstants.JSRE_SEP);
//			}
//			
//			else if (t.isEntity()) {
//				out.append(Integer.toString(counter++)); //Id
//				out.append(BracketingConstants.JSRE_SEP);
//				
//				out.append(BracketingConstants.PROT_B);	//Text
//				out.append(BracketingConstants.JSRE_SEP);
//				
//				out.append(BracketingConstants.PROT_B);	//Lemma
//				out.append(BracketingConstants.JSRE_SEP);
//				
//				out.append(t.getPos());					//POS
//				out.append(BracketingConstants.JSRE_SEP);
//				
//				out.append(BracketingConstants.PROT_ENTITY); //Entity Type
//				out.append(BracketingConstants.JSRE_SEP);
//				
//				out.append(BracketingConstants.LABEL_TARGET); //Entity Label
//				out.append(BracketingConstants.EMPTY);
//			}
//			else {
//				out.append(Integer.toString(counter++)); //Id
//				out.append(BracketingConstants.JSRE_SEP);
//				
//				out.append(t.getText());	//Text
//				out.append(BracketingConstants.JSRE_SEP);
//				
//				out.append(lemmata.get(t.getText()));	//Lemma!!#@todo
//				out.append(BracketingConstants.JSRE_SEP);
//				
//				out.append(t.getPos());					//POS
//				out.append(BracketingConstants.JSRE_SEP);
//				
//				out.append(BracketingConstants.EMPTY); //Entity Type
//				out.append(BracketingConstants.JSRE_SEP);
//				
//				out.append(BracketingConstants.EMPTY); //Entity Label
////				out.append(BracketingConstants.EMPTY);			
//			}
//			
//			out.append(BracketingConstants.SPACE);
//		}
//		
//
//		
//
//		out.append(SvmLightTreeKernelConstants.EOL);
	} 
	
//	protected int write(int end, String text, Token token, Bracketing bracketing, String bracketingTree, Appendable sb) throws IOException {
//		
//		System.out.println(token.getText());
//		for (SingleCharOffset sentenceOffset : token.getCharOffset().getCharOffsets()) {
//			
//			SingleCharOffset bracketingOffset = bracketing.toBracketingCharOffset(sentenceOffset);
////			sb.append(bracketingTree, end, bracketingOffset.getStart());
//			
//			if (text != null) {
//				sb.append(text);
//			}
//			else {
//				sb.append(bracketingTree, bracketingOffset.getStart(), bracketingOffset.getEnd());
//			}
//			end = bracketingOffset.getEnd();
//		}
//		return end;
//	}

}
