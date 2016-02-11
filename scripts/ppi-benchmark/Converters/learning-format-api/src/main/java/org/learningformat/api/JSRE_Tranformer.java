package org.learningformat.api;

import jargs.gnu.CmdLineParser;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.Reader;
import java.io.Writer;
import java.nio.charset.Charset;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.learningformat.impl.DefaultElementFactory;
import org.learningformat.transform.JSRE_ExampleWriter;
import org.learningformat.transform.SvmLightTreeKernelTransformer;
import org.learningformat.util.FileHelper;
import org.learningformat.util.PorterStemmer;
import org.learningformat.xml.CorpusListener;
import org.learningformat.xml.Parser;



public class JSRE_Tranformer implements CorpusListener {
	
	private static String outBaseDir = "jsre-corpus";
	private static String inFile;
	private static String splitDir;
	private static String corpus;
	private static String lemmaFile; //"/home/philippe/Desktop/svm/otherMethods/jsre/corpus/out/tst.txt.txp";
	
	
	static CmdLineParser cmdParser = new CmdLineParser();
	static CmdLineParser.Option inFileOption  = cmdParser.addStringOption('i', "in");
	static CmdLineParser.Option outBaseDirOption = cmdParser.addStringOption('o',"outdir");
	static CmdLineParser.Option splitOption = cmdParser.addStringOption('s', "split");
	static CmdLineParser.Option lemmaOption = cmdParser.addStringOption('l', "lemma");
	static CmdLineParser.Option corpusOption = cmdParser.addStringOption('c', "corpus");
	static CmdLineParser.Option stemmerOption = cmdParser.addBooleanOption('\0', "porter");
	static CmdLineParser.Option tokenizerOption = cmdParser.addStringOption('t', "tokenizer");	
	static CmdLineParser.Option skipTrainOption = cmdParser.addBooleanOption('\0', "skip-train");
	
	static int selfIntact; 
	static int intact;
	static int notSelf;
	static boolean skipTrain = false;

	private final Map<String, Integer> folds; //Mapping between folds
	private final String tokenizer;
	private final static int desiredFoldsCount = 10;
	private final Writer[] test = new Writer[desiredFoldsCount];
	private final Writer[] train = new Writer[desiredFoldsCount];
	private final JSRE_ExampleWriter exampleWriter;
	
	
	/** Pre-computed leamma's. */
	protected HashMap<String, String > lemmata;
	/** Stemmer used if {@link lemmata} is <code>null</code>. If <code>null</code>, the {@link Token#getText()} is used as lemma. */
	protected PorterStemmer stemmer;
	private static boolean doStemming;
	
	
	/**
	 * Implement lemmatization fallback 
	 * @author illes
	 *
	 */
	public class Lemmatizer {
	    public String lemmatize(String token) {
		String lemma = null;
		
		if (lemmata != null) lemma = lemmata.get(token);
		else if (stemmer != null) lemma = stemmer.stem(token);
		    
		// never return null
		return lemma != null ? lemma : token;
	    }
	}
	
	public static void main(String[] args) throws Exception{
		
		parseArgs(args);
		
		File inputFile = new File(inFile);

		FileHelper.checkFile(inputFile);
		Reader in = null;
		
		Charset encoding = Charset.forName("UTF-8");

		//Get corpusName and getFolds...
		String corpusName = 
			corpus != null
			? corpus
			: inputFile.getName().replaceFirst("\\.xml", "");
		//corpusName = corpusName.substring(0, corpusName.indexOf('-'));//Just at the moment
		Map<String, Integer> folds = SvmLightTreeKernelTransformer.readFolds(splitDir, corpusName/*, 0*/);// Last parameter not necessary?
		

		FileHelper.checkDir(new File(outBaseDir));
		File outDir = new File(new File(outBaseDir), corpusName);
//		System.out.println(baseDir + File.separator + corpusName + "-folds");
		outDir.mkdirs();
		FileHelper.checkDir(outDir);
		
	    final String tokenizer = (String) cmdParser.getOptionValue(tokenizerOption, "split" /*LearningFormatConstants.CHARNIAK_LEASE_TOKENIZER*/);
		
		JSRE_Tranformer ec = new JSRE_Tranformer(
				tokenizer,
				folds, outDir, lemmaFile, doStemming);

		in = FileHelper.getBufferedFileReader(inputFile, encoding);
		Parser parser = new Parser(
				Collections.singleton(tokenizer),
				Collections.<String>emptySet(),
				Collections.<String>emptySet(),
				new DefaultElementFactory(), ec);
		parser.setImmediatelyRemoveDocuments(true); // be GC friendly
		parser.process(in);
		in.close();
	}
	
	//Here happens the magic


	private void close() throws IOException
	{
		IOException error = null;
		for (Writer w : test) {
			try {
				w.close();
			} catch (IOException e) { error = e; }
		}
		for (Writer w : train) {
			try {
				w.close();
			} catch (IOException e) { error = e; }
		}
		if (error != null)
			throw error;
	}
	//Flush all writers
	@Override
	public void endCorpus() {
		System.out.println(selfIntact +"\t" +intact +"\t" +notSelf);
		try {
			close();
		}
		catch (Exception e) {
			throw new RuntimeException("Error closing some writers", e);
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
			
			//For each Pair:
			for (Pair pair : pairs) {
				intact++;
				String e1Id = pair.getE1().getId();
				String e2Id = pair.getE2().getId();
				
				if (!e1Id.equals(e2Id)) { // Only no self-interacting pairs (makes little sense on tree and other structures)
					String key = e1Id.compareTo(e2Id) > 0 ? e1Id + '|' + e2Id : e2Id + '|' + e1Id; // Generates a unique key.
					notSelf++;
					
					if (!uniquePairs.contains(key)) {
						uniquePairs.add(key);
						String docid = sentence.getDocument().getId();

						Integer fold = folds.get(docid); //This document is used in which fold? 
						if (fold == null) {
							throw new IllegalStateException(
									"no fold found for doc '" + docid + "'");
						}
						
						try {
//							exampleWriter.write(pair, sentence, writers[fold.intValue()]);//Exception							
							String example = exampleWriter.getOutput(pair, sentence, new Lemmatizer());
							test[fold.intValue()].append(example);
							for(int j=0; j<desiredFoldsCount; j++)
								if(fold.intValue()!=j)
									train[j].append(example);
						} catch (IOException e) {
							throw new RuntimeException("Error while writing JSRE test/train example.", e);
						}
					}
				}
				else
					selfIntact++;
			}			
		}
	}

	@Override
	public void startCorpus(Corpus corpus) {
		// do nothing
	}

	@Override
	public void startDocument(Document document) {
	}

	
	
	//Class constructor
	public JSRE_Tranformer(String tokenizer, Map<String, Integer> folds, File dirOut, String lemma, boolean doPorterStemming) throws FileNotFoundException {
		super();
		this.tokenizer = tokenizer;
		this.folds = folds;
		if (doPorterStemming) stemmer = new PorterStemmer();
		if (lemma != null) lemmata = Lemma.readLemma(lemma);
		final Charset encoding = Charset.forName("UTF-8");
		this.exampleWriter =  createExampleWriter();
		
		// create output files
		for (int i = 0; i < test.length; i++) {
			test[i] = 
				FileHelper.getBufferedFileWriter(new File(dirOut, "test" + i + ".txt"), encoding);
			train[i] = skipTrain
				? new FileHelper.NullWriter()
				: FileHelper.getBufferedFileWriter(new File(dirOut, "train" + i + ".txt"), encoding);
		}

	}

	protected JSRE_ExampleWriter createExampleWriter() {
		return new JSRE_ExampleWriter(tokenizer);
	}

	
	private static void printUsage() {
	    System.err.println(
        		"Usage:\n" +
        		"\t[-i, --in    	] FILE  	Input file\n" +
        		"\t[-o, --outdir	] DIR   	Output dir\n" +
        		"\t[-s, --split 	] DIR   	Directory of splits\n" +
        		"\t[-t, --tokenizer	] NAME  	Tokenizer (for POS tags) \n" +
        		"\t[    --skip-train]       	Do not write train examples\n" +
        		"\t[-c, --corpus	] NAME  	Corpus name (should match file and folders)\n" +
        		"\t[-l, --lemma 	] FILE  	Precomputed lemmata\n" +
        		"\t[-t, --tokenizer	] NAME  	Tokenizer (for POS tags) \n" +
        		"\t[    --porter	]       	Use stemmer\n"
        		);
        }
	
	
	
	private static void parseArgs(String args[]) {
		try {
		    cmdParser.parse(args);
        }
        catch ( CmdLineParser.OptionException e ) {
            System.err.print(e.getMessage());
            e.printStackTrace();
            printUsage();
            System.exit(2);
        }
       
        inFile = (String) cmdParser.getOptionValue(inFileOption, inFile);
        outBaseDir = (String)  cmdParser.getOptionValue(outBaseDirOption, outBaseDir);
        splitDir = (String) cmdParser.getOptionValue(splitOption, splitDir);
        lemmaFile = (String) cmdParser.getOptionValue(lemmaOption, lemmaFile);
        doStemming = (Boolean) cmdParser.getOptionValue(stemmerOption, Boolean.FALSE);
        corpus = (String) cmdParser.getOptionValue(corpusOption, null);
        skipTrain = (Boolean) cmdParser.getOptionValue(skipTrainOption, Boolean.FALSE);
       
        if (inFile == null || outBaseDir == null || splitDir == null) {
            System.err.println("A required argument (corpus, in, outdir, split) is missing and has no default value.");
            printUsage();
            System.exit(2);
        }
        
	}
	
	

}
