package org.learningformat.transform.dependency.transformer;

import java.util.Collections;
import java.util.HashSet;
import java.util.Set;

import org.learningformat.transform.dependency.DependencyGraph;
import org.learningformat.transform.dependency.DependencyGraph.DependencyData;

/**
 * A dummy example to show how a transformer actually works
 * @author philippe
 *
 */
public class EdgeRemoverTransformer  implements DependencyGraphTransformer {
	
	Set<String> dependencyTypesToRemove;

	/**
	 * Empty constructor with <b>det</b> as toy example
	 */
	public EdgeRemoverTransformer() {
		this(Collections.singleton("det"));			
	}
	
	
	/**
	 * Removes all edges contained in the set 
	 * @param dependencyTypesToRemove
	 */
	public EdgeRemoverTransformer(Set<String> dependencyTypesToRemove) {
		super();
		this.dependencyTypesToRemove = dependencyTypesToRemove;
	}
	
	@Override
	public DependencyGraph transform(DependencyGraph dg) {
		// provide name
		dg.setName(dg.getName()+"_edgeRemove");
		
		// collect
		Set<DependencyData> edgesToRemove = new HashSet<DependencyData>();
		for (DependencyData d : dg.getGraph().edgeSet())
			if (dependencyTypesToRemove.contains(d.getType()))
				edgesToRemove.add(d);
		
		// remove
		for (DependencyData d : edgesToRemove)
			dg.getGraph().removeEdge(d);
		
		return dg;
	}

}
