package org.learningformat.api;

import org.learningformat.impl.DefaultElementFactory;

public abstract class ElementFactory {
	
	public static final String ELEMENT_FACTORY_PROPERTY = "org.unifiedformat.api.ElementFactory";
	
	public abstract Bracketing createBracketing();
	
	public abstract CharOffsetMapEntry createCharOffsetMapEntry();
	public abstract Corpus createCorpus();
	public abstract Dependency createDependency();
	public abstract DependencyToken createDependencyToken();
	public abstract Document createDocument();
	public abstract Entity createEntity();
	public abstract Pair createInteraction();
	
	public abstract Parse createParse();
	public abstract Sentence createSentence();
	public abstract Token createToken();

	public abstract Tokenization createTokenization();

	public ElementFactory newInstance() throws ClassNotFoundException, InstantiationException, IllegalAccessException {
		String className = System.getProperty(ELEMENT_FACTORY_PROPERTY);
		ElementFactory result = null;
		
		if (className != null){
			Class<?> cl = Class.forName(className);
			if (cl != null) {
				result = (ElementFactory) cl.newInstance();
			}
		}
		if (result == null) {
			result = new DefaultElementFactory();
		}
		return result;
	}

}
