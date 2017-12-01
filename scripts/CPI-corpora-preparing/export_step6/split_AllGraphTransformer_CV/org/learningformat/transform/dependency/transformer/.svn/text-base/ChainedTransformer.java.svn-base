package org.learningformat.transform.dependency.transformer;

import org.learningformat.transform.dependency.DependencyGraph;

/**
 * Applies a sequence of {@link DependencyGraphTransformer}s to a {@link DependencyGraph}.
 * @author illes
 *
 */
public class ChainedTransformer implements DependencyGraphTransformer {
	
	final private DependencyGraphTransformer[] stages;

	
	/**
	 * 
	 * @param stages the {@link DependencyGraphTransformer}s to apply, the last one is applied first.
	 */
	public ChainedTransformer(DependencyGraphTransformer... stages) {
		this.stages = stages;
	}

	@Override
	public DependencyGraph transform(DependencyGraph dg) {
		
		for (int i = stages.length - 1; i >= 0 ; i--) {
			String name = dg.getName();
			DependencyGraph transformed = stages[i].transform(dg);
			transformed.setName(transformed.getName() + ":" + name);
			dg = transformed;
		}
		
		return dg;
	}
}
