package org.learningformat.transform.dependency;

import jargs.gnu.CmdLineParser;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.Writer;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;

import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Source;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.TransformerFactoryConfigurationError;
import javax.xml.transform.stream.StreamResult;
import javax.xml.transform.stream.StreamSource;

import org.apache.commons.configuration.ConfigurationException;
import org.apache.commons.configuration.XMLConfiguration;
import org.jgrapht.DirectedGraph;
import org.learningformat.api.Corpus;
import org.learningformat.api.Dependency;
import org.learningformat.api.Document;
import org.learningformat.api.LearningFormatConstants;
import org.learningformat.api.Parse;
import org.learningformat.api.Sentence;
import org.learningformat.api.Token;
import org.learningformat.api.Tokenization;
import org.learningformat.transform.dependency.DependencyGraph.DependencyData;
import org.learningformat.transform.dependency.transformer.CDTransformer;
import org.learningformat.transform.dependency.transformer.ConjTransformer;
import org.learningformat.transform.dependency.transformer.DependencyGraphTransformer;
import org.learningformat.transform.dependency.transformer.IdentityTransformer;
import org.learningformat.transform.dependency.transformer.UDTransformer;
import org.learningformat.util.FileHelper;
import org.learningformat.xml.CorpusListener;
import org.learningformat.xml.Elements;
import org.learningformat.xml.XmlConstants;
import org.xml.sax.Attributes;
import org.xml.sax.SAXException;
import org.xml.sax.XMLFilter;
import org.xml.sax.helpers.AttributesImpl;

public class TransformedDependencyInjector extends org.learningformat.xml.Parser {
	
	private static String inFile, outFile;
	private static String sourceDepParser;
	private static String sourceTokenizer;
	private static String xsltFile="/home/philippe/workspace/ppi-benchmark/Converters/XML/merge-parses.xsl";	//TODO: Read later dynamically
	private static DependencyGraphTransformer transformation;
	/** 
	 * GraphViz output directory. No output is produced if <code>null</code>
	 */
	private static String dotDir;
	
	
	private static boolean hasTokenization(Sentence s, String tokenizer)
	{
    	boolean hasTokenization = false;
    	if (s.getTokenizations() == null || s.getTokenizations().size() == 0)
    	{
		    System.err.println("ERROR: Found no tokenizations");
		    return false;
    	}
		for (Tokenization tokenization : s.getTokenizations())
		{
			if (tokenizer.equals(tokenization.getTokenizer()))
			{
			    System.err.println("INFO: Found tokenization: " + tokenization.getTokenizer()  + " as " +  tokenizer);
			    hasTokenization = true;
			}
			else
			    System.err.println("WARNING: Ignoring tokenization: " + tokenization.getTokenizer() + " wanted " + tokenizer);
		}
		return hasTokenization;
	}
	
	private static boolean hasDepParse(Sentence s, String depParser)
	{
    	boolean hasDepParse = false;
    	if (s.getParses() == null || s.getParses().size() == 0)
    	{
		    System.err.println("ERROR: Found no parses");
		    return false;
    	}    	
    	for ( Parse depParse : s.getParses())
		{
			if (depParser.equals(depParse.getParser()))
			{
			    System.err.println("INFO: Found dep parse: " + depParse.getParser()  + " as " +  depParser);
			    hasDepParse = true;
			}
			else
			    System.err.println("INFO: Ignoring dep parse: " + depParse.getParser() + " wanted " + depParser);
		}
		if (!hasDepParse)
		{
			StringBuilder sb = new StringBuilder();
			for ( Parse depParse : s.getParses())
				sb.append(",").append(depParse.getParser());
			System.err.println("ERROR: Found no parse '" + depParser +"' (available: " + sb.toString() +")");
		}
		return hasDepParse;
	}
	
	protected class DependencyInjectingFilter extends LearningFormatHandler {
		
		@Override
		public void endElement(String uri, String localName, String name) throws SAXException {
	    	super.endElement(uri, localName, name);
			
			if (Elements.sentenceanalyses.equals(name)) {
														
				if (getCurrentSentence() == null) {
					System.err.println("ERROR: no sentence");
				}
				else if (hasTokenization(getCurrentSentence(), TransformedDependencyInjector.sourceTokenizer) 
						&& hasDepParse(getCurrentSentence(), TransformedDependencyInjector.sourceDepParser))
		    	{
					System.err.println("INFO: sentence " + getCurrentSentence().getId() + " (" + getCurrentSentence().getOrigId()+")");
					final Tokenization tokenization = getCurrentSentence().getTokenization(TransformedDependencyInjector.sourceTokenizer); 
					final Parse parse = getCurrentSentence().getParse(TransformedDependencyInjector.sourceDepParser);

					if (parse == null)
						throw new NullPointerException();
				
					if (tokenization == null)
						throw new NullPointerException();

					// create graph
			    	DependencyGraph dg = new DependencyGraph(TransformedDependencyInjector.sourceDepParser);
			    	DirectedGraph<Token, DependencyData> g = dg.getGraph();
				
			    	// initialize graph
			    	for (Token token : tokenization.getTokens())
			    		g.addVertex(token);
					if (parse.getDependencies() != null)
				    	for (Dependency dep : parse.getDependencies())
				    		g.addEdge(
				    				tokenization.getToken(dep.getT1().getId()), 
				    				tokenization.getToken(dep.getT2().getId()),
			    					new DependencyData(dep));
			    	
			    	// transform
			    	DependencyGraph transformed = transformation.transform(dg);

			    	
			    	// make sure it has a (unique) name
			    	if (sourceDepParser.equals(transformed.getName()) || transformed.getName() == null)
			    		throw new IllegalStateException("parser name not set by " + transformation.getClass().getCanonicalName());
			    	
			    	// add the source graph's parser attribute
			    	transformed.setName(transformed.getName() + ":" + sourceDepParser);
			    	
			    	// write
			    	writeDependencies(Collections.<DependencyGraph>singleton(transformed));
			    	
			    	// produce GraphViz output
					if (dotDir != null)
					{
							System.out.println("Yes");
						File dotFile = new File(new File(dotDir), coalesce(getCurrentSentence().getOrigId(), getCurrentSentence().getId())+".dot");
						if (dotFile.exists())
							System.err.println("WARNING: Overwriting DOT file '" + dotFile.getAbsolutePath() + "'");
						
						Writer dotWriter = null;
						try {
							dotWriter = FileHelper.getBufferedFileWriter(dotFile, Charset.forName("UTF-8"));
							GraphVizWriter.writeDot(dg, dotWriter);
						} catch (IOException e) {
							System.err.println("ERROR: writing DOT file '" + dotFile.getAbsolutePath() + "': " + e.getMessage());
						}
						finally
						{
							try {
								if (dotWriter != null)
									dotWriter.close();
							} catch (IOException e) {
								e.printStackTrace();
							}
						}
					}
		    	}
				else {
					hasTokenization(getCurrentSentence(), TransformedDependencyInjector.sourceTokenizer);
					 
					hasDepParse(getCurrentSentence(), TransformedDependencyInjector.sourceDepParser);					
				}
			}
	    	emitEndElement(uri, localName, name);
		}
		
		@Override
		public void startElement(String uri, String localName, String name,
				Attributes attributes) throws SAXException {
			super.startElement(uri, localName, name, attributes);
			emitStartElement(uri, localName, name, attributes);
		}
		
		private void writeDependencies(Collection<DependencyGraph> dgs) throws SAXException
		{
			emitStartElement("", "", Elements.parses, null);
			for(DependencyGraph dg : dgs)
				writeDependency(dg);
			emitEndElement("", "", Elements.parses);
		}

		/**
		 * <pre>
		 *   &lt;parse parser="Charniak-Lease" tokenizer="Charniak-Lease">
         *  	&lt;dependency id="clp_1" t1="clt_3" t2="clt_2" type="nn" />
         *  	&lt;dependency id="clp_2" t1="clt_37" t2="clt_3" type="prep_in" />
		 *</pre>
		 * @throws SAXException
		 */
		private void writeDependency(DependencyGraph dg) throws SAXException
		{
	    	// output
			AttributesImpl parseAttributes = new AttributesImpl();
			parseAttributes.addAttribute(null, null, org.learningformat.xml.Attributes.tokenizer, XmlConstants.CDATA, TransformedDependencyInjector.sourceTokenizer);
			parseAttributes.addAttribute(null, null, org.learningformat.xml.Attributes.parser, XmlConstants.CDATA, dg.getName());
	    	emitStartElement(null, null, Elements.parse, parseAttributes);
	    	int i = 0;
	    	for (DependencyData dep : dg.getGraph().edgeSet())
	    	{
	    		i++;
		        // <dependency id="clp_2" t1="clt_37" t2="clt_3" type="prep_in" />
    			AttributesImpl depAttributes = new AttributesImpl();
    			depAttributes.addAttribute(null, null, org.learningformat.xml.Attributes.id, XmlConstants.CDATA, "d_" + (i));
    			depAttributes.addAttribute(null, null, org.learningformat.xml.Attributes.t1, XmlConstants.CDATA, dg.getGraph().getEdgeSource(dep).getId());
    			depAttributes.addAttribute(null, null, org.learningformat.xml.Attributes.t2, XmlConstants.CDATA, dg.getGraph().getEdgeTarget(dep).getId());
    			depAttributes.addAttribute(null, null, org.learningformat.xml.Attributes.type, XmlConstants.CDATA, dep.getType());
    			depAttributes.addAttribute(null, null, org.learningformat.xml.Attributes.origId, XmlConstants.CDATA, dep.getId());
    			emitStartElement(null, null, Elements.dependency, depAttributes);
    			emitEndElement(null, null, Elements.dependency);
	    	}
			emitEndElement(null, null, Elements.parse);
		}
	}
	
	public static <T> T coalesce(T a, T b) {
	    return a == null ? b : a;
	}
	

	
	private static void printUsage() {
        System.err.println(
        		"Usage:\n" +
        		"InputFile [-f,--file] (mandatory)\n" +
        		"OutputFile [-o,--out]\n" + 
        		"Tokenizer [-t, --tokenizer] (default: '"+LearningFormatConstants.CHARNIAK_LEASE_TOKENIZER+ "')\n" +
        		"Parser [-p,--parser]  (default: '" + LearningFormatConstants.CHARNIAK_LEASE_PARSER + "')\n" + 
        		"Produce GraphViz .dot files into directory [-d,--dot-dir]\n" 
        		);
        		    }
	
	private static void parseArgs(String args[]){
		CmdLineParser parser = new CmdLineParser();
		
		CmdLineParser.Option inFileOption  = parser.addStringOption('f', "file");
		CmdLineParser.Option outFileOption = parser.addStringOption('o',"out");
		CmdLineParser.Option parserOption = parser.addStringOption('p', "parser");
		CmdLineParser.Option tokenizerOption = parser.addStringOption('t', "tokenizer");
		CmdLineParser.Option dotDirOption = parser.addStringOption('d', "dot-dir");
		CmdLineParser.Option propertyFileOption = parser.addStringOption('y', "property");
		
		try {
            parser.parse(args);
        }
        catch ( CmdLineParser.OptionException e ) {
        	System.err.println("ERROR: " + e.getMessage());
            printUsage();
            System.exit(2);
        }

        inFile    = (String) parser.getOptionValue(inFileOption);
        outFile   = (String) parser.getOptionValue(outFileOption);
	    sourceDepParser = (String) parser.getOptionValue(parserOption, LearningFormatConstants.CHARNIAK_LEASE_PARSER);
	    sourceTokenizer = (String) parser.getOptionValue(tokenizerOption, LearningFormatConstants.CHARNIAK_LEASE_TOKENIZER);
	    dotDir  = (String) parser.getOptionValue(dotDirOption);
//	    String propertyFile = (String) parser.getOptionValue(propertyFileOption);
        
	    
//	    try {
//			XMLConfiguration config = new XMLConfiguration("/home/philippe/workspace/learning-format-api/test.xml");
//			
//			List<String> generalizers=config.getList("generalizer.name");
//			for(String generalizer:generalizers)
//				System.out.println(generalizer);
//			
//			System.out.println(config.getString("UD.description"));
//			List<String> list=config.getList("UD.type");
//			for(String l:list){
//				System.out.println(l);
//			}
//
//			
//		} catch (ConfigurationException e) {
//			// TODO Auto-generated catch block
//			e.printStackTrace();
//		}
//
//		System.exit(1);
	    
	    
	    // TODO: add some sensical tranfo here
//	    transformation = new IdentityTransformer();
//	    transformation = new CDTransformer();
	    transformation = new ConjTransformer();
//	    transformation = new ChainedTransformer(new ConjTransformer(), new ConjTransformer(), new IdentityTransformer());
//	    transformation = new EdgeRemoverTransformer();	//Demo Remover
	    
        if(inFile == null){
        	System.err.println("ERROR: No input file [-f, --file] provided");
        	printUsage();
            System.exit(2);
        }
        
        if(inFile.equals(outFile)){
        	System.err.println("ERROR: The input and the output files should be different");
            System.exit(2);
        }
        
        if (dotDir != null)
        {
        	File dir = new File(dotDir);
        	if (!(dir.exists() && dir.isDirectory()))
        	{
        		System.err.println("INFO: creating DOT directory '" + dir.getAbsolutePath() +"'" );
        		dir.mkdir();
        	}
        }
    }

	public static void main(String[] args) {
		boolean error=false;
		
		//Some test by me
	    List<DependencyGraphTransformer> transformations = new ArrayList<DependencyGraphTransformer>();
	    transformations.add(new IdentityTransformer());
	    transformations.add(new ConjTransformer());
	    transformations.add(new CDTransformer(true, false));
	    transformations.add(new CDTransformer(false, true));
	    transformations.add(new CDTransformer(true, true));
	    transformations.add(new UDTransformer(true, false, false, false));
	    transformations.add(new UDTransformer(false, true, false, false));
	    transformations.add(new UDTransformer(false, false, true, false));
	    transformations.add(new UDTransformer(false, false, false, true));
		
	    InputStream in = null;
		OutputStream out = null;
	    try{
	    	parseArgs(args);
	    	
		    File tem = File.createTempFile("transformer", ".xml");
	        tem.deleteOnExit();
	        copy(new File(inFile), tem);
	        
	        for(DependencyGraphTransformer dgt : transformations){
		    	transformation = dgt;	//Set transformer
		    	
		    	in = new FileInputStream(tem);	
		    	TransformedDependencyInjector t = new TransformedDependencyInjector();
		    	System.out.println("transformation");
		    	if (outFile != null)	
					t.process(in, new File(outFile));//Do the transformation
				else 
					t.process(in);//Do the transformation
		    	
		    	//Finally we have to perform some XSLT transformation, because the new trees are in the wrong folder
		    	Source xmlSource = new StreamSource(outFile);
		        Source xsltSource = new StreamSource(xsltFile);
		        TransformerFactory transFact = TransformerFactory.newInstance();
		        Transformer trans = transFact.newTransformer(xsltSource);
		        trans.setOutputProperty(OutputKeys.METHOD, "xml"); 
		        trans.setOutputProperty(OutputKeys.INDENT, "yes"); 
		        trans.setOutputProperty(OutputKeys.OMIT_XML_DECLARATION, "no"); 
		        trans.setOutputProperty("indent", "2");
		        System.out.println("Copying");
		        trans.transform(xmlSource, new StreamResult(new FileOutputStream(tem)));
	        }
	        
	        copy(tem, new File(outFile));
	    	
	    }catch(Exception e){
	    	e.printStackTrace();
	    	error = true;
	    }
	    finally {
			if (in != null) {
				try {
					in.close();
				} catch (IOException e) {
					e.printStackTrace();
					error = true;
				}
			}
			if (out != null) {
				try {
					out.close();
				} catch (IOException e) {
					e.printStackTrace();
					error = true;
				}
			}
		}
	    

		if (error){
			System.err.println("ERROR processing '" + inFile +"'");
			System.exit(1);
		}
	
		
	}
	
	private static void copy(File from, File to) throws IOException{
        //Copy content manually, as temp.renameTo(dest) lead to problems
        FileReader inT = new FileReader(from);
        FileWriter outT = new FileWriter(to);
        int c;

        while ((c = inT.read()) != -1){	
        	outT.write(c);
        }

        inT.close();
        outT.close(); 
	}
	
	protected BufferedReader ptbTreeReader;
	
	@Override
	protected XMLFilter createHandler() {
		return new DependencyInjectingFilter();
	}
	
	public TransformedDependencyInjector() 
	throws TransformerFactoryConfigurationError, TransformerException, ParserConfigurationException, SAXException 
	{
		super(new CorpusListener() {
			int docCounter = 0;
			
			@Override
			public void startDocument(Document document) {
				++docCounter;
				System.err.println("INFO: Processing document #" + docCounter + ": '" + document.getOrigId() +"' (" + document.getId() +")");
			}
			
			@Override
			public void startCorpus(Corpus corpus) {
			}
			
			@Override
			public void processSentence(Sentence sentence) {
			}
			
			@Override
			public void endDocument() {
			}
			
			@Override
			public void endCorpus() {
			}
		});
	}
}
