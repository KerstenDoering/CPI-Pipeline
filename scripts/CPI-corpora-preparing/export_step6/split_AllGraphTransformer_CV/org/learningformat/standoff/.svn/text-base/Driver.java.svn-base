package org.learningformat.standoff;

import jargs.gnu.CmdLineParser;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FilenameFilter;
import java.io.IOException;
import java.nio.charset.Charset;

import org.learningformat.api.Corpus;
import org.learningformat.api.Document;
import org.learningformat.api.Sentence;
import org.learningformat.impl.DefaultCorpus;
import org.learningformat.standoff.KnowledgeBasePairClassifier.KnowledgeBase;
import org.learningformat.standoff.KnowledgeBasePairClassifier.UndirectedKnowledgeBase;
import org.learningformat.standoff.PairGenerator.PairClassifier;
import org.learningformat.util.CSVDictReader;
import org.learningformat.util.FileHelper;

import au.com.bytecode.opencsv.CSVReader;

/**
 * Class to dispatch conversion of standoff annnotated texts to Airola XML format.
 * @see {@link http://categorizer.tmit.bme.hu/trac/wiki/PubMed2Airola}
 * @author illes
 *
 */
public class Driver {

	final static char NO_SHORT_OPTION = '\0';
	static CmdLineParser cmdParser = new CmdLineParser();
	static CmdLineParser.Option outFileOption = 
		cmdParser.addStringOption('o', "out-file");
	static CmdLineParser.Option pairsFileOption = 
		cmdParser.addStringOption('p', "pairs-file");
	static CmdLineParser.Option encodingOption = 
		cmdParser.addStringOption('e', "encoding");
	static CmdLineParser.Option oneBasedOption = 
		cmdParser.addBooleanOption(NO_SHORT_OPTION, "one-based");
	static CmdLineParser.Option endInclusiveOption = 
		cmdParser.addBooleanOption(NO_SHORT_OPTION, "end-inclusive");	
	static CmdLineParser.Option corpusOption = 
		cmdParser.addStringOption('c', "corpus");
	static CmdLineParser.Option fromOption = 
		cmdParser.addIntegerOption(NO_SHORT_OPTION, "from");
	static CmdLineParser.Option withPairsOption = 
		cmdParser.addBooleanOption(NO_SHORT_OPTION, "with-pairs");
	static CmdLineParser.Option fatalOption = 
		cmdParser.addBooleanOption(NO_SHORT_OPTION, "fatal");
	

	private static void printUsage() {
		System.err
				.println("Usage:\n java ... [options] file.txt [...]\n java ... [options] input_dir\n\nOptions:\n"
						+ "\t[-o, --out-file      ] FILE   	Output file\n"
						+ "\t[-p, --pairs-file    ] FILE   	Undirected identifier pairs\n"
						+ "\t[-c, --corpus        ] NAME  	Corpus name\n"
						+ "\t[-e, --encoding      ] NAME  	Input encoding (default: UTF-8)\n"
						+ "\t[    --from          ] NUM   	Assign document indices starting from (default: 0)\n"
						+ "\t[    --one-based     ]        	Input annotation offsets start at position 1\n"
						+ "\t[    --end-inclusive ]        	Input annotation's end position is inclusive\n"
						+ "\t[    --with-pairs    ]        	Output only sentences having pairs\n"
						+ "\t[    --fatal         ]        	Halt on parse errors\n"
						);
	}

	public static void main(String[] args) {
		try {
			cmdParser.parse(args);
		} catch (CmdLineParser.OptionException e) {
			System.err.print(e.getMessage());
			e.printStackTrace();
			printUsage();
			System.exit(2);
		}
		try {
			// unpack options
			boolean offsetOneBased = (Boolean) cmdParser.getOptionValue(oneBasedOption,	Boolean.FALSE);
			boolean offsetEndInclusive = (Boolean) cmdParser.getOptionValue(endInclusiveOption, Boolean.FALSE);
			boolean withPairs = (Boolean) cmdParser.getOptionValue(withPairsOption, Boolean.FALSE);
			boolean fatal = (Boolean) cmdParser.getOptionValue(fatalOption, Boolean.FALSE);
			String encodingName = (String) cmdParser.getOptionValue(encodingOption, "UTF-8");
			String corpusName = (String) cmdParser.getOptionValue(corpusOption, "out");
			String outFileName = (String) cmdParser.getOptionValue(outFileOption, corpusName+".xml");
			String pairsFileName = (String) cmdParser.getOptionValue(pairsFileOption, "kb.csv");
			int startFrom = (Integer) cmdParser.getOptionValue(fromOption, new Integer(0));
			String[] inputFileNames = cmdParser.getRemainingArgs();

			if (inputFileNames == null || inputFileNames.length == 0)
			{
				System.err.println("ERROR: No input files (.txt) specified.\n");
				printUsage();
				System.exit(2);				
			}
			
			// initialize
			StandoffParser parser = new StandoffParser();
			
			parser.setOffsetOneBased(offsetOneBased);
			parser.setOffsetEndInclusive(offsetEndInclusive);
			parser.setStopOnError(fatal);
			
			File outFile = new File(outFileName);
			//FileHelper.checkFile(outFile);
			Charset charset = Charset.forName(encodingName);
		
			Corpus corpus = new DefaultCorpus();
			corpus.setSource(corpusName);

			File pairsFile = new File(pairsFileName);
			
			//TODO startFrom
			if (startFrom != 0)
				throw new UnsupportedOperationException("not implemented");
			
			KnowledgeBase kb = knowledgeBaseFromCSV(pairsFile);
			PairClassifier pc = new KnowledgeBasePairClassifier(kb);

			// TODO: there is no need to keep all documents in memory (referenced from corpus)
			// rewrite to print xml header, documents at once, xml footer
			long millis = System.currentTimeMillis();
			
			// list directory
			if (new File(inputFileNames[0]).isDirectory())
			{
				System.err.println("INFO: reading contents of directory: '" + inputFileNames[0] +"'");
				final File dir = new File(inputFileNames[0]);
				final FilenameFilter filter = new FileHelper.IncludePatternFilenameFilter("^.*\\.txt$");
				final String[] files = dir.list(filter);
				
				inputFileNames = new String[files.length];
				for (int i = 0; i < files.length; i++) {
					inputFileNames[i] = new File(dir, files[i]).getCanonicalPath();
				}
			}
			// process input files
			for (String inputFileName : inputFileNames) {
				File inputFile = new File(inputFileName);
				FileHelper.checkFile(inputFile);
				File dir = inputFile.getParentFile();
				String prefix = inputFile.getName().replaceFirst("\\.txt$", "");
				Document d = parser.fromStandoffFiles(corpus.getSource(), dir, prefix, charset);
				
				// propagate pairs
				for (Sentence s : d.getSentences())
					PairGenerator.addClassiedPairs(s, pc);
				
				// add to corpus
				d.setCorpus(corpus);
			}
			millis = System.currentTimeMillis() - millis;	
			System.err.println("INFO: Corpus with " + corpus.getDocuments().size() + " documents constructed in " + (millis/1000.0f) + " seconds.");
			
			// generate output
			AirolaXmlWriter writer = new AirolaXmlWriter();
			writer.setSentencesWithPairsOnly(withPairs);
			millis = System.currentTimeMillis();			
			writer.toXMLFile(corpus, outFile, 2);
			millis = System.currentTimeMillis() - millis;		
			System.err.println("INFO: Output written to '" + outFile + "' in " + (millis/1000.0f) + " seconds.");
		}
		 catch (IOException e) {
			 e.printStackTrace();
			 System.exit(1);
		}
	}

	private static KnowledgeBase knowledgeBaseFromCSV(File kbFile) throws FileNotFoundException, IOException {
		System.err.println("INFO: Parsing knowledge base  from '" + kbFile.getCanonicalPath() + "' ...");
		long millis = System.currentTimeMillis();
		KnowledgeBase kb = UndirectedKnowledgeBase.from(
				new CSVDictReader(
					new CSVReader(
						FileHelper.getBufferedFileReader(kbFile,	Charset.forName("UTF-8"))))
							.captureHeader());
		millis = System.currentTimeMillis() - millis;		
		System.err.println("INFO: Parsed knowledge base with " + kb.size() + " unique pairs in " + (millis/1000.0f) + " seconds.");
		return kb;
	}

}