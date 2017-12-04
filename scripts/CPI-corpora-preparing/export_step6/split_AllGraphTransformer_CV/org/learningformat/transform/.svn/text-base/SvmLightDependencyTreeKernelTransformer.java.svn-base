package org.learningformat.transform;

import jargs.gnu.CmdLineParser;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Reader;
import java.util.Collections;
import java.util.Map;
import java.util.Set;

import javax.xml.parsers.ParserConfigurationException;

import org.learningformat.api.LearningFormatConstants;
import org.learningformat.impl.DefaultElementFactory;
import org.learningformat.transform.EntityContextExampleWriter.EntityPosition;
import org.learningformat.transform.EntityContextExampleWriter.LengthsPolicy;
import org.learningformat.transform.EntityContextExampleWriter.SelfReferences;
import org.learningformat.transform.EntityContextExampleWriter.Stemming;
import org.learningformat.util.ElementsCounter;
import org.learningformat.xml.Parser;
import org.xml.sax.SAXException;

public class SvmLightDependencyTreeKernelTransformer extends SvmLightTreeKernelTransformer {

	protected static enum Format {q, c, b};
	public static enum DependencyTypeGeneralization {none, genConj, genConjSubj, genConjSubjObj, genConjObj};
	public static final String UTF8 = "UTF-8";
	protected final int qGramLengthMin;
	protected final int qGramLengthMinMax;
	protected final int qGramLengthMaxMin;
	protected final int qGramLengthMax;
	protected final int kBandLength;
	protected final LengthsPolicy lengthsPolicy = LengthsPolicy.UP_TO;
	protected final Format format = Format.b;
	public static DependencyTypeGeneralization dependencyTypeGeneralization = DependencyTypeGeneralization.none;

	protected static EntityPosition entityPosition = EntityPosition.OUTSIDE;
	//private static EntityPosition entityPosition = EntityPosition.BEGINNING;
	protected static SelfReferences selfReferences = SelfReferences.NO_SELF_REF;
	public static Stemming stemming = Stemming.STEM;
	
	private static void printUsage() {
        System.err.println(
        		"Usage:\n" +
        		"InputFile [-f,--file] OutputDir [-o,--out]\n" +
        		"Directory of splits [-s,--split]\n" +
        		"Tokenizer [-t, --tokenizer] (default: '"+LearningFormatConstants.CHARNIAK_LEASE_TOKENIZER+ "')\n" +
        		"Parser (should match tokenizer) [-p,--parser]  (default: '" + LearningFormatConstants.CHARNIAK_LEASE_PARSER + "')\n" +
        		"Min length of paths [--qmin] (int: [1,5], default: 2)\n" +
        		"Max of min length of paths [--qminmax] (int: [1,5], default: 2)\n" +
        		"Min of max length of paths [--qmaxmin] (int: [1,5], default: 2)\n" +
        		"Max length of paths [--qmax] (int: [1,5], default: 2)\n" +
        		"Value of \'k\' [-k,--kvalue] (int: [0,2], default: 0)\n");        		    
	}

	
	public SvmLightDependencyTreeKernelTransformer(String tokenizer, String parser, int qmin, int qminmax, int qmaxmin, int qmax, int k) 
	{
		super(tokenizer, parser, LineStyle.CUSTOM_KERNEL, null, null );
	    this.qGramLengthMin = qmin;
	    this.qGramLengthMinMax = qminmax;
	    this.qGramLengthMaxMin = qmaxmin;
	    this.qGramLengthMax = qmax;
	    this.kBandLength = k;
	    
	}

	public void run(String inFile, String split, String baseDir) throws IOException, ParserConfigurationException, SAXException 
	{
		

//		for (qGramLengthMin = 1; qGramLengthMin <= 2; qGramLengthMin++) {
//			for (qGramLengthMax = qGramLengthMin; qGramLengthMax <= 3; qGramLengthMax++) {
//				for (kBand = 0; kBand <= Math.min(1, qGramLengthMax); kBand++) {

		
		
		for ( int qGramMin = qGramLengthMin; qGramMin <= qGramLengthMinMax; qGramMin++) {
			for (int qGramMax = qGramLengthMaxMin; qGramMax <= qGramLengthMax; qGramMax ++) {
				for (int kBand = 0; kBand<= Math.min(kBandLength, qGramMax); kBand ++) {
					File inputFile = new File(inFile);
					Set<String> emptySet = Collections.emptySet();
					Reader in = null;
					ElementsCounter ec = new ElementsCounter();
					try {
						in = new InputStreamReader(new FileInputStream(inputFile),
								UTF8);
						org.learningformat.xml.Parser parser = new Parser(emptySet,
								emptySet, emptySet, new DefaultElementFactory(), ec);
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
					File outDir = new File(baseDir + File.separator + lineStyle+ 
							"-"+ format 
							+"-"+ qGramMin //qGramLengthMin
							+"to"+ qGramMax //qGramLengthMax
							+"-k"+kBand // 
							+"-"+lengthsPolicy +"-"+ entityPosition
							+"-"+ selfReferences
							+"-"+ stemming
							+"-"+ dependencyTypeGeneralization
							+File.separator + corpusName
							+ "-folds");
//					File outDir = new File(inputFile.getParent() + File.separator + lineStyle+ "-dep-"+qGramLength +File.separator + inputFile.getName()
//							+ "-folds");
					outDir.mkdirs();
					// define varying parameters of parents
					((SvmLightTreeKernelTransformer)this).folds = folds;
					((SvmLightTreeKernelTransformer)this).dirOut = outDir;
					((SvmLightTreeKernelTransformer)this).initializeExampleWriters( qGramMin, qGramMax, kBand );
					try {
						in = new InputStreamReader(new FileInputStream(inputFile), UTF8);
						Parser parser = new Parser(
							Collections.singleton(getTokenizer()), // tokenizer
							emptySet, // bracketing (syntax parser)
							Collections.singleton(getParser()), // dependency parser
							new DefaultElementFactory(), 
							this);
						parser.process(in);
						
					} finally {
						if (in != null) {
							in.close();
						}
					}
						
//					}
					
//					for (String dep : Parser.dependencyTypes) {
//						System.out.println("public static final String "+ toJavaIdentifier(dep) +" = \""+ dep +"\";");
//					}
//
//					for (String dep : Parser.dependencyTypes) {
//						System.out.println("dependencyGeneralizer.put("+ toJavaIdentifier(dep) +", "+ toJavaIdentifier(dep)+");");
//					}
//
//					System.exit(0);
					
	//			}
			}
			}
		}
	}
		
	public static void main(String[] args) throws Exception {
		CmdLineParser parser = new CmdLineParser();
		
		CmdLineParser.Option inFileOption  = parser.addStringOption('f', "file");
		CmdLineParser.Option outBaseDirOption = parser.addStringOption('o',"out");
		CmdLineParser.Option splitOption = parser.addStringOption('s', "split");
		CmdLineParser.Option parserOption = parser.addStringOption('p', "parser");
		CmdLineParser.Option tokenizerOption = parser.addStringOption('t', "tokenizer");
		CmdLineParser.Option qminOption = parser.addIntegerOption("qmin");
		CmdLineParser.Option qminmaxOption = parser.addIntegerOption("qminmax");
		CmdLineParser.Option qmaxminOption = parser.addIntegerOption("qmaxmin");
		CmdLineParser.Option qmaxOption = parser.addIntegerOption("qmax");
		CmdLineParser.Option kOption = parser.addIntegerOption('k', "kvalue");
		try {
	        parser.parse(args);
	    }
	    catch ( CmdLineParser.OptionException e ) {
	        printUsage();
	        System.exit(2);
	    }
	    String inFile, baseDir, split;
	    
	    inFile = (String)   parser.getOptionValue(inFileOption);
	    baseDir = (String)  parser.getOptionValue(outBaseDirOption);
	    split = (String) parser.getOptionValue(splitOption);

		Integer qmin = (Integer) parser.getOptionValue(qminOption, 2);
		Integer qmax = (Integer) parser.getOptionValue(qmaxOption, 2);
		Integer qminmax = (Integer) parser.getOptionValue(qminmaxOption, qmax);
		Integer qmaxmin = (Integer) parser.getOptionValue(qmaxminOption, qmin); 
		Integer k = (Integer) parser.getOptionValue(kOption, 0);
		
		
	    if(inFile==null || baseDir==null || split == null){
	    	printUsage();
	        System.exit(2);
	    }
		if ( qmin < 0 || qmin > 5 ){
			qmin = 2;
			System.err.println("Warning: qmin was out of range [1,5], now is set to default: " + qmin );
		}
		if ( qmax < 0 || qmax > 5 ){
			qmax = 2;
			System.err.println("Warning: qmax was out of range [1,5], now is set to default: " + qmax );
		}
		if ( k < 0 || k > 2){
			k = 0;
			System.err.println("Warning: k was out of range [0,2], now set to default: " + k );
		}
	    if ( qmin > qminmax )
	    {
	    	qminmax = qmin;
	    	System.err.println("Warning: qmin was greater than qminmax, now both are set to: " + qmin );
	    }
	    if ( qmaxmin > qmax )
	    {
	    	qmaxmin = qmax;
	    	System.err.println("Warning: qmaxmin was greater than qmax, now both are set to: " + qmax );
	    }
	    
	    final String depParser = (String) parser.getOptionValue(parserOption, LearningFormatConstants.CHARNIAK_LEASE_PARSER);
	    final String tokenizer = (String) parser.getOptionValue(tokenizerOption, LearningFormatConstants.CHARNIAK_LEASE_TOKENIZER);
	    
		SvmLightDependencyTreeKernelTransformer tf = new SvmLightDependencyTreeKernelTransformer(
				tokenizer,
				depParser,
				qmin, qminmax, qmaxmin, qmax, k);
	    
//		SvmLightDependencyTreeKernelTransformer me=
//			new SvmLightDependencyTreeKernelTransformer(
//				(Integer) parser.getOptionValue(parser.getOptionValue(qminOption, 2),
//				(Integer) parser.getOptionValue(qmaxOption, 2), 
//				(Integer) parser.getOptionValue(kOption, 0));	 
		tf.run(inFile, split, baseDir);
	}
	
//	private static String toJavaIdentifier(String str) {
//		return str.replace('.', '_').replace("&", "amp").replace("+", "plus_").replace("/", "slash").replace("-", "minus");
//	}
	
	@Override
	protected ExampleWriter createExampleWriter( int qGramMin, int qGramMax, int kBand ) {
		switch (format) {
		case b:
			System.out.println("Parser: " + getParser() + ", qmin: " + qGramMin + ", qmax: " + qGramMax + ", kBand: " + kBand + ", lpolicy: " + lengthsPolicy);
			return new PathBandExampleWriter(getParser(), qGramMin, qGramMin, kBand, lengthsPolicy);
		case c:
			return new EntityContextExampleWriter(getParser(), qGramLengthMax, lengthsPolicy, entityPosition, selfReferences);
		default:
			throw new IllegalStateException();
		}
	}
}
