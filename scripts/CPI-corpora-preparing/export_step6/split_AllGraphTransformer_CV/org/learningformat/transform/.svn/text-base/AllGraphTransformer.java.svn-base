package org.learningformat.transform;


import jargs.gnu.CmdLineParser;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.StringWriter;
import java.nio.charset.Charset;
import java.util.HashMap;
import java.util.Map;
import java.util.zip.GZIPInputStream;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerConfigurationException;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.TransformerFactoryConfigurationError;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;

import org.learningformat.util.FileHelper;
import org.learningformat.xml.Elements;
import org.w3c.dom.Document;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;
import org.xml.sax.SAXParseException;


public class AllGraphTransformer
{

	static int desiredFoldsCount = 10;
    static Document[] testSplits  = new Document[desiredFoldsCount];
    static Document[] trainSplits = new Document[desiredFoldsCount];
       
	static DocumentBuilder builder;
	static Document inputDoc;
	static String corpusName;
	
	static File inFile,baseDir,splitLocation;
	
	public static void main( String[] argv ){
		Charset splitEncoding = Charset.forName("UTF-8");
		parseArgs(argv);
		
		corpusName = extractCorpusName (inFile.getName());
			
		System.err.println("Processing corpus '" + corpusName +"'");
		
		try {
			
			final Map<String, Integer> folds = readFolds(splitLocation, splitEncoding);
			
			builder = DocumentBuilderFactory.newInstance().newDocumentBuilder();
						
			if(inFile.getName().endsWith(".gz"))
				inputDoc= builder.parse(new GZIPInputStream(new FileInputStream(inFile)));
			else
				inputDoc = builder.parse(inFile);
				
			initXMLDocuments();
		
			//Iterate over all nodes with tag <Document>
			NodeList documents = inputDoc.getElementsByTagName(Elements.document);		
			for (int i = 0; i < documents.getLength(); i++) {
				final Node doc = documents.item(i);
				final int testSplit = folds.get(doc.getAttributes().getNamedItem("id").getNodeValue());
//					System.out.println(split);

				//Read the node and save it into the 
				appendImportChild(testSplits[testSplit], doc, true);
				
				for (int trainSplit = 0; trainSplit < desiredFoldsCount; trainSplit++) {
					//Append the files only when 
					if (trainSplit != testSplit) {
						appendImportChild(trainSplits[trainSplit], doc, true);
					}
				}
			}
		}
		catch( SAXParseException spe ) {
			System.err.println( "\n** Parsing error, line " + spe.getLineNumber() + ", uri "  + spe.getSystemId() );
			System.err.println( "   " + spe.getMessage() );
			Exception e = ( spe.getException() != null ) ? spe.getException() : spe;
			e.printStackTrace();
		}
		catch( SAXException sxe ) {
			Exception e = ( sxe.getException() != null ) ? sxe.getException() : sxe;
			e.printStackTrace();
		}
		catch( ParserConfigurationException pce ) {
			pce.printStackTrace();
		} 
		catch( IOException ioe ) {
			ioe.printStackTrace();
		}
		
		saveXMLDocuments();
		System.out.println("Parsed and stored " +corpusName);
	}
	
	/**
	 * Import a node and add it to document element as a child node.
	 * @param root
	 * @param child
	 * @param deep
	 * @return
	 */
	private static Node appendImportChild(Document root, Node child, boolean deep)
	{
		return root.getDocumentElement().appendChild(root.importNode(child, deep));		
	}

	/**
	 * Import a node and add it to document element as a child node.
	 * @param root
	 * @param child
	 * @param deep
	 * @return
	 */
	private static Node appendImportDocumentElement(Document root, Node docElement, boolean deep)
	{
		return root.appendChild(root.importNode(docElement, deep));		
	}

	/**
	 * Initializes the XML-Documents on which everything is written
	 */
	private static void initXMLDocuments(){

		final Node rootNode = inputDoc.getDocumentElement();

		//Initialize the outputTestDocumentss
		for (int i=0; i< desiredFoldsCount;i++){
			//Initialize each Document with the root Node of inputDoc
			appendImportDocumentElement((testSplits[i] = builder.newDocument()), rootNode, false);
		}

		//Initialize the output Train documents
		for (int i=0; i< desiredFoldsCount;i++){
			//Initialize each Document with the root Node of inputDoc
			appendImportDocumentElement((trainSplits[i] = builder.newDocument()), rootNode, false);
		}
	}

	@SuppressWarnings ("unused")
	private static String toXMLString(Document d) {
		if (d== null)
			throw new NullPointerException();
		
		StringWriter sw = new StringWriter();
		try {
			Transformer transformer = TransformerFactory.newInstance().newTransformer();
			transformer.transform(new DOMSource(d), new StreamResult(sw));
		}
		catch (TransformerException e) {
		}
		catch (TransformerFactoryConfigurationError e) {
		}
		
		return sw.toString();
	}
	
	private static void saveXMLDocuments(){
		try{
			File outFile=new File(baseDir+File.separator+ corpusName + File.separator);
			outFile.mkdirs();
			Transformer transformer = TransformerFactory.newInstance().newTransformer();
			for (int i=0; i< desiredFoldsCount;i++){
				String file= outFile.getPath() +File.separator +"test" +i +".txt";
				transformer.transform(new DOMSource(testSplits[i]), new StreamResult(new FileWriter(file)));
//				transformer.transform(new DOMSource(outputDocTest[i]), new StreamResult(new OutputStreamWriter(new GZIPOutputStream(new FileOutputStream(new File(file))))));
				
				file= outFile.getPath() +File.separator +"train" +i +".txt";
				transformer.transform(new DOMSource(trainSplits[i]), new StreamResult(new FileWriter(file)));
//				transformer.transform(new DOMSource(outputDocTest[i]), new StreamResult(new OutputStreamWriter(new GZIPOutputStream(new FileOutputStream(new File(file))))));
				}
			}
		
			catch( TransformerConfigurationException tce ) {
				System.err.println( "\n** Transformer Factory error" );
				System.err.println( "   " + tce.getMessage() );
				Throwable e = ( tce.getException() != null ) ? tce.getException() : tce;
				e.printStackTrace();
			} catch( TransformerException tfe ) {
				System.err.println( "\n** Transformation error" );
				System.err.println( "   " + tfe.getMessage() );
				Throwable e = ( tfe.getException() != null ) ? tfe.getException() : tfe;
				e.printStackTrace();
			}
			catch(IOException ioe){
				System.err.println("IO-Exception occured");
				ioe.printStackTrace();
			}
		
	}
	
	/**
	 * Extracts the corpusName from the XML-Filename
	 * @param corpusName XML-File
	 * @return
	 */
	private static String extractCorpusName(String corpusName){
//		String corpusName = inputFile.getName();
		if (false && corpusName.indexOf('-') != -1)
			corpusName = corpusName.substring(0, corpusName.indexOf('-'));
		else 
		{ 
			if ( corpusName.indexOf('.') != -1)
				corpusName = corpusName.substring(0, corpusName.indexOf('.'));
		}	
		return corpusName;
	}

	
	/**
	 * Reads the Splits of a certain corpus (defined in variable corpusName)
	 * @param splitLocation Location of the defined splits
	 * @return
	 * @throws IOException
	 */
	private static Map<String, Integer> readFolds(File foldsRoot, Charset encoding) throws IOException {
		
		Map<String, Integer> result = new HashMap<String, Integer>();
//		corpusName= extractCorpusName(corpusName);
		
		if (("BioInferM".equals(corpusName))||("BioInferCLAnalysis_split_SMBM_version".equals(corpusName))) {
			corpusName = "BioInfer";
		}
		if (("AImedM".equals(corpusName))|| ("AImedprob".equals(corpusName))) {
			corpusName = "AImed";
		}
		final File foldsDir = new File(foldsRoot, corpusName);

		for (int i = 0; i < desiredFoldsCount; i++) {
			final File foldFile = new File( foldsDir, "test-" + (i + 1));
			final BufferedReader r = FileHelper.getBufferedFileReader(foldFile, encoding);
			
			String line = null;
			final Integer I = i;
			while ((line = r.readLine()) != null) {
				final String docid = line.substring(line.indexOf(' ') + 1).trim();
				result.put(docid, I);
			}
		}
		
//		for(Iterator<String> key=result.keySet().iterator(); key.hasNext();){
//			String k= key.next();
//			System.out.println(k+"\t" +result.get(k));
//		}
		
		
		return result;
	}
	
	private static void printUsage() {
        System.err.println(
        		"Usage:\n" +
        		"InputFile [-f,--file] OutputDir [-o,--out]\n" +
        		"Directory of splits [-s,--split]\n");
        		    
	}

	
	private static void parseArgs(String args[]){
		CmdLineParser parser = new CmdLineParser();
		
		CmdLineParser.Option inFileOption  = parser.addStringOption('f', "file");
		CmdLineParser.Option outBaseDirOption = parser.addStringOption('o',"out");
		CmdLineParser.Option splitOption = parser.addStringOption('s', "split");
		
		try {
	        parser.parse(args);
	    }
	    catch ( CmdLineParser.OptionException e ) {
	        printUsage();
	        System.exit(2);
	    }

	    try {
		    inFile = new File((String) parser.getOptionValue(inFileOption));
		    baseDir = new File((String) parser.getOptionValue(outBaseDirOption));
		    splitLocation = new File((String) parser.getOptionValue(splitOption));
	    } 
	    catch (NullPointerException e) {
	    	printUsage();
	        System.exit(2);
	    }
	}
}

