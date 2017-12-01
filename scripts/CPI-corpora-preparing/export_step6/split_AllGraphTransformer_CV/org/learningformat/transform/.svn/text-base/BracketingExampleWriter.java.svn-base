package org.learningformat.transform;

import java.io.IOException;

import org.learningformat.api.Bracketing;
import org.learningformat.api.CharOffset;
import org.learningformat.api.LearningFormatConstants;
import org.learningformat.api.Pair;
import org.learningformat.api.Sentence;
import org.learningformat.api.Token;
import org.learningformat.api.Tokenization;
import org.learningformat.api.CharOffset.SingleCharOffset;
import org.learningformat.transform.SvmLightTreeKernelConstants.LineStyle;

public class BracketingExampleWriter implements BracketingConstants, ExampleWriter {
	protected String tokenizer;
	protected String parser;
	protected LineStyle lineStyle;
	
	
	public BracketingExampleWriter(String tokenizer, String parser, LineStyle lineStyle) {
		super();
		this.tokenizer = tokenizer;
		this.parser = parser;
		this.lineStyle = lineStyle;
	}

	protected int write(int end, String text, Token token, Bracketing bracketing, String bracketingTree, Appendable sb) throws IOException {
		for (SingleCharOffset sentenceOffset : token.getCharOffset().getCharOffsets()) {
			SingleCharOffset bracketingOffset = bracketing.toBracketingCharOffset(sentenceOffset);
//			System.out.println(bracketingTree);
//			System.out.println(end);
//			System.out.println(bracketingOffset.getStart());
//			System.out.println(bracketingTree.substring(end, bracketingOffset.getStart()));
//			
			if(end > bracketingOffset.getStart()){				
				System.out.println("error: end=" + end + " > start=" +  bracketingOffset.getStart() +" while processing '" + text +"' (" + sentenceOffset +" ~ " + bracketingOffset+ " ) in '" + bracketingTree +"'");
//				sb.append("ERROR");
//
				end = bracketingOffset.getEnd()+1;
				throw new IllegalStateException();
				//continue;
			}
				
			
			sb.append(bracketingTree, end, bracketingOffset.getStart());
			if (text != null) {
				sb.append(text);
//				end = bracketingOffset.getEnd()+1;
			}
			else {
				sb.append(bracketingTree, bracketingOffset.getStart(), bracketingOffset.getEnd());
//				end = bracketingOffset.getEnd();
			}
			end = bracketingOffset.getEnd();			
		}
		return end;
	}

	public void write(Pair pair, Sentence sentence, Appendable out) throws IOException {
		
		out.append(pair.isInteraction() ? SvmLightTreeKernelConstants.POSITIVE_EXAMPLE : SvmLightTreeKernelConstants.NEGATIVE_EXAMPLE);
		out.append(SvmLightTreeKernelConstants.SPACE);
		switch (lineStyle) {
		case MOSCHITTI:
			out.append(SvmLightTreeKernelConstants.BT);
			out.append(SvmLightTreeKernelConstants.SPACE);
			break;
		case CUSTOM_KERNEL:
			out.append(SvmLightTreeKernelConstants.HASH);
			break;

		default:
			throw new IllegalStateException("Unexpected lineStyle '"+ lineStyle +"'");
		}
		
		
		Bracketing b = sentence.getBracketing(parser);
		if(b == null)
			throw new IllegalStateException("No braketing '" +parser +"'");
		String bracketingTree = b.getBracketing();
		Tokenization tokenization = sentence.getTokenization(tokenizer);
		
		int end = 0;
		for (Token t : tokenization.getTokens()) {
			CharOffset tokenCharOffset = t.getCharOffset();
			
			boolean ovelapsE1 = tokenCharOffset.overlaps(pair.getE1().getCharOffset()); 
			boolean ovelapsE2 = tokenCharOffset.overlaps(pair.getE2().getCharOffset()); 
			
			if (ovelapsE1 && ovelapsE2) {
				end = write(end, LearningFormatConstants.PROT1_AND_PROT2, t, b, bracketingTree, out);
			}
			else if (ovelapsE1) {
				end = write(end, LearningFormatConstants.PROT1, t, b, bracketingTree, out);
			}
			else if (ovelapsE2) {
				end = write(end, LearningFormatConstants.PROT2, t, b, bracketingTree, out);
			}
			else if (t.isEntity()) {
				end = write(end, LearningFormatConstants.PROT, t, b, bracketingTree, out);
			}
			else {
				end = write(end, null, t, b, bracketingTree, out);
			}
		}
		
		
		if (end < bracketingTree.length()) {
			/* append the rest */
			out.append(bracketingTree, end, bracketingTree.length());
		}
		switch (lineStyle) {
		case MOSCHITTI:
			out.append(SvmLightTreeKernelConstants.SPACE);
			out.append(SvmLightTreeKernelConstants.ET);
			break;
		case CUSTOM_KERNEL:
			break;
		default:
			throw new IllegalStateException("Unexpected lineStyle '"+ lineStyle +"'");
		}
		out.append(SvmLightTreeKernelConstants.EOL);

	}
	
	
}
