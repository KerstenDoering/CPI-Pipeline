package org.learningformat.standoff;

//import static net.sf.practicalxml.builder.XmlBuilder.attribute;
import static net.sf.practicalxml.builder.XmlBuilder.element;
import static org.learningformat.standoff.StandoffParser.toSingleCharOffset;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.nio.charset.Charset;
import java.util.zip.GZIPOutputStream;

import net.sf.practicalxml.builder.AttributeNode;
import net.sf.practicalxml.builder.CommentNode;
import net.sf.practicalxml.builder.ElementNode;
import net.sf.practicalxml.builder.Node;
import net.sf.practicalxml.builder.XmlBuilder;

import org.learningformat.api.CharOffsetProvider;
import org.learningformat.api.Corpus;
import org.learningformat.api.Dependency;
import org.learningformat.api.Document;
import org.learningformat.api.Entity;
import org.learningformat.api.Pair;
import org.learningformat.api.Parse;
import org.learningformat.api.Sentence;
import org.learningformat.api.Token;
import org.learningformat.api.Tokenization;
import org.learningformat.xml.Attributes;
import org.learningformat.xml.Elements;

/**
 * Class to convert the in-memory representation of a corpus to Airola-style XML.
 * 
 * @author illes
 *
 */
public class AirolaXmlWriter {
	
	public static final int NO_INDENTATION = -1;
	
	/**
	 * Output only sentences having at least one pair.
	 */
	private boolean sentencesWithPairsOnly;
	
	public void setSentencesWithPairsOnly(boolean sentencesWithPairsOnly) {
		this.sentencesWithPairsOnly = sentencesWithPairsOnly;
	}
	
	
	
	/**
	 * Convenience method to write an XML to file.
	 * 
	 * @param corpus
	 * @param outFile
	 * @param indent non-negative values result in indented output, negative values result in no whitespace between elements (fast). 
	 * @throws IOException 
	 */
	public void toXMLFile(Corpus corpus, File outFile, int indent) throws IOException
	{
		ElementNode xml = toXml(corpus);
		OutputStream out;
		
		if(outFile.toString().endsWith(".gz"))	//TODO: Phils code.. Okay?
			out = new GZIPOutputStream(new FileOutputStream(outFile));
		else
			out = new FileOutputStream(outFile);
		toXMLStream(xml, out, indent);
		out.close();
	}

	/**
	 * Write XML to stream, without indentation.
	 * @param corpus
	 * @param outFile
	 * @throws IOException 
	 */
	public static void toXMLStream(ElementNode xml, OutputStream out) throws IOException
	{
		toXMLStream(xml, out, NO_INDENTATION);
	}
	
	/**
	 * Write XML to stream. 
	 * @param corpus
	 * @param outFile
	 * @param indent non-negative values result in indented output, NO_INDENTATION results in no whitespace between elements (fast). 
	 * @throws IOException 
	 */
	public static void toXMLStream(ElementNode xml, OutputStream out, int indent) throws IOException
	{
		if (xml == null)
			throw new IllegalArgumentException();
		if (out == null)
			throw new IllegalArgumentException();
		
		if (indent >= 0)
			out.write(xml.toString(indent).getBytes(Charset.forName("UTF-8")));
		else if (indent == NO_INDENTATION)
			xml.toStream(out);
		else
			throw new IllegalArgumentException("Unrecognized indent: " + indent);
	}

	private static ElementNode toElementNode(Corpus corpus)
	{
		return element(Elements.corpus,
				attribute(Attributes.source, corpus.getSource()));
	}

	private static ElementNode toElementNode(Document d)
	{
    	return element(Elements.document,
				attribute(Attributes.id, d.getId()),
				attribute(Attributes.origId, d.getOrigId()));
	}
	
	private static ElementNode toElementNode(Pair p)
	{
		return element(Elements.pair,
				attribute(Attributes.id, p.getId()),
				attribute(Attributes.e1, p.getE1().getId()),
				attribute(Attributes.e2, p.getE2().getId()),
				attribute(Attributes.interaction, p.isInteraction() ? "True" : "False"),
				attribute(Attributes.type, p.getType()));
	}
	
	private static ElementNode toElementNode(Entity e)
	{
		return element(Elements.entity,
				attribute(Attributes.id, e.getId()),
				attribute(Attributes.charOffset, charOffsetDescriptor(e)),
				attribute(Attributes.text, e.getText()),
				attribute(Attributes.type, e.getType()),
				attribute(Attributes.origId, e.getOrigId()));		
	}
	
	private static ElementNode toElementNode(Sentence s)
	{
		return element(Elements.sentence,
				attribute(Attributes.id, s.getId()),
				attribute(Attributes.origId, s.getOrigId()),
				attribute(Attributes.text, s.getText()),
				attribute(Attributes.charOffset, charOffsetDescriptor(s)));	     	
	}
	
	/**
	 * <pre>&lt;parse parser="Charniak-Lease" tokenizer="Charniak-Lease"></pre>
	 * @param p
	 * @return
	 */
	private static ElementNode toElementNode(Parse p)
	{
		return element(Elements.parse,
				attribute(Attributes.parser, p.getParser()),
				attribute(Attributes.tokenizer, p.getTokenization().getTokenizer()));	     	
	}
	
//    <sentenceanalyses>
//    <parses>
//      
//        <dependency id="clp_1" t1="clt_3" t2="clt_2" type="nn" />
	
		/**
		 * <pre>&lt;dependency id="clp_1" t1="clt_3" t2="clt_2" type="nn" /></pre>
		 * @param d
		 * @return
		 */
    	private static ElementNode toElementNode(Dependency d)
    	{
    		return element(Elements.dependency,
    				attribute(Attributes.id, d.getId()),
    				attribute(Attributes.t1, d.getT1().getId()),
    				attribute(Attributes.t2, d.getT2().getId()),
    				attribute(Attributes.type, d.getType()));	     	
    	}

    	
        
		/**
		 * <pre>&lt;token POS="IN" charOffset="0-1" id="clt_1" text="In" /></pre>
		 * @param t
		 * @return
		 */
    	private static ElementNode toElementNode(Token t)
    	{
    		return element(Elements.token,
    				attribute(Attributes.POS, t.getPos()),
    				attribute(Attributes.charOffset, charOffsetDescriptor(t)),
    				attribute(Attributes.id, t.getId()),
    				attribute(Attributes.text, t.getText()));	     	
    	}
    	/**
    	 * <pre>&lt;tokenization tokenizer="Charniak-Lease"></pre> 
    	 */
    	private static ElementNode toElementNode(Tokenization t)
    	{
    		return element(Elements.tokenization,
    				attribute(Attributes.tokenizer, t.getTokenizer()));	     	
    	}
    	

    	private Node toXml(Parse p) {
    		
    		ElementNode parseNode = toElementNode(p); 
    		
    		for (Dependency d : p.getDependencies())
    			parseNode.addChild(toElementNode(d));

    		return parseNode;
    	}
    	
    	private Node toXml(Tokenization t) {
    		
    		ElementNode tokenizationNode = toElementNode(t); 
    		
    		for (Token n : t.getTokens())
    			tokenizationNode.addChild(toElementNode(n));

    		return tokenizationNode;
    	}


	/**
	 * Assemble a standoff annotated Airola-style XML from PPI mentions. 
	 */
	public ElementNode toXml(Corpus corpus)
	{
		ElementNode root = toElementNode(corpus);
				
		for (Document d : corpus.getDocuments())
		{
			Node documentNode = toXml(d);
		    root.addChild(documentNode);
	    }
		return root;
	}
	
	private Node toXml(Sentence s) {
		
		ElementNode sentenceNode = toElementNode(s);
		
		if (sentencesWithPairsOnly && s.getAllPairs().size() == 0)
			return new CommentNode(("skipped sentence without a pair: " + sentenceNode.toString(NO_INDENTATION)).trim());

		for (Entity e : s.getEntities())
			sentenceNode.addChild(toElementNode(e));

		for (Pair ppi : s.getAllPairs())
			sentenceNode.addChild(toElementNode(ppi));
				
		if (!s.getTokenizations().isEmpty())
		{
			ElementNode sentenceAnalysis = element(Elements.sentenceanalyses);
			ElementNode tokenizations = element(Elements.tokenizations);
			
			for (Tokenization t : s.getTokenizations())
				tokenizations.addChild(toXml(t));
			
			sentenceAnalysis.addChild(tokenizations);
					
			if (!s.getParses().isEmpty())
			{
				ElementNode parses = element(Elements.parses);
				
				for (Parse p : s.getParses())
					parses.addChild(toXml(p));
				
				sentenceAnalysis.addChild(parses);
			}
			sentenceNode.addChild(sentenceAnalysis);
		}

		return sentenceNode;
	}
	
	
	
	
	private Node toXml(Document d) {
//		Map<Entity, String> proteinAnnotation2entityLabel = new HashMap<Entity, String>();
//		Map<Pair, String> ppi2pairLabel = new HashMap<Pair, String>();
		
	    System.err.println("INFO: Processing document '" + d.getId() + "' (" + d.getOrigId() + ") ...");
		
	    ElementNode documentNode = toElementNode(d);

	    for (Sentence s : d.getSentences())
	    {
	    	Node sentenceNode = toXml(s);
			documentNode.addChild(sentenceNode);
	    }
		return documentNode;
	}
	
	

	/**
	 * Convenience method.
	 * 
	 * Creates an {@link AttributeNode} with given key and value if both are non-<code>null</code>. Returns <code>null</code> otherwise.
	 * 
	 * @param key
	 * @param value
	 * @return an Attribute node
	 * @throws NullPointerException iff key is <code>null</code>
	 */
	private static Node attribute(String key, String value) throws NullPointerException {
		if (key == null)
			throw new NullPointerException();
		if (value != null)
			return XmlBuilder.attribute(key, value);
		return null;
	}

//	private static String substring(TextProvider t, CharOffsetProvider e) {
//		SingleCharOffset sco = toSingle(e);
//		return t.getText().substring(sco.getStart(), sco.getEnd()+1);
//	}
	
	private static String charOffsetDescriptor(CharOffsetProvider e) {
		if (e.getCharOffset().getCharOffsets().length == 0)
			return null; // missing charoffset
		return 	toSingleCharOffset(e).toString();
	}
	
}
