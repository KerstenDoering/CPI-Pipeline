package org.learningformat.standoff;

import static org.learningformat.standoff.StandoffParser.toSingleCharOffset;

import org.learningformat.api.Entity;
import org.learningformat.api.Pair;
import org.learningformat.api.Sentence;
import org.learningformat.impl.DefaultPair;


/**
 * Class to populate {@link Sentence}s having {@link Entity}s with {@link Pair}s. 
 * @author illes
 *
 */
public class PairGenerator {

	enum PairClassification {
		/**
		 * Not an interaction. 
		 */
		FALSE,
		
		/**
		 * An interaction. 
		 */
		TRUE,
		
		/**
		 * Exclude from output. 
		 */
		IGNORE;
		
		/**
		 * Convenience method.
		 * 
		 * @param whether the pair is an interaction
		 * @return {@link #TRUE} or {@link #FALSE}
		 */
		static PairClassification fromBoolean(boolean b) {
			return b ? TRUE : FALSE;
		}
		
		/**
		 * Convenience method
		 * @return
		 * @throws IllegalArgumentException iff <pre><code>this == {@link #IGNORE}</code></pre> 
		 */
		boolean toBoolean() throws IllegalArgumentException {
			if (this == TRUE)
				return true;
			if (this == FALSE)
				return false;
			throw new IllegalArgumentException("not boolean: " + this);
		}
	}

	/**
	 * Interface for classifying entity pairs.
	 * @author illes
	 *
	 */
	public interface PairClassifier {
		PairClassification classify(Entity e1, Entity e2);
	}
	
	/**
	 * Ignores entities in reverse (e2 before e1) order. 
	 * @author illes
	 *
	 */
	public static class OrderedPairClassifier implements PairClassifier
	{
		final PairClassification output;
		
		public OrderedPairClassifier(boolean output) {
			this.output = PairClassification.fromBoolean(output);
		}
		
		@Override
		public PairClassification classify(Entity e1, Entity e2) {
			if (wrongOrder(e1, e2))
				return PairClassification.IGNORE;
			return output;
		}
		
		protected static boolean wrongOrder(Entity e1, Entity e2)
		{
			return toSingleCharOffset(e1).compareTo(toSingleCharOffset(e2)) <= 0;
		}
	}

	/**
	 * Helper method to apply a {@link PairClassifier} to every possible {@link Entity} pair in a {@link Sentence}.
	 * @param s
	 * @param c
	 * @return the number of {@link Pair}s added.
	 */
	static int addClassiedPairs(Sentence s, PairClassifier c)
	{
		int added = 0;
		for (Entity e1 : s.getEntities())
		{
			for (Entity e2 : s.getEntities())
			{
				PairClassification r = c.classify(e1, e2);
				if (r == PairClassification.IGNORE)
					continue;
				
				Pair ppi = new DefaultPair();
				ppi.setE1(e1);
				ppi.setE2(e2);
				ppi.setInteraction(r.toBoolean());
				ppi.setId(s.getId() +".p" + s.getAllPairs().size());
				
				s.addInteraction(ppi);
				added++;
			}
		}
		return added;
	}
	
}
