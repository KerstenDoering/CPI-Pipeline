package org.learningformat.transform;

import java.io.IOException;

import org.learningformat.api.LearningFormatConstants;
import org.learningformat.api.Pair;
import org.learningformat.api.Token;

public class AbstractExampleWriter {

	protected String getTokenLabel(Pair pair, Token token)
			throws IOException {
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
