package org.learningformat.transform;

import jargs.gnu.CmdLineParser;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.Writer;
import java.nio.charset.Charset;
import java.util.Collections;
import java.util.Set;

import javax.xml.parsers.ParserConfigurationException;

import org.learningformat.api.Corpus;
import org.learningformat.api.Document;
import org.learningformat.api.Sentence;
import org.learningformat.impl.DefaultElementFactory;
import org.learningformat.util.FileHelper;
import org.learningformat.xml.CorpusListener;
import org.learningformat.xml.Parser;
import org.xml.sax.SAXException;


public class PtbRawSentenceTransformer implements CorpusListener {

	private static String inFile, outFile;
	private static void printUsage() {
        System.err.println(
        		"Usage:\n" +
        		"InputFile [-f,--file] OutputFile [-o,--out] - optional\n" + 
        		"If no output file is given, the default is <InputFile>-ptb-s.txt");
        }
	
	
	private static void parseArgs(String args[]){
		CmdLineParser parser = new CmdLineParser();
		
		CmdLineParser.Option inFileOption  = parser.addStringOption('f', "file");
		CmdLineParser.Option outFileOption = parser.addStringOption('o',"out");
		
		try {
            parser.parse(args);
        }
        catch ( CmdLineParser.OptionException e ) {
            printUsage();
            System.exit(2);
        }

        inFile = (String)   parser.getOptionValue(inFileOption);
                
        if(inFile==null) {
        	printUsage();
            System.exit(2);
        }
        outFile = (String)  parser.getOptionValue(outFileOption, inFile + "-ptb-s.txt");
	}

	/*
	private static class PtbSingleSentenceAFileTransformer extends PtbRawSentenceTransformer {
		
		public PtbSingleSentenceAFileTransformer(File outputPrefix) {
			super(null);
			this.outputPrefix = outputPrefix;
		}
		protected File outputPrefix;
		@Override
		public void processSentence(Sentence sentence) {
			try {
				out = new OutputStreamWriter(new FileOutputStream(new File(outputPrefix, sentence.getId() +".txt")), "utf-8");
				super.processSentence(sentence);
			} catch (UnsupportedEncodingException e) {
				throw new RuntimeException(e);
			} catch (FileNotFoundException e) {
				throw new RuntimeException(e);
			} finally {

				if (out != null) {
					try {
						out.close();
					} catch (IOException e) {
						throw new RuntimeException(e);
					}
				}
			}
		}
		
	}
	*/
	protected Writer out;
	
	public PtbRawSentenceTransformer(Writer out) {
		super();
		this.out = out;
	}

	public static void main(String[] args) {
		try { 
			parseArgs(args);
			Charset encoding = Charset.forName("UTF-8");
			if (args.length < 1) {
				throw new IllegalArgumentException("Min. 1 argument needed.");
			}
			transform(new File(inFile), encoding);
		} catch (Exception e) {
			System.err.println("ERROR: " + e.getMessage());
			e.printStackTrace();
			System.exit(1);
		}
	}
	
	private static void transform(File path, Charset encoding) throws SAXException, IOException, ParserConfigurationException {
		Writer out = null;
		InputStream in = null;
		try {
			try {
			in = new FileInputStream(path);
			} catch (IOException e) {
				throw new IOException("Error opening file '" + path +"':" + e.getMessage(), e);
			}
			out = FileHelper.getBufferedFileWriter(new File(outFile), encoding);
			
			System.out.println(path);
			
			Set<String> readTokenizations = Collections.emptySet();
			Set<String> readBracketings = Collections.emptySet();
			Set<String> readParses = Collections.emptySet();
			
			Parser parser = new Parser(
					readTokenizations,
					readBracketings,
					readParses,
					new DefaultElementFactory(),
					new PtbRawSentenceTransformer(out)
			);
			parser.process(in);
		} finally {
			if (in != null) {
				in.close();
			}

			if (out != null) {
				out.close();
			}
		}
	}
	/*
	private static void transformSingle(String path) throws SAXException, IOException, ParserConfigurationException {
		Reader in = null;
		try {
			File f = new File(path);
			File singleSentenceDir = new File(f.getParent(), f.getName() + "-sentences");
			singleSentenceDir.mkdirs();
			in = new InputStreamReader(new FileInputStream(f), "utf-8");
			
			System.out.println(path);
			
			Set<String> readTokenizations = Collections.emptySet();
			Set<String> readBracketings = Collections.emptySet();
			Set<String> readParses = Collections.emptySet();
			
			org.learningformat.xml.Parser parser = new Parser(
					readTokenizations,
					readBracketings,
					readParses,
					new DefaultElementFactory(),
					new PtbSingleSentenceAFileTransformer(singleSentenceDir)
			);
			parser.process(in);
		} finally {
			if (in != null) {
				in.close();
			}
		}
	}
	*/

	@Override
	public void endCorpus() {
	}

	@Override
	public void endDocument() {
	}
	
	private int i = 1;

	@Override
	public void processSentence(Sentence sentence) {
		
		System.err.println(sentence.getId() +" "+ i++);
		
		try {

			out.write(BracketingConstants.BEGIN_SENTENCE_OPEN);
			out.write(sentence.getId());
			out.write(BracketingConstants.BEGIN_SENTENCE_CLOSE);
			out.write(BracketingConstants.SPACE);
			out.write(sentence.getText());
			out.write(BracketingConstants.SPACE);
			out.write(BracketingConstants.END_SENTENCE);
			out.write(BracketingConstants.LF);
			
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
