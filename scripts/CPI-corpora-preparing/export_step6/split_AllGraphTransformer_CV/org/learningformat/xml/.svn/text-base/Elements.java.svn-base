package org.learningformat.xml;

import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.NoSuchElementException;
import java.util.Set;

public class Elements {
	public static final String corpus = "corpus";
	public static final String dependency = "dependency";
	public static final String document = "document";
	public static final String entity = "entity";
	public static final String pair = "pair";
	public static final String parse = "parse";
	public static final String parses = "parses";
	public static final String sentence = "sentence";
	public static final String sentenceanalyses = "sentenceanalyses";
	public static final String token = "token";
	public static final String tokenization = "tokenization";
	public static final String tokenizations = "tokenizations";
	public static final String bracketing = "bracketing";
	public static final String bracketings = "bracketings";
	public static final String charOffsetMapEntry = "charOffsetMapEntry";

	public static final Map<String, Set<String>> ALLOWED_ATTRIBUTES = new HashMap<String, Set<String>>(12);
	static {
		Set<String> s = null;
		s = new HashSet<String>(2);
		s.add(Attributes.cvsVersion);
		s.add(Attributes.source);
		ALLOWED_ATTRIBUTES.put(Elements.corpus, s);

		s = new HashSet<String>(4);
		s.add(Attributes.id);
		s.add(Attributes.t1);
		s.add(Attributes.t2);
		s.add(Attributes.type);
		s.add(Attributes.origId);
		ALLOWED_ATTRIBUTES.put(Elements.dependency, s);

		s = new HashSet<String>(4);
		s.add(Attributes.PMID);
		s.add(Attributes.id);
		s.add(Attributes.origID);
		s.add(Attributes.origId);
		ALLOWED_ATTRIBUTES.put(Elements.document, s);

		s = new HashSet<String>(7);
		s.add(Attributes.charOffset);
		s.add(Attributes.id);
		s.add(Attributes.origID);
		s.add(Attributes.origId);
		s.add(Attributes.seqId);
		s.add(Attributes.text);
		s.add(Attributes.type);
		ALLOWED_ATTRIBUTES.put(Elements.entity, s);

		s = new HashSet<String>(4);
		s.add(Attributes.e1);
		s.add(Attributes.e2);
		s.add(Attributes.id);
		s.add(Attributes.origId);
		s.add(Attributes.interaction);
		s.add(Attributes.type);
		ALLOWED_ATTRIBUTES.put(Elements.pair, s);

		s = new HashSet<String>(2);
		s.add(Attributes.parser);
		s.add(Attributes.tokenizer);
		ALLOWED_ATTRIBUTES.put(Elements.parse, s);

		s = new HashSet<String>(3);
		s.add(Attributes.parser);
		s.add(Attributes.tokenizer);
		s.add(Attributes.bracketing);
		ALLOWED_ATTRIBUTES.put(Elements.bracketing, s);

		s = new HashSet<String>(2);
		s.add(Attributes.sentenceTextCharOffset);
		s.add(Attributes.bracketingCharOffset);
		ALLOWED_ATTRIBUTES.put(Elements.charOffsetMapEntry, s);

		s = new HashSet<String>(0);
		ALLOWED_ATTRIBUTES.put(Elements.parses, s);

		s = new HashSet<String>(5);
		s.add(Attributes.id);
		s.add(Attributes.origID);
		s.add(Attributes.origId);
		s.add(Attributes.seqId);
		s.add(Attributes.text);
		s.add(Attributes.charOffset);// added for wider usability
		ALLOWED_ATTRIBUTES.put(Elements.sentence, s);

		s = new HashSet<String>(0);
		ALLOWED_ATTRIBUTES.put(Elements.sentenceanalyses, s);

		s = new HashSet<String>(4);
		s.add(Attributes.POS);
		s.add(Attributes.charOffset);
		s.add(Attributes.id);
		s.add(Attributes.text);
		ALLOWED_ATTRIBUTES.put(Elements.token, s);

		s = new HashSet<String>(1);
		s.add(Attributes.tokenizer);
		ALLOWED_ATTRIBUTES.put(Elements.tokenization, s);
	
		ALLOWED_ATTRIBUTES.put(Elements.bracketings, Collections.<String>emptySet());
		ALLOWED_ATTRIBUTES.put(Elements.tokenizations, Collections.<String>emptySet());
		ALLOWED_ATTRIBUTES.put(Elements.bracketings, Collections.<String>emptySet());

		s = null;
	}

	public static void checkAttributes(String element, org.xml.sax.Attributes attributes) {
		if (attributes == null)
			return;
		Set<String> allowed = ALLOWED_ATTRIBUTES.get(element);
		if (allowed == null)
			throw new NoSuchElementException("Unknown XML element '"+ element+"'");
		for (int i = 0; i < attributes.getLength(); i++) {
			if (attributes.getLocalName(i) != null && !allowed.contains(attributes.getLocalName(i))) {
				System.err.println("ATTRIBUTE: " + attributes.toString());
				throw new IllegalStateException("Unexpected attribute '"+ attributes.getLocalName(i) +"' for element '"+ element +"'.");
			}
		}
	}
}
