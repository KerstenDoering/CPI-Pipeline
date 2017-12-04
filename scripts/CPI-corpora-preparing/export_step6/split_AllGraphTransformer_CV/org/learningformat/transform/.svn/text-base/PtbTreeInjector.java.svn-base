package org.learningformat.transform;

import jargs.gnu.CmdLineParser;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.Writer;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.regex.Pattern;

import javax.xml.parsers.ParserConfigurationException;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.TransformerFactoryConfigurationError;
import javax.xml.transform.sax.SAXSource;
import javax.xml.transform.stream.StreamResult;

import org.learningformat.api.CharOffset;
import org.learningformat.api.LearningFormatConstants;
import org.learningformat.api.Token;
import org.learningformat.impl.DefaultCharOffsetMapEntry;
import org.learningformat.impl.ErrorListener;
import org.learningformat.util.ArrayEnumerationFactory;
import org.learningformat.util.FileHelper;
import org.learningformat.xml.Elements;
import org.learningformat.xml.XmlConstants;
import org.xml.sax.Attributes;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;
import org.xml.sax.XMLFilter;
import org.xml.sax.XMLReader;
import org.xml.sax.helpers.AttributesImpl;
import org.xml.sax.helpers.XMLFilterImpl;

import edu.stanford.nlp.trees.TypedDependency;

public class PtbTreeInjector {
	
	protected static class BracketingInjectingFilter extends XMLFilterImpl {
	    
	    	
	    /**
	     * Whether to use document relative or sentence relative {@link Token} {@link CharOffset}s.
	     */
	    private final boolean documentRelativeTokenCharOffsets;

	    private boolean sentenceHasDesiredTokenization;
		private String sentenceBracketed;
		private String sentencePlain;
		private String sentenceLabel;
		private CharOffset sentenceCharOffset;
		private Set<String> sentenceTagsSeen = new HashSet<String>();
		private List<Token> sentenceTokens = new ArrayList<Token>();
		private final ErrorListener el = new ErrorListener();

		final String tokenizer;
		final String parser;

		private final PennTreeBankConverter ptbConverter = new PennTreeBankConverter();
		private final StanfordConverter stanfordConverter = new StanfordConverter(false);
		
		private final Map<String,String> ptbTrees;		
	    	
		public BracketingInjectingFilter(final XMLReader parent, final String tokenizer, final String parser, Map<String,String> ptbTrees) {
			super(parent);
			clearSentence();
			this.documentRelativeTokenCharOffsets = false;
			this.parser = parser;
			this.tokenizer = tokenizer;
			this.ptbTrees = ptbTrees;
			
		}
		
		
		@Override
		public void startElement(String uri, String localName, String name,
				Attributes atts) throws SAXException {
			
			super.startElement(uri, localName, name, atts);
			
			sentenceTagsSeen.add(name);
			
			if (Elements.sentence.equals(name)) {
			    clearSentence();
			    sentenceLabel = atts.getValue(org.learningformat.xml.Attributes.id);	    
			    sentencePlain = atts.getValue(org.learningformat.xml.Attributes.text);
			    if (sentencePlain == null)
			    	throw new RuntimeException("Tag <sentence> does not have a 'text' attribute, which should contain the original plain text of the sentence. (id='" + sentenceLabel +"')");
			    sentenceBracketed = ptbTrees.get(sentenceLabel);
				if (sentenceBracketed == null) {
					// if (fatal) throw new IllegalStateException("Parse for sentence '" + sentenceLabel + "' missing.");
					// else {
					System.err.println("WARNING: Parse for sentence '" + sentenceLabel + "' is missing (maybe due to a parser error?), skipping.");
					sentenceBracketed = ""; // pretend parse error
					// }
					
				}
				else if (sentenceBracketed.length() == 0)	{
					System.err.println("WARNING: Parse for sentence '" + sentenceLabel + "' is empty (maybe due to a parser error?), skipping.");
				}
			    
			    String charOffset = atts.getValue(org.learningformat.xml.Attributes.charOffset);
			    if (charOffset != null)
				sentenceCharOffset = new CharOffset(charOffset);
			    
			    
			}
			else if (Elements.sentenceanalyses.equals(name)) {
			    // if no sentenceanalyses tag exists, see #writeSentenceAnalyses()
			    writeBracketings();
			}
			else if (Elements.tokenization.equals(name)) {
				String tokenizerName = atts.getValue(org.learningformat.xml.Attributes.tokenizer);
				if (tokenizer.equals(tokenizerName))
				{
				    System.err.println("Found tokenization: " + tokenizerName  + " as " +  tokenizer);
				    sentenceHasDesiredTokenization = true;
				}
				else
				{
				    System.err.println("Ignoring tokenization: " + tokenizerName + " wanted " + tokenizer);
				}
			}
			else if (Elements.sentence.equals(name)) {
			    clearSentence();
			}
		}
		
		protected void clearSentence()
		{
			sentenceLabel = null;
		    sentenceHasDesiredTokenization = false;
		    sentenceBracketed = null;
		    sentencePlain = null;
		    sentenceCharOffset = null;
		    sentenceTagsSeen.clear();
		    sentenceTokens.clear();
		}
		
		
		
		@Override
		public void endElement(String uri, String localName, String name) throws SAXException {
		    
		    	if (Elements.tokenizations.equals(name) && !sentenceHasDesiredTokenization) {
		    	    writeTokenization();
		    	    sentenceHasDesiredTokenization = true;
		    	} 
		    	else if (Elements.sentenceanalyses.equals(name) && !sentenceHasDesiredTokenization) {
		    	    writeTokenizations();
		    	    sentenceHasDesiredTokenization = true;
		    	}
		    	else if (Elements.sentence.equals(name) && !sentenceHasDesiredTokenization)
		    	{
		    	    writeSentenceAnalyses();
		    	    sentenceHasDesiredTokenization = true;
		    	}
    		    
    		    
		    	super.endElement(uri, localName, name);
		}
		
		private void writeSentenceAnalyses() throws SAXException {
			super.startElement("", "", Elements.sentenceanalyses, new AttributesImpl());
			writeBracketings();
			writeDependencies();
			writeTokenizations();
			super.endElement("", "", Elements.sentenceanalyses);
		}

		private void writeBracketings() throws SAXException
		{
	    	if (sentenceBracketed == null)
	    	    throw new IllegalStateException("Sentence in ptb format should have been read at opening <sentence> tag.");
		    	
			super.startElement("", "", Elements.bracketings, null);
			{
        			AttributesImpl bracketingAttributes = new AttributesImpl();
        			bracketingAttributes.addAttribute(null, null, org.learningformat.xml.Attributes.tokenizer, XmlConstants.CDATA, tokenizer);
        			bracketingAttributes.addAttribute(null, null, org.learningformat.xml.Attributes.parser, XmlConstants.CDATA, parser);
        			bracketingAttributes.addAttribute(null, null, org.learningformat.xml.Attributes.bracketing, XmlConstants.CDATA, sentenceBracketed);
        			super.startElement(null, null, Elements.bracketing, bracketingAttributes);
        			super.endElement(null, null, Elements.bracketing);
			}
			super.endElement(null, null, Elements.bracketings);
		}

		private void writeDependencies() throws SAXException
		{
			super.startElement("", "", Elements.parses, null);
			writeDependency();
			super.endElement(null, null, Elements.parses);
		}

		/**
		 * <pre>
		 *   &lt;parse parser="Charniak-Lease" tokenizer="Charniak-Lease">
         *  	&lt;dependency id="clp_1" t1="clt_3" t2="clt_2" type="nn" />
         *  	&lt;dependency id="clp_2" t1="clt_37" t2="clt_3" type="prep_in" />
		 *</pre>
		 * @throws SAXException
		 */
		private void writeDependency() throws SAXException
		{
	    	if (sentenceBracketed == null)
	    	    throw new IllegalStateException("Sentence (in PTB format) should have been read from stand-off file at opening <sentence> tag.");
			else if (sentenceBracketed.length() == 0)	{
				System.err.println("WARNING: Parse for sentence '" + sentenceLabel + "' is empty (maybe due to a parser error?), skipping dependencies.");
				return;
			}

	    	List<TypedDependency> dependencies = stanfordConverter.convertPrbToDependencies(sentenceBracketed);
	    	
			AttributesImpl parseAttributes = new AttributesImpl();
			parseAttributes.addAttribute(null, null, org.learningformat.xml.Attributes.tokenizer, XmlConstants.CDATA, tokenizer);
			parseAttributes.addAttribute(null, null, org.learningformat.xml.Attributes.parser, XmlConstants.CDATA, parser);
	    	super.startElement(null, null, Elements.parse, parseAttributes);
	        // <dependency id="clp_2" t1="clt_37" t2="clt_3" type="prep_in" />
	    	for (int i = 0; i < dependencies.size(); i++) 
	    	{
    	    	TypedDependency dep = dependencies.get(i);
	    	    	
    			AttributesImpl depAttributes = new AttributesImpl();
    			depAttributes.addAttribute(null, null, org.learningformat.xml.Attributes.id, XmlConstants.CDATA, "d_" + (i+1));
    			depAttributes.addAttribute(null, null, org.learningformat.xml.Attributes.t1, XmlConstants.CDATA, "t_" + StanfordConverter.getTokenIndex(dep.gov()));
    			depAttributes.addAttribute(null, null, org.learningformat.xml.Attributes.t2, XmlConstants.CDATA, "t_" + StanfordConverter.getTokenIndex(dep.dep()));
    			depAttributes.addAttribute(null, null, org.learningformat.xml.Attributes.type, XmlConstants.CDATA, StanfordConverter.getDependencyType(dep));
    			depAttributes.addAttribute(null, null, org.learningformat.xml.Attributes.origId, XmlConstants.CDATA, dep.toString());
    			super.startElement(null, null, Elements.dependency, depAttributes);
    			super.endElement(null, null, Elements.dependency);
	    	}
		    	
			super.endElement(null, null, Elements.parse);
		}
		
		
		private void writeTokenizations() throws SAXException
		{
			super.startElement(null, null, Elements.tokenizations, null);
			writeTokenization();
			super.endElement(null, null, Elements.tokenizations);
		    
		}
		
		private void writeTokenization() throws SAXException
		{
	    	if (sentenceBracketed == null)
	    	    throw new IllegalStateException("Sentence (in PTB format) should have been read from stand-off file at opening <sentence> tag.");
	    	if (sentencePlain == null)
	    	    throw new IllegalStateException("Sentence (plain text) should have been read from XML attribute at opening <sentence> tag.");
	    	if (documentRelativeTokenCharOffsets && sentenceCharOffset == null)
	    	    throw new IllegalStateException("Sentence charOffset should have been read from XML attribute at opening <sentence> tag. (If no tokenization of the desired type is available in the XML, please provide a charOffset attribute for the sentence tag so that the alignment can use that.)");

			final AttributesImpl tokenizationAttributes = new AttributesImpl();
			tokenizationAttributes.addAttribute(null, null, org.learningformat.xml.Attributes.tokenizer, XmlConstants.CDATA, tokenizer);
//			tokenizationAttributes.addAttribute(null, null, org.learningformat.xml.Attributes.parser, XmlConstants.CDATA, parser);
	    	super.startElement(null, null, Elements.tokenization, tokenizationAttributes);
	    	
	    	List<Token> tokens; 
	    	try {
		    	tokens = ptbConverter.ptb2alignedTokens(
		    		sentenceBracketed,
		    		sentencePlain, 
		    		documentRelativeTokenCharOffsets
		    			? sentenceCharOffset.getCharOffsets()[0].getStart()
		    			: 0,
		    		sentenceTokens);
	    	} catch (IllegalStateException e) {
				el.error(e);
				tokens = null;
				System.err.println("INFO: skipping tokenization of sentence '" + sentenceLabel +"'");
			}
	    	if (tokens != null)
	    	{
		    	sentenceTokens = tokens;
		    	//<token POS="DT" charOffset="0-2" id="clt_1" text="The" />
		    	for (int i = 0; i < tokens.size(); i++) {
	    	    	Token token = tokens.get(i);
		    	    	
	    			AttributesImpl tokenAttributes = new AttributesImpl();
	    			tokenAttributes.addAttribute(null, null, org.learningformat.xml.Attributes.POS, XmlConstants.CDATA, token.getPos());
	    			tokenAttributes.addAttribute(null, null, org.learningformat.xml.Attributes.charOffset, XmlConstants.CDATA, token.getCharOffset().toString());
	    			tokenAttributes.addAttribute(null, null, org.learningformat.xml.Attributes.id, XmlConstants.CDATA, "t_" + (i+1));
	    			tokenAttributes.addAttribute(null, null, org.learningformat.xml.Attributes.text, XmlConstants.CDATA, token.getText());
	    			super.startElement(null, null, Elements.token, tokenAttributes);
	    			super.endElement(null, null, Elements.token);
				}
	    	}
		    	
			super.endElement(null, null, Elements.tokenization);
			
		}		
	}
	
	protected static class CharOffsetMappingInjectingFilter extends XMLFilterImpl {
	
		public CharOffsetMappingInjectingFilter(XMLReader parent, BufferedReader mappingReader) {
			super(parent);
			this.mappingReader = mappingReader;
		}
		
		private String lastSentenceId;
		private final BufferedReader mappingReader;
		
		private static final Pattern mappingLineDelimiter =  Pattern.compile("[" + CharOffset.COMMA + DefaultCharOffsetMapEntry.COLON + "]");
		
	
		@Override
		public void startElement(String uri, String localName, String name,
				Attributes atts) throws SAXException {
			
			super.startElement(uri, localName, name, atts);
			
			if (Elements.sentence.equals(name)) {
				lastSentenceId = atts.getValue(org.learningformat.xml.Attributes.id);
			}
			else if (Elements.bracketing.equals(name)) {
				try {
					String mappingLine = mappingReader.readLine();
					if (mappingLine == null) {
						throw new IllegalStateException("Premature end of file.");
					}
					Enumeration<String> st =  ArrayEnumerationFactory.makeEnumeration(mappingLineDelimiter.split(mappingLine));
					
					String sentId = st.nextElement();
					
					if (!sentId.equals(lastSentenceId)) {
						throw new IllegalStateException("Unexpected sentence id '"+ sentId +"' expected '"+ lastSentenceId +"'");
					}
					
					while (st.hasMoreElements()) {
						String sentenceTextCharOffset = st.nextElement();
						if (!st.hasMoreElements())
							throw new IllegalStateException("Unexpected number of tokens in line '" + mappingLine + "'");
						String bracketingCharOffset = st.nextElement();
						AttributesImpl bracketingAttributes = new AttributesImpl();
						bracketingAttributes.addAttribute(null, null, org.learningformat.xml.Attributes.sentenceTextCharOffset, XmlConstants.CDATA, sentenceTextCharOffset);
						bracketingAttributes.addAttribute(null, null, org.learningformat.xml.Attributes.bracketingCharOffset, XmlConstants.CDATA, bracketingCharOffset);
						super.startElement(null, null, Elements.charOffsetMapEntry, bracketingAttributes);
						super.endElement(null, null, Elements.charOffsetMapEntry);
					}
				}
				catch (IOException e) {
					throw new RuntimeException("Error reading mappings", e);
				}
			}
		}		
	}
	
	private static String inFile, outFile, parseFile, tokenFile;
	//boolean inject;
	private static boolean injectTrees ;
	private static boolean stopOnError;

	
	private static void printUsage() {
        System.err.println(
        		"Usage:\n" +
        		"InputFile [-f,--file] InjectTree [-i,--inject] OutputFile [-o,--out]\n" + 
        		"Optional: ParseFile [-p,--parse] TokenFile [-t,--token] StopOnError [--fatal]" + 
        		"Default value of <ParseFile>: charniak-johnson/<InputFile>-ptb-s.txt-parsed.txt" +  
        		"Default value of <TokenFile>: <InputFile>-bracketing-tokens.txt" );
        		    }
	
	private static void parseArgs(String args[]){
		CmdLineParser parser = new CmdLineParser();
		
		CmdLineParser.Option inFileOption  = parser.addStringOption('f', "file");
		CmdLineParser.Option injectOption  = parser.addBooleanOption('i', "inject");
		CmdLineParser.Option outFileOption = parser.addStringOption('o',"out");
		CmdLineParser.Option parseFileOption = parser.addStringOption('p',"parse");
		CmdLineParser.Option tokenFileOption = parser.addStringOption('t',"token");
		CmdLineParser.Option fatalOption = parser.addBooleanOption("fatal");
		try {
            parser.parse(args);
        }
        catch ( CmdLineParser.OptionException e ) {
            printUsage();
            System.exit(2);
        }

        inFile = (String)   parser.getOptionValue(inFileOption);
        injectTrees = (Boolean) parser.getOptionValue(injectOption, Boolean.FALSE);
        outFile = (String)  parser.getOptionValue(outFileOption);
        parseFile = (String)  parser.getOptionValue(parseFileOption);
        tokenFile = (String)  parser.getOptionValue(tokenFileOption);
        stopOnError = (Boolean) parser.getOptionValue(fatalOption, Boolean.FALSE);
        
        if(inFile==null || outFile==null){
        	printUsage();
            System.exit(2);
        }
        if(inFile.equals(outFile)){
        	System.err.println("The input and the output files should be different");
            System.exit(2);
        }
        if(outFile.equals(parseFile)&& injectTrees){
        	System.err.println("The parse and the output files should be different");
            System.exit(2);
        }
        if(outFile.equals(tokenFile)&& !injectTrees){
        	System.err.println("The token and the output files should be different");
            System.exit(2);
        }
    }

	public static void main(String[] args) {
		
		BufferedReader corpusReader = null;
		BufferedReader ptbTreeReader = null;
		Writer out = null;
		Charset encoding = Charset.forName("UTF-8");
		
		try {
//			for (int i = 0; i < args.length; i++) {
				
			parseArgs(args);
			
			final File in = new File(inFile); 
			corpusReader = FileHelper.getBufferedFileReader(in, encoding);
			
			File inject = null;
			if (injectTrees) {
				if ( parseFile == null || parseFile.isEmpty())
					inject = new File(in.getParent() + File.separator + "charniak-johnson"+ File.separator +in.getName() + "-ptb-s.txt-parsed.txt");
				else
					inject = new File(parseFile);
			} else {
				if ( tokenFile == null || tokenFile.isEmpty())
					inject = new File(in.getAbsolutePath() + "-bracketing-tokens.txt");
				else
					inject = new File(tokenFile);
			}
			ptbTreeReader = FileHelper.getBufferedFileReader(inject, encoding);
			out = FileHelper.getBufferedFileWriter(new File(outFile), encoding);
			
			new PtbTreeInjector(corpusReader, ptbTreeReader, out, stopOnError);
				
//			}
			System.exit(0);
		} catch (Exception e) {
			e.printStackTrace();
		}
		finally {
			if (corpusReader != null) {
				try {
					corpusReader.close();
				} catch (IOException e) {
				}
			}
			if (ptbTreeReader != null) {
				try {
					ptbTreeReader.close();
				} catch (IOException e) {
				}
			}
			if (out != null) {
				try {
					out.close();
				} catch (IOException e) {
				}
			}
		}
		System.exit(1);	
	}
	
	protected Writer out;
	
	
	
	public PtbTreeInjector(BufferedReader corpusReader, BufferedReader auxReader, Writer out, boolean fatal) throws TransformerFactoryConfigurationError, TransformerException, ParserConfigurationException, SAXException, IOException {
		super();
		this.out = out;
		SAXParser parser = SAXParserFactory.newInstance().newSAXParser();
		
		XMLReader xmlReader = parser.getXMLReader();
		
		XMLFilter filter = null;
		if (injectTrees) {
			filter = new BracketingInjectingFilter(xmlReader,
					LearningFormatConstants.CHARNIAK_LEASE_TOKENIZER,
					LearningFormatConstants.CHARNIAK_JOHNSON_MCCLOSKY_PARSER,
					parserOutputReaderToMap(auxReader));
			((BracketingInjectingFilter) filter).el.setStopOnError(fatal);
		}
		else {
			filter = new CharOffsetMappingInjectingFilter(xmlReader, auxReader);
			//((CharOffsetMappingInjectingFilter) filter).el.setStopOnError(fatal);
		}
		
		SAXSource src = new SAXSource(filter, new InputSource(corpusReader));
		StreamResult rslt = new StreamResult(out);
		
		Transformer t = TransformerFactory.newInstance().newTransformer();
		t.setOutputProperty(OutputKeys.OMIT_XML_DECLARATION, "yes");
 		t.setOutputProperty(OutputKeys.INDENT, "yes");
 		t.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "2");

		
		
		t.transform(src, rslt);
		
	}
	
	static Map<String, String> parserOutputReaderToMap(BufferedReader ptbTreeReader) throws IOException
	{
		Map<String, String> map = new HashMap<String, String>(100);
		Pattern sep = Pattern.compile("\t");
		String line;
		for (int lineNo = 1; (line = ptbTreeReader.readLine()) != null; lineNo++)
		{
			String[] fields = sep.split(line);
			if (fields.length != 2)
				System.err.println("WARNING: Suspicious line " + lineNo + " '" + line +"'");
			final String id;
			final String parse;			
			if (fields.length == 1)
			{
				id = fields[0];
				parse = "";
			}
			else if (fields.length == 2)
			{
				id = fields[0];
				parse = fields[1];
			}
			else
			{
				throw new IllegalStateException("Unrecognized line " + lineNo + " '" + line +"'");				
			}
			
			if (map.put(id, parse) != null)
				throw new IllegalStateException("Duplicate senetence identifier '" + id +"' on line " + lineNo + " '" + line +"'");
		}
		return map;
	}
}
