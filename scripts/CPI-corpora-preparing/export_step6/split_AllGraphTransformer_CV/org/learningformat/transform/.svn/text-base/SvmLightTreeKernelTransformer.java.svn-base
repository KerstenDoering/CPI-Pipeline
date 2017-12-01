package org.learningformat.transform;

import jargs.gnu.CmdLineParser;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.UnsupportedEncodingException;
import java.io.Writer;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.learningformat.api.Corpus;
import org.learningformat.api.Document;
import org.learningformat.api.LearningFormatConstants;
import org.learningformat.api.Pair;
import org.learningformat.api.Sentence;
import org.learningformat.impl.DefaultElementFactory;
import org.learningformat.util.ElementsCounter;
import org.learningformat.xml.CorpusListener;
import org.learningformat.xml.Parser;

public class SvmLightTreeKernelTransformer implements CorpusListener,
		SvmLightTreeKernelConstants {

	protected LineStyle lineStyle;

	protected static int desiredFoldsCount = 10;
	
	protected Writer[] writers = new Writer[desiredFoldsCount];
	
	private static String inFile, baseDir, split;
	private static boolean moschitti, custom;
	private static void printUsage() {
        System.err.println(
        		"Usage:\n" +
        		"InputFile [-f,--file] OutputDir [-o,--out]\n" +
        		"Directory of splits [-s,--split]\n" +
        		"Moschitti format [-m,--moschitti] " +
        		"Custom  format [-c,--custom]");
        		    
	}
	
	
	
	private static void parseArgs(String args[]){
		CmdLineParser parser = new CmdLineParser();
		
		CmdLineParser.Option inFileOption  = parser.addStringOption('f', "file");
		CmdLineParser.Option outBaseDirOption = parser.addStringOption('o',"out");
		CmdLineParser.Option splitOption = parser.addStringOption('s', "split");
		CmdLineParser.Option moschittiOption  = parser.addBooleanOption('m', "moschitti");
		CmdLineParser.Option customOption  = parser.addBooleanOption('c', "custom");
		
		try {
            parser.parse(args);
        }
        catch ( CmdLineParser.OptionException e ) {
            printUsage();
            System.exit(2);
        }

        inFile = (String)   parser.getOptionValue(inFileOption);
        baseDir= (String)  parser.getOptionValue(outBaseDirOption);
        split = (String) parser.getOptionValue(splitOption);
        moschitti= (Boolean) parser.getOptionValue(moschittiOption, Boolean.FALSE);
        custom= (Boolean) parser.getOptionValue(customOption, Boolean.FALSE);

        
        if(inFile==null || baseDir==null || split == null){
        	printUsage();
            System.exit(2);
        }
        
        if(moschitti==true && custom==true || moschitti==false && custom==false ){
        	System.err.println("Moschitti and Custom kernel are both (un)set. Not valid option");
        	printUsage();
        	System.exit(2);
        }
	}

	
	public static void main(String[] args) throws Exception {
		parseArgs(args);	

			if (args.length < 1) {
				throw new IllegalArgumentException("Min. 1 argument needed.");
			}
			LineStyle lineStyle = LineStyle.CUSTOM_KERNEL;
			if(custom==true){
				lineStyle  = LineStyle.CUSTOM_KERNEL;
			}
			else if(moschitti==true){
				lineStyle = LineStyle.MOSCHITTI;
			}
			else{
				printUsage();
				System.exit(2);
			}
		
//			for (int i = 0; i < args.length; i++) {

				File inputFile = new File(inFile);

				Set<String> emptySet = Collections.emptySet();
				InputStream in = null;
				ElementsCounter ec = new ElementsCounter();
				try {
					in = new FileInputStream(inputFile);
					Parser parser = new Parser(
							emptySet,
							emptySet, 
							emptySet, 
							new DefaultElementFactory(), ec);
					parser.process(in);

				} finally {
					if (in != null) {
						in.close();
					}
				}

				String corpusName = inputFile.getName();
				while ( corpusName.indexOf('-') != -1)
					corpusName = corpusName.substring(0, corpusName.indexOf('-'));
				while ( corpusName.indexOf('.') != -1)
					corpusName = corpusName.substring(0, corpusName.indexOf('.'));
					

				Map<String, Integer> folds = readFolds(split, corpusName/*, ec.getDocumentsCount()*/);
				
				File outDir = new File(baseDir + File.separator + lineStyle +File.separator + corpusName
								+ "-folds");
				outDir.mkdirs();

				SvmLightTreeKernelTransformer tf = new SvmLightTreeKernelTransformer(
						LearningFormatConstants.CHARNIAK_LEASE_TOKENIZER,
						LearningFormatConstants.CHARNIAK_JOHNSON_MCCLOSKY_PARSER,
						lineStyle, folds, outDir);
				
				try {
					in = new FileInputStream(inputFile);
					Parser parser = new Parser(
							Collections.singleton(LearningFormatConstants.CHARNIAK_LEASE_TOKENIZER),
							Collections.singleton(LearningFormatConstants.CHARNIAK_JOHNSON_MCCLOSKY_PARSER),
							Collections.singleton(LearningFormatConstants.CHARNIAK_JOHNSON_MCCLOSKY_PARSER), // null: all parses,  emptySet: ignore parses, ...
							new DefaultElementFactory(), tf);
					tf.initializeExampleWriters();
					parser.process(in);
					
					System.exit(0);
				} finally {
					if (in != null) {
						in.close();
					}
				}
//			}

	}

	public static Map<String, Integer> readFolds(String splitLocation, String corpusName) throws IOException {
		Map<String, Integer> result = new HashMap<String, Integer>();

		//System.err.println("readFolds(" + splitLocation +"," + corpusName  + ")");
		
		if (("BioInferM".equals(corpusName))||("BioInferCLAnalysis_split_SMBM_version".equals(corpusName))) {
			corpusName = "BioInfer";
		}
		if (("AImedM".equals(corpusName))|| ("AImedprob".equals(corpusName))) {
			corpusName = "AIMed";
		}
		File foldsRoot = new File(splitLocation);
		File foldsDir = new File(foldsRoot, corpusName);
		
		

		for (int i = 0; i < desiredFoldsCount; i++) {
			int readFold = i + 1;

			BufferedReader r = new BufferedReader(
					new InputStreamReader(new FileInputStream(new File(
							foldsDir, corpusName + readFold + ".txt")), "UTF-8"));
			String line = null;
			while ((line = r.readLine()) != null) {
				String docid = line.substring(line.indexOf(' ') + 1).trim();
				result.put(docid, Integer.valueOf(i));
			}
		}
		return result;
	}

	protected Map<String, Integer> folds;
	protected ExampleWriter exampleWriter;

	protected File dirOut;

	private final String parser;

	private final String tokenizer;
	
	public String getParser() {
		return parser;
	}


	public String getTokenizer() {
		return tokenizer;
	}



	public SvmLightTreeKernelTransformer(String tokenizer, String parser,
			LineStyle lineStyle, Map<String, Integer> folds, File dirOut) {
		super();
		this.tokenizer = tokenizer;
		this.parser = parser;
		this.lineStyle = lineStyle;
		this.folds = folds;
		this.dirOut = dirOut;
		
		if (parser == null)
			throw new IllegalArgumentException("parser should not be null");

	}

	public void initializeExampleWriters()
	{
		this.exampleWriter = createExampleWriter();

		for (int i = 0; i < writers.length; i++) {
			try {
				writers[i] = new OutputStreamWriter(new FileOutputStream(
						new File(dirOut, "" + i + ".txt")), SvmLightDependencyTreeKernelTransformer.UTF8 );
			} catch (UnsupportedEncodingException e) {
				throw new RuntimeException(e);
			} catch (FileNotFoundException e) {
				throw new RuntimeException(e);
			}
		}

	}

	
	public void initializeExampleWriters(int qGramMin, int qGramMax, int kBand)
	{
		this.exampleWriter = createExampleWriter( qGramMin, qGramMax, kBand );

		for (int i = 0; i < writers.length; i++) {
			try {
				writers[i] = new OutputStreamWriter(new FileOutputStream(
						new File(dirOut, "" + i + ".txt")), SvmLightDependencyTreeKernelTransformer.UTF8 );
			} catch (UnsupportedEncodingException e) {
				throw new RuntimeException(e);
			} catch (FileNotFoundException e) {
				throw new RuntimeException(e);
			}
		}

	}
	

	protected ExampleWriter createExampleWriter() {
		return new BracketingExampleWriter(tokenizer, parser, lineStyle);
	}

	protected ExampleWriter createExampleWriter(int qGramMin, int qGramMax, int kBand) {
		throw new UnsupportedOperationException("Supported only in SvmLightDependencyTKT!");
		//return new BracketingExampleWriter(tokenizer, parser, lineStyle);
	}

	@Override
	public void endCorpus() {
		for (int i = 0; i < writers.length; i++) {
			try {
				writers[i].close();
			} catch (IOException e) {
				throw new RuntimeException(e);
			}
		}
	}

	@Override
	public void endDocument() {
	}

	@Override
	public void processSentence(Sentence sentence) {

		try {

			List<Pair> pairs = sentence.getAllPairs();

			if (pairs != null) {
				Set<String> uniquePairs = new HashSet<String>(pairs.size());
				for (Pair pair : pairs) {

					String e1Id = pair.getE1().getId();
					String e2Id = pair.getE2().getId();

					if (!e1Id.equals(e2Id)) {
						/* no self-interactions */

						/* check if this pair is unique */
						/*
						 * create a key in which the e1 and e2 ids are ordered
						 * alphabetically
						 */
						String key = e1Id.compareTo(e2Id) > 0 ? e1Id + '|'
								+ e2Id : e2Id + '|' + e1Id;
						if (!uniquePairs.contains(key)) {
							uniquePairs.add(key);

							String docid = sentence.getDocument().getId();

							Integer fold = folds.get(docid);
							if (fold == null) {
								throw new IllegalStateException(
										"no fold found for doc '" + docid + "'");
							}
							if ( writers[fold.intValue()] == null ) {
								throw new IllegalStateException(
										"Writer not found for fold '" + fold.intValue() + "'");
							}
							exampleWriter.write(pair, sentence, writers[fold.intValue()]);
						}
					}
				}
			}

		} catch (IOException e) {
			throw new RuntimeException();
		}

	}

	@Override
	public void startCorpus(Corpus corpus) {
	}

	@Override
	public void startDocument(Document document) {
	}

}
