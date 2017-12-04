package org.learningformat.transform;

import java.io.IOException;

import org.learningformat.api.Dependency;
import org.learningformat.api.DependencyToken;
import org.learningformat.api.LearningFormatConstants;
import org.learningformat.api.Pair;
import org.learningformat.api.Parse;
import org.learningformat.api.Sentence;
import org.learningformat.api.Token;

public class DotExampleWriter extends AbstractExampleWriter implements ExampleWriter {

	public static final char BACKSLASH = '\\';
	public static final String COLOR = "color";
	public static final String DIGRAPH = "digraph";
	public static final char EOL = '\n';
	public static final char EQUALS = '=';
	public static final char GT = '>';
	private static final String LABEL = "label";
	public static final char LEFT_BRACE = '{';
	public static final char LEFT_SQUARE_BRACKET = '[';
	public static final char MINUS = '-';
	public static final char QUOT = '"';
	public static final char RIGHT_BRACE = '}';
	public static final char RIGHT_SQUARE_BRACKET = ']';
	public static final char SEMICOLON = ';';
	public static final char SPACE = ' ';
	private int indentDepth = 0;

	protected String indentString = "  ";
	
	protected String parser;
	
	public DotExampleWriter(String parser) {
		super();
		this.parser = parser;
	}

	protected void decreaseIndent() {
		indentDepth--;
	}
	protected void increaseIndent() {
		indentDepth++;
	}
	@Override
	public void write(Pair pair, Sentence sentence, Appendable writer) throws IOException {
		
		writer.append(DIGRAPH);
		writer.append(SPACE);
		writeLiteral(pair.getId(), writer);
		writer.append(SPACE);
		writer.append(LEFT_BRACE);
		
		writer.append(EOL);
		increaseIndent();
		
		
		Parse parse = sentence.getParse(parser);

		for (Token token : parse.getTokenization().getTokens()) {
			
			DependencyToken dt = (DependencyToken) token;
			if (dt.getGovernorsCount() > 0 || dt.getDependentsCount() > 0) {
				/* only tokens with dependencies */
				
				writeIndent(writer);
				
				writeIdentifier(token.getId(), writer);
				writer.append(SPACE);
				writer.append(LEFT_SQUARE_BRACKET);
				
				String tokenLabel = getTokenLabel(pair, token);
				writeLabel(token.getText(), writer);
				
				writeEntityColor(tokenLabel, writer);
				
				writer.append(RIGHT_SQUARE_BRACKET);
				writer.append(SEMICOLON);
				writer.append(EOL);
			}
		}
		
		writer.append(EOL);
		
		/* deps */
		
		for (Dependency dep : parse.getDependencies()) {
			writeIndent(writer);
			writeIdentifier(dep.getT1().getId(), writer);
			writer.append(MINUS);
			writer.append(GT);
			writeIdentifier(dep.getT2().getId(), writer);
			writer.append(SPACE);
			writer.append(LEFT_SQUARE_BRACKET);
			writeLabel(dep.getType(), writer);
			writer.append(RIGHT_SQUARE_BRACKET);
			writer.append(SEMICOLON);
			writer.append(EOL);
		}
		
		decreaseIndent();
		writer.append(RIGHT_BRACE);
	}
	protected void writeColor(String color, Appendable writer) throws IOException {
		writer.append(COLOR);
		writer.append(EQUALS);
		writeLiteral(color, writer);
	}
	private void writeEntityColor(String tokenLabel, Appendable writer) throws IOException {
		writer.append(SPACE);
		if (LearningFormatConstants.PROT1_AND_PROT2.equals(tokenLabel)) {
			writeColor("red", writer);
		}
		else if (LearningFormatConstants.PROT1.equals(tokenLabel)) {
			writeColor("blue3", writer);
		}
		else if (LearningFormatConstants.PROT2.equals(tokenLabel)) {
			writeColor("darkorchid4", writer);
		}
		else if (LearningFormatConstants.PROT.equals(tokenLabel)) {
			/* do nothing */
			writeColor("black", writer);
		}
		else {
			writeColor("gray86", writer);
		}
	}
	protected void writeIdentifier(String str, Appendable writer) throws IOException {
		writer.append(str);
	}
	
	protected void writeIndent(Appendable writer) throws IOException {
		for (int i = 0; i < indentDepth; i++) {
			writer.append(indentString);
		}
	}
	protected void writeLabel(String str, Appendable writer) throws IOException {
		writer.append(LABEL);
		writer.append(EQUALS);
		writeLiteral(str, writer);
	}
	
	protected void writeLiteral(String str, Appendable writer) throws IOException {
		writer.append(QUOT);
		writer.append(str.replace(String.valueOf(QUOT), ""+ BACKSLASH + QUOT));
		writer.append(QUOT);
	}
	
}
