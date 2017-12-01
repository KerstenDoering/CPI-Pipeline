/**
 * 
 */
package org.learningformat.transform;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.learningformat.api.CharOffset;
import org.learningformat.api.Token;
import org.learningformat.api.CharOffset.SingleCharOffset;
import org.learningformat.impl.DefaultToken;

/**
 * 
 * @author illes
 *
 */
public class PennTreeBankConverter
{
    protected static final Pattern mTokenPattern = Pattern.compile(
    		"[(]" + 		// opening paren
    		"([^()\\s]+)" +	// group #1: POS tag 
    		"\\s+" +		// whitespace
    		"([^()\\s]+)" +	// group #2: token
    		"[)]");			// closing paren
    protected static final int mTokenPOSGroup = 1;
    protected static final int mTokenTextGroup = 2;
    
    protected final Matcher mTokenMatcher = mTokenPattern.matcher("");
    
    public static final Map<String, String> ptbEscapes = new HashMap<String, String>();
    
    static {
		ptbEscapes.put("-LRB-", "(");
		ptbEscapes.put("-RRB-", ")");
		ptbEscapes.put("-LSB-", "[");
		ptbEscapes.put("-RSB-", "]");
		ptbEscapes.put("-LCB-", "{");
		ptbEscapes.put("-RCB-", "}");
		ptbEscapes.put("''",    "\"");
		ptbEscapes.put("``",    "\"");
    }
    
    public static String decodePTBTokenText(String tokenText)
    {
	String decoded = ptbEscapes.get(tokenText);
	if (decoded == null) {
	    // TODO really nothing to do?
	    return tokenText;
	} else {
	    // escape found
	    return decoded;
	}
    }


    /**
     * Get tokens from escaped PTB format as defined by {@link #mTokenPattern}. {@link Token}'s {@link CharOffset} will reflect position in the bracketed string.
     * 
     * @note
     * 	No un-escaping of PTB syntax is done (e.g. "-LRB-" to "(")
     * @param bracketed
     * @return
     */
    public List<Token> ptb2tokens(final String bracketed)
    {
	return ptb2tokens(bracketed, new ArrayList<Token>());
    }

    /**
     * Adds tokens to a supplied list after clearing it.
     * @see #ptb2tokens(String)
     * @param bracketed
     * @param tokens
     * @return
     */
    public List<Token> ptb2tokens(final String bracketed, List<Token> tokens)
    {
	mTokenMatcher.reset(bracketed);
	tokens.clear();
	while (mTokenMatcher.find())
	{
	    SingleCharOffset[] offsets = {
		    new SingleCharOffset(
			    mTokenMatcher.start(mTokenTextGroup), 
			    mTokenMatcher.end(mTokenTextGroup))};
	    
	    Token t = new DefaultToken();
	    t.setCharOffset(new CharOffset(offsets));
	    t.setText(mTokenMatcher.group(mTokenTextGroup));
	    t.setPos(mTokenMatcher.group(mTokenPOSGroup));
	    
	    tokens.add(t);
	}
	return tokens;
    }

    /**
     * Convenience method 
     * @param bracketed
     * @param plain
     * @return
     * @see {@link #ptb2alignedTokens(String, String, int, List)}
     */
    public List<Token> ptb2alignedTokens(final String bracketed, final String plain)
    {
    	return ptb2alignedTokens(bracketed, plain, 0, new ArrayList<Token>());
    }

    /**
     * Align tokens extracted from a PTB formatted parse tree's tokens with the source plain text. 
     * @param bracketed PTB format parse tree of sentence
     * @param plain source text of sentence
     * @param baseOffset the sentence's begin offset for document relative offsets
     * @param tokens the list object to be filled with the tokens
     * @return a list of PTB escaped, POS tagged tokens
     *  
     */
    public List<Token> ptb2alignedTokens(final String bracketed, final String plain, final int baseOffset, final List<Token> tokens)
    {
	if (tokens == null || bracketed == null || plain == null)
	    throw new IllegalArgumentException("Should not be null.");
	
	ptb2tokens(bracketed, tokens);
	
	int lastTokenEnd = 0;
	for (int i = 0; i < tokens.size(); ++i)
	{
	    final Token t = tokens.get(i);
	    final String unescapedTokenText = decodePTBTokenText(t.getText()); // the PTB unescaped token text
	    final String decodedTokenText; // the original/input word
	    int index = plain.indexOf(unescapedTokenText, lastTokenEnd);
	    
	    if (index >=0) {
	    	decodedTokenText = unescapedTokenText;	    	
	    }
    	// undo the nasty insertion of a period at the end of the sentences by the parser (if any)
	    else if (index < 0 && i == tokens.size() -1 && unescapedTokenText.equals("."))
	    {
	    	System.err.println("INFO: doing nasty dot-at-the-end-of-sentence removal");
	    	Token prevToken = tokens.get(i-1);
	    	// does prevToken end in a dot?
	    	if (!(prevToken.getText().lastIndexOf('.') == prevToken.getText().length()-1))
	    		throw new IllegalStateException("does not end in dot: " + prevToken);
	    	
	    	// shorten prevToken by 1 (== ".".length())
	    	SingleCharOffset prevOffset =  prevToken.getCharOffset().getCharOffsets()[0];
	    	prevOffset.setStartEnd(prevOffset.getStart(), prevOffset.getEnd()-1);
	    	prevToken.setText(prevToken.getText().substring(0, prevToken.getText().length()-1));
	    	lastTokenEnd--;
	    	decodedTokenText = unescapedTokenText;	    	
	    	index = plain.indexOf(decodedTokenText, lastTokenEnd);

	    }
	    
	    // nasty un-escaped
	    else if (index < 0 && t.getText().equals("''"))
	    {
	    	System.err.println("INFO: doing nasty unescaped token lookup for token `" + t.getText() +"`");
	    	decodedTokenText = t.getText();
		    index = plain.indexOf(decodedTokenText, lastTokenEnd);
	    }
	    else if (index < 0 && t.getText().equals("n't"))
	    {
	    	System.err.println("INFO: doing nasty negative suffix lookup for token `" + t.getText() +"`");
	    	decodedTokenText = "'t";
		    index = plain.indexOf(decodedTokenText, lastTokenEnd);
	    }
	    else
	    {
	    	decodedTokenText = null;
	    }

	    
	    if (index < 0)
	    	throw new IllegalStateException("Could not find token " + (i+1) +" '" + unescapedTokenText + "' (PTB: '" + t.getText() + "') " +
				"when searched from position " + lastTokenEnd + 
				"\n in sentence '" + plain +"'" +
				"\n given PTB '" + bracketed+ "'");
	    
    	SingleCharOffset[] offsets =  t.getCharOffset().getCharOffsets();
    	
    	if (offsets.length != 1)
    	    throw new UnsupportedOperationException("Cannot handle charoffset: " + Arrays.toString(offsets));
    	
    	t.setText(decodedTokenText);
    	
    	// adjust Charoffset
    	offsets[0].setStartEnd(
    		baseOffset + index, 
    		baseOffset + index + decodedTokenText.length());
    	
    	lastTokenEnd = index + decodedTokenText.length();
	}
	
	return tokens;
    }
    
    
    public static void main(String[] args) {
	System.err.println("Testing " + PennTreeBankConverter.class.getCanonicalName());
	PennTreeBankConverter conv = new PennTreeBankConverter();
	
	//String plain = "In vivo studies of the activity of four of the kinases, KinA, KinC, KinD (ykvD) and KinE (ykrQ), using abrB transcription as an indicator of Spo0A~P level, revealed that KinC and KinD were responsible for Spo0A~P production during the exponential phase of growth in the absence of KinA and KinB.";
	//String bracketed = "(S1 (S (NP (NP (ADJP (FW In) (FW vivo)) (NNS studies)) (PP (IN of) (NP (NP (DT the) (NN activity)) (PP (IN of) (NP (NP (NP (CD four)) (PP (IN of) (NP (DT the) (NNS kinases)))) (, ,) (NP (NP (NP (NNP KinA) (, ,) (NNP KinC)) (, ,) (NP (NP (NN KinD)) (PRN (-LRB- -LRB-) (NP (NN ykvD)) (-RRB- -RRB-))) (CC and) (NP (NNP KinE))) (PRN (-LRB- -LRB-) (NP (CD ykrQ)) (-RRB- -RRB-))))))) (, ,) (VP (VBG using) (NP (NN abrB) (NN transcription)) (PP (IN as) (NP (NP (DT an) (NN indicator)) (PP (IN of) (NP (NN Spo0A~P) (NN level)))))) (, ,)) (VP (VBD revealed) (SBAR (IN that) (S (NP (NP (NN KinC)) (CC and) (NP (NN KinD))) (VP (VBD were) (ADJP (JJ responsible) (PP (IN for) (NP (NN Spo0A~P) (NN production)))) (PP (IN during) (NP (NP (DT the) (JJ exponential) (NN phase)) (PP (IN of) (NP (NN growth))))) (PP (IN in) (NP (NP (DT the) (NN absence)) (PP (IN of) (NP (NP (NN KinA)) (CC and) (NP (NN KinB)))))))))) (. .)))";
	String plain = "Therefore, ftsY is solely expressed during sporulation from a sigma(K)- and GerE-controlled promoter that is located immediately upstream of ftsY inside the smc gene.";
	String bracketed = "(S1 (S (S (ADVP (RB Therefore)) (, ,) (NP (NN ftsY)) (VP (VBZ is) (ADVP (RB solely)) (VP (VBN expressed) (PP (IN during) (NP (NP (NN sporulation)) (PP (IN from) (NP (NP (NP (NP (DT a) (NN sigma)) (PRN (-LRB- -LRB-) (NP (NN K)) (-RRB- -RRB-)) (: -)) (CC and) (NP (JJ GerE-controlled) (NN promoter))) (SBAR (WHNP (WDT that)) (S (VP (VBZ is) (ADJP (JJ located) (ADVP (RB immediately) (RB upstream) (PP (IN of) (NP (NN ftsY)))) (S (VP (VBP inside) (NP (DT the) (NN smc) (NN gene))))))))))))))) (. .)))";
	List<Token> tokens = conv.ptb2alignedTokens(bracketed, plain);
	
	System.out.println("PLAIN:\t" + plain);
	System.out.println("BRACKETED:\t" + plain);
	System.out.println("ALIGNED:\t" + Arrays.toString(tokens.toArray()));
    }
    
    
}
