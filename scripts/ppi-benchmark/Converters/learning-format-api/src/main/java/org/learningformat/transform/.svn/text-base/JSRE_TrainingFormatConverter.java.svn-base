package org.learningformat.transform;

import jargs.gnu.CmdLineParser;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

@Deprecated
public class JSRE_TrainingFormatConverter {

	static String outDir="/home/philippe/Desktop/svm/corpus/out/";
	static String filename="/home/philippe/Desktop/svm/corpus/LLL-learning-format.xml";
	static String tokenizer="split";

	
	
	public static void main(String[] args) throws ParserConfigurationException, SAXException, IOException {
		parseArgs(args);
		DocumentBuilder builder = DocumentBuilderFactory.newInstance().newDocumentBuilder();
		Document inputDoc = builder.parse(new File(filename));
		outDir+=tokenizer;
//		System.out.println(outDir);
		new File(outDir).mkdirs();
		
//		String corpus= extractCorpusName(new File(filename).getName());
//		System.out.println(corpus);
		
	
		
		NodeList sentences = inputDoc.getElementsByTagName("sentence");	
		//Iterate over the Sentences of a specific corpus-file
		for (int i = 0; i < sentences.getLength(); i++) {
			Element sentence= (Element) sentences.item(i);
			NodeList tokenizations= sentence.getElementsByTagName("tokenization");
			String sentenceId= sentence.getAttribute("id");
//			System.out.println("Sentence: " +sentenceId);
			
	        BufferedWriter out = new BufferedWriter(new FileWriter(outDir+File.separator+sentenceId));
	    
			//Iterate over the tokenizations of a specific Sentence
			for(int j=0; j< tokenizations.getLength(); j++){
				Element tokenization= (Element) tokenizations.item(j);
				
				//Check if the tokenization equals split or charniak lease (depending on tokenizer)
				if(tokenization.getAttribute("tokenizer").equalsIgnoreCase(tokenizer)){
					NodeList tokens = tokenization.getElementsByTagName("token");

					//Iterate over tokens
					for (int k = 0; k< tokens.getLength(); k++){
						Element token = (Element) tokens.item(k);
						out.write(token.getAttribute("text")+"\n");
//						System.out.println(token.getAttribute("text"));
					}
				}
			}
			out.flush();
			out.close();
		}
	}
	
	private static void parseArgs(String args[]){
		CmdLineParser parser = new CmdLineParser();
		
		CmdLineParser.Option inFileOption  = parser.addStringOption('i', "infile");
		CmdLineParser.Option outBaseDirOption = parser.addStringOption('o',"outdir");
		CmdLineParser.Option splitOption = parser.addStringOption('t', "tokenizer");
		
		try {
	        parser.parse(args);
	    }
	    catch ( CmdLineParser.OptionException e ) {
	        printUsage();
	        System.exit(2);
	    }

	    filename = (String)   parser.getOptionValue(inFileOption);
	    outDir= (String)  parser.getOptionValue(outBaseDirOption);
	    tokenizer= (String) parser.getOptionValue(splitOption);
	   
	    if(outDir==null || filename==null || tokenizer == null){
	    	printUsage();
	        System.exit(2);
	    }
	}
	
	private static void printUsage() {
        System.err.println(
        		"Usage:\n" +
        		"InputFile [-i,--infile] OutputDir [-o,--outdir]\n" +
        		"Use tokenization [-t, --tokenizer] split/charniak-lease \n");
        		    
	}
}
