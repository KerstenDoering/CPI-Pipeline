package org.learningformat.transform.dependency.transformer;

import org.learningformat.transform.dependency.DependencyGraph;


public interface DependencyGraphTransformer {

	DependencyGraph transform(DependencyGraph dg);
	
}
