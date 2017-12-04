package org.learningformat.xml;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.Reader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Hashtable;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;

import javax.xml.parsers.ParserConfigurationException;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Result;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.TransformerFactoryConfigurationError;
import javax.xml.transform.sax.SAXSource;
import javax.xml.transform.stream.StreamResult;

import org.learningformat.api.Bracketing;
import org.learningformat.api.CharOffset;
import org.learningformat.api.CharOffsetMapEntry;
import org.learningformat.api.Corpus;
import org.learningformat.api.Dependency;
import org.learningformat.api.DependencyToken;
import org.learningformat.api.Document;
import org.learningformat.api.ElementFactory;
import org.learningformat.api.Entity;
import org.learningformat.api.Pair;
import org.learningformat.api.Parse;
import org.learningformat.api.Sentence;
import org.learningformat.api.Token;
import org.learningformat.api.Tokenization;
import org.learningformat.impl.DefaultElementFactory;
import org.learningformat.util.FileHelper;
import org.xml.sax.Attributes;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;
import org.xml.sax.XMLFilter;
import org.xml.sax.XMLReader;
import org.xml.sax.helpers.XMLFilterImpl;

public class Parser {
	
	
	private final Set<String> dependencyTypes = new TreeSet<String>();

	@Override
	public String toString() {
		return Integer.toString(dependencyTypes.size()) ;
	}
	
	/**
	 * Set whether to try to continue after encountering inconsistencies inn the corpus.
	 *  
	 * @note May lead to other errors, use at own risk.
	 */
	public void setTryToRecoverFromErrors(boolean tryToRecoverFromErrors) {
		this.tryToRecoverFromErrors = tryToRecoverFromErrors;
	}
	

	/**
	 * Try to continue after encountering inconsistencies inn the corpus. 
	 * @note May lead to other errors, use at own risk.
	 */
	private boolean tryToRecoverFromErrors = false;
	
	public static String getOrigId(Attributes attributes) {
		String result = attributes.getValue(org.learningformat.xml.Attributes.origId);
		if (result == null) {
			result = attributes.getValue(org.learningformat.xml.Attributes.origID);
		}
		return result;
	}
	
	@SuppressWarnings("serial")
	public static class CorpusInconsitencyException extends Exception {
		
		public CorpusInconsitencyException() {
			super();
		}
		
		public CorpusInconsitencyException(String message) {
			super(message);
		}
		
		public CorpusInconsitencyException(String message, Throwable cause) {
			super(message, cause);
		}
	}
	
	private static class DependencyInfo  {

		protected String id;
		protected String id1;
		protected String id2;
		protected String type;

	
		
		public DependencyInfo(String id, String id1, String id2, String type) {
			super();
			this.id = id;
			this.id1 = id1;
			this.id2 = id2;
			this.type = type;
		}

		@SuppressWarnings("unused")
		public DependencyInfo(Dependency dep) {
			this.id = dep.getId();
			this.id1 = dep.getT1().getId();
			this.id2 = dep.getT2().getId();
			this.type = dep.getType();
		}

		public String getId() {
			return id;
		}

		public String getId1() {
			return id1;
		}

		public String getId2() {
			return id2;
		}

		public String getType() {
			return type;
		}

	}

	protected class LearningFormatHandler extends XMLFilterImpl implements
			org.learningformat.xml.Attributes {
		
		protected class ParseInfo {

			protected List<DependencyInfo> dependencyInfos = new ArrayList<DependencyInfo>(16);
			protected final Parse parse;
			protected final String tokenizer;
			
			public ParseInfo(String tokenizer, Parse parse) {
				super();
				this.parse = parse;
				this.tokenizer = tokenizer;
			}

			public void addDependencyInfo(DependencyInfo idDependency) {
				dependencyInfos.add(idDependency);
			}

			public void completeParse(Tokenization tokenization) throws CorpusInconsitencyException {
				parse.setTokenization(tokenization);
				
				List<Token> tokens = tokenization.getTokens();
				Map<String, DependencyToken> tokenMap = new Hashtable<String, DependencyToken>(tokens.size() + (tokens.size() / 3) + 1);
				for (Token token : tokens) {
					if (!(token instanceof DependencyToken)) {
						throw new InternalError("Token not an instance of DependencyToken.");
					}
					tokenMap.put(token.getId(), (DependencyToken)token);
				}
				
				for (DependencyInfo di : dependencyInfos) {
					DependencyToken governor = tokenMap.get(di.getId1());
					if (governor == null) {
						throw new CorpusInconsitencyException("No parent found for id '"+ di.getId1() +"' in dependency '"+ di.getId() +"'." +getCurrentSentence().getId());
					}
					DependencyToken dependent = tokenMap.get(di.getId2());
					if (dependent == null) {
						throw new CorpusInconsitencyException("No child found for id '"+ di.getId2() +"' in dependency '"+ di.getId() +"'." +getCurrentSentence().getId());
					}
					
					Dependency dependency = elementFactory.createDependency();
					dependency.setId(di.getId());
					dependency.setT1(governor);
					dependency.setT2(dependent);
					dependency.setType(di.getType());
					
					parse.addDependency(dependency);
					governor.addDependent(dependency);
					dependent.addGovernor(dependency);
					
				}
			}

			public Parse getParse() {
				return parse;
			}

			public String getTokenizer() {
				return tokenizer;
			}

			public void removeDependencyInfo(DependencyInfo idDependency) {
				dependencyInfos.remove(idDependency);
			}

//			public void setParse(Parse parse) {
//				this.parse = parse;
//			}
			
//			public void setTokenizer(String tokenizer) {
//				this.tokenizer = tokenizer;
//			}

		}

		private final Map<String, Bracketing> bracketingMap;
		private Bracketing currentBracketing;
		private Corpus currentCorpus;
		private Document currentDocument;
		private ParseInfo currentParseInfo;
		private Sentence currentSentence;

		private Tokenization currentTokenization;
		private Map<String, Map<String, ParseInfo>> dependencyInfoMap;
		
		
		
		public LearningFormatHandler() {
			if (readParses == null || readParses.size() > 0) {
				dependencyInfoMap = new HashMap<String, Map<String, ParseInfo>>();
			}
			else
				dependencyInfoMap = null;
			
			if (readBracketings == null || readBracketings.size() > 0) {
				bracketingMap = new HashMap<String, Bracketing>();
			}
			else
				bracketingMap = null;
		}

		protected void emitEndElement(String uri, String localName, String name)
		throws SAXException {
			super.endElement(uri, localName, name);
		}
		
		@Override
		public void endElement(String uri, String localName, String name)
				throws SAXException {
			try {
				if (Elements.corpus.equals(name)) {
					corpusListener.endCorpus();
					currentCorpus = null; // be GC friendly
				} else if (Elements.bracketing.equals(name)) {
					currentBracketing = null; // be GC friendly
				} else if (Elements.bracketings.equals(name)) {
				} else if (Elements.charOffsetMapEntry.equals(name)) {
				} else if (Elements.dependency.equals(name)) {
				} else if (Elements.document.equals(name)) {
					corpusListener.endDocument();
					if (currentDocument == null) 
						throw new InternalError("document should not be null");
					// is the document to be removed from the corpus?
					if (immediatelyRemoveDocuments && currentDocument.getCorpus() == currentCorpus) 
					{
						currentCorpus.getDocuments().remove(currentDocument);
						currentDocument.setCorpus(null);
					}
					currentDocument = null; // be GC friendly
				} else if (Elements.entity.equals(name)) {
				} else if (Elements.pair.equals(name)) {
				} else if (Elements.parse.equals(name)) {
					currentParseInfo = null;
				} else if (Elements.parses.equals(name)) {
				} else if (Elements.sentence.equals(name)) {
					corpusListener.processSentence(getCurrentSentence());
					currentSentence = null; // currentDocument still holds a reference
				} else if (Elements.sentenceanalyses.equals(name)) {
					if (dependencyInfoMap != null && dependencyInfoMap.size() > 0) {
						/* all dependencyInfoMap elements should 
						 * already have been removed at this point */
						if (tryToRecoverFromErrors)
							dependencyInfoMap.clear();
						else
							throw new InternalError("dependencyInfoMap not empty (" + Arrays.toString(dependencyInfoMap.keySet().toArray())+")");
					}
					if (bracketingMap != null && bracketingMap.size() > 0) {
						/* all bracketingInfoMap elements should 
						 * already have been removed at this point */
						if (tryToRecoverFromErrors)
							bracketingMap.clear();
						else
							throw new InternalError("bracketingInfoMap not empty (" + Arrays.toString(bracketingMap.keySet().toArray())+")");
					}
				} else if (Elements.token.equals(name)) {
				} else if (Elements.tokenization.equals(name)) {
					if (currentTokenization != null) {
						if (dependencyInfoMap != null) {
							Map<String, ParseInfo> pis = dependencyInfoMap.remove(currentTokenization.getTokenizer());
							if (pis != null) {
								for (ParseInfo pi : pis.values())
								{
									pi.completeParse(currentTokenization);
									Parse p = pi.getParse();
									getCurrentSentence().addParse(p);
								}
							}
						}
						
						if (bracketingMap != null) {
							Bracketing b = bracketingMap.remove(currentTokenization.getTokenizer());
							if (b != null) {
								b.setTokenization(currentTokenization);
								getCurrentSentence().addBracketing(b);
							}
						}
					}
					currentTokenization = null;
				} else if (Elements.tokenizations.equals(name)) {
				} else {
					throw new SAXException("Parser: unrecognized element: " + name);
				}
			} catch (CorpusInconsitencyException e) {
				if (!tryToRecoverFromErrors)
					throw new SAXException(e);
				else 
					e.printStackTrace();				
			}
		}

		protected void emitStartElement(String uri, String localName, String name, Attributes attributes) throws SAXException {
			super.startElement(uri, localName, name, attributes);
		}

		
		@Override
		public void startElement(String uri, String localName, String name, Attributes attributes) throws SAXException {
			Elements.checkAttributes(name, attributes);
			try {
				if (Elements.corpus.equals(name)) {
					if (currentCorpus != null)
						throw new IllegalStateException("nested " + Elements.corpus + " elements ('" + attributes.getValue(id) +"' inside '" + currentCorpus.getId() + "')");
					currentCorpus = elementFactory.createCorpus();
					currentCorpus.setId(attributes.getValue(id));
					currentCorpus.setSource(attributes.getValue(source));
					corpusListener.startCorpus(currentCorpus);
				} else if (Elements.bracketing.equals(name)) {
					String parserName = attributes.getValue(parser);
					if (readBracketings == null || readBracketings.contains(parserName)) {
						currentBracketing = elementFactory.createBracketing();
						currentBracketing.setParser(parserName);
						currentBracketing.setBracketing(attributes.getValue(bracketing));
						
						String tokenizerName = attributes.getValue(tokenizer);
						
						bracketingMap.put(tokenizerName, currentBracketing);
	
					}
	
				} else if (Elements.bracketings.equals(name)) {
				} else if (Elements.charOffsetMapEntry.equals(name)) {
					if (currentBracketing != null) {
						CharOffsetMapEntry en = elementFactory.createCharOffsetMapEntry();
						
						en.setBracketingCharOffset(CharOffset.parseSingle(attributes.getValue(org.learningformat.xml.Attributes.bracketingCharOffset)));
						en.setSentenceTextCharOffset(CharOffset.parseSingle(attributes.getValue(org.learningformat.xml.Attributes.sentenceTextCharOffset)));
						currentBracketing.addCharOffsetMapEntry(en);
					}
					
				} else if (Elements.dependency.equals(name)) {
					if (currentParseInfo != null) {
						DependencyInfo di = new DependencyInfo(
								attributes.getValue(id),
								attributes.getValue(t1),
								attributes.getValue(t2),
								attributes.getValue(type)
						);
						currentParseInfo.addDependencyInfo(di);
						
						dependencyTypes.add(di.getType());
					}
				} else if (Elements.document.equals(name)) {
					if (currentDocument != null)
						throw new IllegalStateException("nested " + Elements.document + " elements ('" + attributes.getValue(id) +"' inside '" + currentDocument.getId() + "')");
					currentDocument = elementFactory.createDocument();
					currentDocument.setCorpus(currentCorpus);
					currentDocument.setId(attributes.getValue(id));
					currentDocument.setOrigId(getOrigId(attributes));
					corpusListener.startDocument(currentDocument);
				} else if (Elements.entity.equals(name)) {
					Entity en = elementFactory.createEntity();
					en.setId(attributes.getValue(id));
					en.setCharOffset(CharOffset.parse(attributes
							.getValue(charOffset)));
					en.setOrigId(getOrigId(attributes));
					en.setText(attributes.getValue(text));
					en.setType(attributes.getValue(type));
	
					getCurrentSentence().addEntity(en);
				} else if (Elements.pair.equals(name)) {
					Pair in = elementFactory.createInteraction();
					in.setId(attributes.getValue(id));
					in.setInteraction(Boolean.parseBoolean(attributes
							.getValue(interaction)));
	
					in.setType(attributes.getValue(type));
					in.setOrigId(getOrigId(attributes));
					{
						final String eid = attributes.getValue(e1);
						if (eid == null) {
							throw new CorpusInconsitencyException(
									"e1 not set for interaction " + in.getId());
						}
						final Entity en = getCurrentSentence().findEntity(eid);
						if (en == null) {
							throw new CorpusInconsitencyException("No such entity "
									+ in.getId() + " in sentence "
									+ getCurrentSentence().getId());
						}
						in.setE1(en);
					}
					{
						final String eid = attributes.getValue(e2);
						if (eid == null) {
							throw new IllegalStateException(
									"e2 not set for interaction " + in.getId());
						}
						final Entity en = getCurrentSentence().findEntity(eid);
						if (en == null) {
							throw new CorpusInconsitencyException("No such entity "
									+ in.getId() + " in sentence "
									+ getCurrentSentence().getId());
						}
						in.setE2(en);
					}
	
					getCurrentSentence().addInteraction(in);
				} else if (Elements.parse.equals(name)) {
					String parserName = attributes.getValue(parser);
					if (readParses == null || readParses.contains(parserName)) {
						Parse p = elementFactory.createParse();
						p.setParser(parserName);
						String tokenizerName = attributes.getValue(tokenizer);
						currentParseInfo = new ParseInfo(tokenizerName, p);
						if (!dependencyInfoMap.containsKey(tokenizerName))
							dependencyInfoMap.put(tokenizerName, new HashMap<String, ParseInfo>());
						if(dependencyInfoMap.get(tokenizerName).put(currentParseInfo.getParse().getParser(), currentParseInfo) != null)
							throw new CorpusInconsitencyException("Duplicate parse '" + currentParseInfo.getParse().getParser() + "' for tokenizer '" + tokenizerName + "'");
					}
				} else if (Elements.parses.equals(name)) {
				} else if (Elements.sentence.equals(name)) {
					currentSentence = elementFactory.createSentence();
					getCurrentSentence().setId(attributes.getValue(id));
					getCurrentSentence().setDocument(currentDocument);
					getCurrentSentence().setOrigId(attributes.getValue(getOrigId(attributes)));
					getCurrentSentence().setText(attributes.getValue(text));
				} else if (Elements.sentenceanalyses.equals(name)) {
				} else if (Elements.token.equals(name)) {
					if (currentTokenization != null) {
						Token t = readParses == null || readParses.size() > 0 ? elementFactory
								.createDependencyToken()
								: elementFactory.createToken();
	
						t.setId(attributes.getValue(id));
						t.setCharOffset(CharOffset.parse(attributes
								.getValue(charOffset)));
						t.setText(attributes.getValue(text));
						t.setPos(attributes.getValue(POS));
	
						List<Entity> entities = getCurrentSentence().getEntities();
						if (entities != null && entities.size() > 0) {
							for (Entity en : entities) {
								if (en.getCharOffset().overlaps(t.getCharOffset())) {
									t.setEntity(en);
	//								break;
								}
							}
						}
						
						currentTokenization.addToken(t);
					} else {
						// noop: ignore token 
					}
				} else if (Elements.tokenization.equals(name)) {
					String tokenizerName = attributes.getValue(tokenizer);
					if (readTokenizations == null
							|| readTokenizations.contains(tokenizerName)) {
						currentTokenization = elementFactory.createTokenization();
						currentTokenization.setTokenizer(tokenizerName);
						getCurrentSentence().addTokenization(currentTokenization);
					}
				} else if (Elements.tokenizations.equals(name)) {
				} else {
					throw new SAXException("Parser: unrecognized element: " + name);
				}
			} catch (CorpusInconsitencyException e) {
				if (!tryToRecoverFromErrors)
					throw new SAXException(e);
				else 
					e.printStackTrace();
			}
			
		}

		public Sentence getCurrentSentence() {
			return currentSentence;
		}
	}
	
	/**
	 * Save memory by not collecting references to each object through a corpus object. 
	 */
	private boolean immediatelyRemoveDocuments;
	

	public void setImmediatelyRemoveDocuments(boolean remove) {
		this.immediatelyRemoveDocuments = remove;
	}
	
	/**
	 * Simple possibility to test. Command line arguments are supposed to be
	 * files.
	 * 
	 * @param args
	 */
	public static void main(String[] args) {

		try {
			org.learningformat.xml.Parser parser = new org.learningformat.xml.Parser(
					new org.learningformat.xml.CorpusListener() {

						@Override
						public void endCorpus() {
							System.out.println("Corpus end");
						}

						@Override
						public void endDocument() {
							System.out.println("Document end");
						}

						@Override
						public void processSentence(Sentence sentence) {
							System.out.println("Sentence beginnig");
							System.out.println(sentence.getId());
							List<Pair> posPairs = sentence.getPositivePairs();
							for (Pair pair : posPairs) {
								// do something with the pair
								System.out.println(pair.getE1().getType());
							}
						}

						@Override
						public void startCorpus(Corpus corpus) {
							System.out.println("Corpus " + corpus.getSource()
									+ " started.");
						}

						@Override
						public void startDocument(Document document) {
							System.out.println("Document " + document.getId()
									+ " started.");
						}

					});
			for (String arg : args) {
				parser.process(new FileInputStream(new File(arg)));
			}

		} catch (Exception e) {
			e.printStackTrace();
			System.exit(1);
		}

	}

	protected final CorpusListener corpusListener;

	protected final ElementFactory elementFactory;



	private final XMLFilter handler;

	protected final Set<String> readBracketings;
	/**
	 * null ... read all available parses<br>
	 * empty set ... ignore all parses set ... read only named parses
	 */
	protected final Set<String> readParses;
	
	/**
	 * null ... read all available tokenizations
	 * <br>
	 * empty set ... ignore all tokenisations 
	 * <br>
	 * set ... read only named tokenizations
	 */
	protected final Set<String> readTokenizations;

	protected SAXParser saxParser;

	public Parser(CorpusListener corpusListener)
			throws ParserConfigurationException, SAXException {
		this(null, null, null, new DefaultElementFactory(), corpusListener);
	}

	/**
	 * <code>null</code> - read all available
	 * <br>
	 * empty set - ignore all 
	 * <br>
	 * non-empty set - read only specified
	 */
	public Parser(
			Set<String> readTokenizations, 
			Set<String> readBracketings,
			Set<String> readParses,
			ElementFactory elementFactory, CorpusListener sentenceConsumer)
			throws ParserConfigurationException, SAXException {
		super();
		this.elementFactory = elementFactory;
		this.corpusListener = sentenceConsumer;
		this.readTokenizations = readTokenizations;
		this.readBracketings = readBracketings;
		this.readParses = readParses;

		SAXParserFactory saxParserFactory = SAXParserFactory.newInstance();
		saxParserFactory.setValidating(false);
		saxParser = saxParserFactory.newSAXParser();
		handler = createHandler();

	}

	protected XMLFilter createHandler() {
		return new LearningFormatHandler();
	}

	public void process(InputSource in, Result rslt) throws SAXException, IOException {
		try {
			SAXParser parser = SAXParserFactory.newInstance().newSAXParser();			
			XMLReader xmlReader = parser.getXMLReader();
			
			Transformer t = TransformerFactory.newInstance().newTransformer();
			t.setOutputProperty(OutputKeys.OMIT_XML_DECLARATION, "yes");
	 		t.setOutputProperty(OutputKeys.INDENT, "yes");
	 		t.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "2");
	 		t.setURIResolver(null);
	 		//System.err.println(("IDENTITY:" + ((TransformerImpl)t).isIdentity()));

			handler.setParent(xmlReader);
			
	 		SAXSource src = new SAXSource(handler, in);
//	 		rslt.setSystemId("file:/tmp/fifi.xml"); // NOTE: HACK

	 		t.transform(src, rslt);
		}
		catch (TransformerException e) {
			throw new SAXException(e);
		}
		catch(TransformerFactoryConfigurationError e)
		{
			throw new RuntimeException(e);
		}
		catch(ParserConfigurationException e)
		{
			throw new RuntimeException(e);
		}
	}

	/**
	 * Proccess input, discarding output.
	 * @param in
	 * @throws SAXException
	 * @throws IOException
	 */
	public void process(InputSource in) throws SAXException, IOException {
		Result r = new StreamResult(new FileHelper.NullWriter());
		//Result r = new StreamResult(new FileOutputStream("/dev/null"));
		r.setSystemId("file:/dev/null");
		//System.err.println("SYSTEM_ID: " + r.getSystemId());
		process(in, r);
	}

	
	/**
	 * Convenience method.
	 * @see #process(InputSource, Result)
	 */
	public void process(InputStream in) throws SAXException, IOException {
		if (in == null)
			throw new NullPointerException();
		
		process(new InputSource(in));
	}
	
	/**
	 * Convenience method.
	 * @see #process(InputSource, Result)
	 */
	public void process(Reader in) throws SAXException, IOException {
		if (in == null)
			throw new NullPointerException();
		
		process(new InputSource(in));	
	}
	
	/**
	 * Convenience method.
	 * @see #process(InputSource, Result)
	 */
	public void process(InputStream in, File out) throws SAXException, IOException {
		if (in == null)
			throw new NullPointerException();
		
		if (out == null)
			throw new NullPointerException();
		
		process(new InputSource(in), new StreamResult(out));
	}
	
}
