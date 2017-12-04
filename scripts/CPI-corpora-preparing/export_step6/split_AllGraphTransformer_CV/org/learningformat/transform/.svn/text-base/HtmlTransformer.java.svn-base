package org.learningformat.transform;

import java.io.IOException;

import org.learningformat.api.DependencyToken;
import org.learningformat.api.LearningFormatConstants;
import org.learningformat.api.Pair;
import org.learningformat.api.Parse;
import org.learningformat.api.Sentence;
import org.learningformat.api.Token;

public class HtmlTransformer implements ExampleWriter {

	public static final String BR = "<br>";
	public static final char SPACE = ' ';
	public static final String HTML_START = "<html><body><font face=\"Tahoma\">";
	public static final String HTML_END = "</font></body></html>";
	protected String parser;

	public HtmlTransformer(String parser) {
		super();
		this.parser = parser;
	}
	
	@Override
	public void write(Pair pair, Sentence sentence, Appendable writer) throws IOException {
		
		writer.append(HTML_START);

		Parse parse = sentence.getParse(parser);
		for (Token token : parse.getTokenization().getTokens()) {
			writer.append(SPACE);
			writeColoredToken((DependencyToken)token, pair, sentence, writer);			
		}
		writer.append(HTML_END);

	}
	
	private void writeColoredToken(DependencyToken token, Pair pair, Sentence sentence, Appendable writer) throws IOException {
		writer.append(SPACE);
		
		boolean e1 = pair.getE1().getCharOffset().overlaps(token.getCharOffset());
		boolean e2 = pair.getE2().getCharOffset().overlaps(token.getCharOffset());
		

		if (e1 && e2) {
			writer.append("<b>");
			writer.append("<font color=\"#ff0000\">");
			writeToken(token.getText(), writer);
			writer.append("</font>");
			writer.append("</b>");
		}
		else if (e1) {
			writer.append("<b>");
			writer.append("<font color=\"#0000cd\">");
			writeToken(token.getText(), writer);
			writer.append("</font>");
			writer.append("</b>");
			//writeColor("blue3", writer);
		}
		else if (e2) {
			writer.append("<b>");
			writer.append("<font color=\"#68228b\">");
			writeToken(token.getText(), writer);
			writer.append("</font>");
			writer.append("</b>");
			//writeColor("darkorchid4", writer);
		}
		else if (token.isEntity()) {
			/* do nothing */
			writer.append("<b>");
			writeToken(token.getText(), writer);
			writer.append("</b>");
		}
		else {
			writeToken(token.getText(), writer);
		}
	}

	protected void writeToken(String str, Appendable writer) throws IOException {
		writer.append(str.replace("<", "&lt;"));
	}
	
	protected String getTokenLabel(Pair pair, Token token) throws IOException {
		boolean e1 = pair.getE1().getCharOffset().overlaps(token.getCharOffset());
		boolean e2 = pair.getE2().getCharOffset().overlaps(token.getCharOffset());
		if (e1 && e2) {
			return LearningFormatConstants.PROT1_AND_PROT2;
		}
		else if (e1) {
			return LearningFormatConstants.PROT1;
		}
		else if (e2) {
			return LearningFormatConstants.PROT2;
		}
		else if (token.isEntity()) {
			return LearningFormatConstants.PROT;
		}
		else {
			return token.getText();
		}
	}
	
}
