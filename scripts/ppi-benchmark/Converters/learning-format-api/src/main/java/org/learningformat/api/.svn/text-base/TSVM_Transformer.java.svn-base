package org.learningformat.api;

import jargs.gnu.CmdLineParser;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.Reader;
import java.io.UnsupportedEncodingException;
import java.io.Writer;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import javax.xml.parsers.ParserConfigurationException;

import org.learningformat.impl.DefaultElementFactory;
import org.learningformat.transform.SvmLightTreeKernelTransformer;
import org.learningformat.transform.TSVM_ExampleWriter;
import org.learningformat.xml.Parser;
import org.learningformat.xml.CorpusListener;
import org.xml.sax.SAXException;


public class TSVM_Transformer  implements CorpusListener{

	static String baseOutDir="/home/philippe/Desktop/svm/otherMethods/tsvm/corpus/parsed";
	static String inFile="/home/philippe/Desktop/svm/otherMethods/jsre/corpus/AImed-learning-format.xml";
//	static String inFile="/home/philippe/Desktop/LLL-learning-format.xml";
	static String split="/home/philippe/Desktop/svm/splits";
	protected static String tokenizer= "split";

		
	protected Map<String, Integer> folds; //Mapping between folds
	protected File dirOut;
	protected String parser;
	protected static int desiredFoldsCount = 10;
	protected Writer[] testSentence = new Writer[desiredFoldsCount];	
	protected Writer[] testProtein = new Writer[desiredFoldsCount];
	
	protected TSVM_ExampleWriter exampleWriter;
	

	public static void main(String[] args) throws IOException, ParserConfigurationException, SAXException{
//		parseArgs(args);

		File inputFile = new File(inFile);
		Reader in= null;
		
		String corpusName = inputFile.getName();
		corpusName = corpusName.substring(0, corpusName.indexOf('-'));
		Map<String, Integer> folds = SvmLightTreeKernelTransformer.readFolds(split, corpusName/*, 0*/);
			
		File outDir = new File(baseOutDir + File.separator + corpusName  + File.separator);
		outDir.mkdirs();
		
		
		TSVM_Transformer ec = new TSVM_Transformer(
				LearningFormatConstants.CHARNIAK_LEASE_TOKENIZER,
				LearningFormatConstants.CHARNIAK_JOHNSON_MCCLOSKY_PARSER,
				folds, outDir);
		
		in = new InputStreamReader(new FileInputStream(inputFile), "utf-8");
		org.learningformat.xml.Parser parser = new Parser(
				Collections.singleton(LearningFormatConstants.CHARNIAK_LEASE_TOKENIZER),
				Collections.singleton(LearningFormatConstants.CHARNIAK_JOHNSON_MCCLOSKY_PARSER),
				Collections.singleton(LearningFormatConstants.CHARNIAK_LEASE_PARSER), 
				new DefaultElementFactory(), ec);
		parser.process(in);
		in.close();
		
		System.out.println("The end");

	}
	

	
	protected TSVM_ExampleWriter createExampleWriter() {
		return new TSVM_ExampleWriter(tokenizer, parser);
	}

	//Flush all writers
	@Override
	public void endCorpus() {
		for (int i = 0; i < testSentence.length; i++) {
			try {
				testSentence[i].close();
				testProtein[i].close();	
				
			} catch (IOException e) {
				throw new RuntimeException(e);
			}
		}
	}

	@Override
	public void endDocument() {	
	}

	//Here happens the magic
	@Override
	public void processSentence(Sentence sentence) {
		List<Pair> pairs = sentence.getAllPairs();	

		if (pairs != null) { //Has the sentence a pair
			Set<String> uniquePairs = new HashSet<String>(pairs.size());
			
			for (Pair pair : pairs) {
				String e1Id = pair.getE1().getId();
				String e2Id = pair.getE2().getId();
				
				if (!e1Id.equals(e2Id)) {//Only non-self interacting pairs					
					String key = e1Id.compareTo(e2Id) > 0 ? e1Id + '|' + e2Id : e2Id + '|' + e1Id; // Generates a unique key.
					if (!uniquePairs.contains(key)) {
						uniquePairs.add(key);
						String docid = sentence.getDocument().getId();

						Integer fold = folds.get(docid); //This document is used in which fold? 
//						System.out.println(fold);
						if (fold == null) {
							throw new IllegalStateException(
									"no fold found for doc '" + docid + "'");
						}
							
						try {
							
							String output[]= exampleWriter.getOutput(pair, sentence, tokenizer);
							testSentence[fold.intValue()].append(output[0]);
							testProtein[fold.intValue()].append(output[1]);
							
//							for(int j=0; j<desiredFoldsCount; j++){
//								if(fold.intValue()!=j){
//									trainSentence[fold.intValue()].append(output[0]);
//									trainProtein[fold.intValue()].append(output[1]);
//								}
//							}
//							
						} catch (IOException e) {
							System.err.println("Error while writing writer");
							e.printStackTrace();
						}
					}
				}
			}			
		}
	}

	@Override
	public void startCorpus(Corpus corpus) {		
	}

	@Override
	public void startDocument(Document document) {		
	}
	
	//Class constructor
	public TSVM_Transformer(String tokenizer, String parser,  Map<String, Integer> folds, File dirOut) {
		super();
		TSVM_Transformer.tokenizer = tokenizer;
		this.parser = parser;
		this.folds = folds;
		this.dirOut = dirOut;		
		this.exampleWriter =  createExampleWriter();

		//Produce the different files
		for (int i = 0; i < testSentence.length; i++) {
			try {				
				testSentence[i] = new OutputStreamWriter(new FileOutputStream( new File(dirOut, "sentence" + i + ".test")), "utf-8");
				testProtein[i] = new OutputStreamWriter(new FileOutputStream( new File(dirOut, "protein" + i + ".test")), "utf-8");
			} catch (UnsupportedEncodingException e) {
				throw new RuntimeException(e);
			} catch (FileNotFoundException e) {
				throw new RuntimeException(e);
			}
		}
	}

	private static void printUsage() {
        System.err.println(
        		"Usage:\n" +
        		"InputFile [-i,--in] OutputDir [-o,--outdir]\n" +        		
        		"Directory of splits [-s,--split]\n" +
        		"Used tokenizer : [-t, --tokenizer]\n" );
        }
	
	
	
	@SuppressWarnings("unused")
	private static void parseArgs(String args[]){
		CmdLineParser parser = new CmdLineParser();
		
		CmdLineParser.Option inFileOption  = parser.addStringOption('i', "in");
		CmdLineParser.Option outBaseDirOption = parser.addStringOption('o',"outdir");
		CmdLineParser.Option splitOption = parser.addStringOption('s', "split");
		CmdLineParser.Option tokenizerOption = parser.addStringOption('t', "tokenizer");
		
		
		try {
            parser.parse(args);
        }
        catch ( CmdLineParser.OptionException e ) {
            printUsage();
            System.exit(2);
        }

        inFile = (String)   parser.getOptionValue(inFileOption);
        baseOutDir= (String)  parser.getOptionValue(outBaseDirOption);
        split = (String) parser.getOptionValue(splitOption);
        tokenizer= (String) parser.getOptionValue(tokenizerOption);

        
        if(inFile==null || baseOutDir==null || split == null || tokenizer==null){
        	printUsage();
            System.exit(2);
        }
        
	}

	
}
