package org.learningformat.transform.dependency.transformer;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

import org.jgrapht.DirectedGraph;
import org.jgrapht.alg.DijkstraShortestPath;
import org.learningformat.api.Token;
import org.learningformat.transform.dependency.DependencyGraph;
import org.learningformat.transform.dependency.DependencyGraph.DependencyData;

/**
 * Removes dependencies with the type "conj_and" and checks if the removal leaves the graph disconnected
 * @author philippe
 *	
 *
 */
public class ConjTransformer implements DependencyGraphTransformer{

	//TODO: Maybe this makes more sense if target and source are proteins?
	//TODO: Currently this method only collapses conj_and, Needs further tests ;)
	@Override
	public DependencyGraph transform(DependencyGraph dg) {
		
		dg.setName("conj");
		DirectedGraph<Token, DependencyData> graph = dg.getGraph();
		Set<DependencyData> remove = new HashSet<DependencyData>();
		
		//Find edges which could be removed
		for(DependencyData edge:graph.edgeSet()){//Iterate Edges
			if(edge.getType().equals("conj_and")){
				remove.add(edge); 
			}
		}
		
		//Remove edges
		for (DependencyData edge:remove){
			
			Token source= graph.getEdgeSource(edge);
			Token target= graph.getEdgeTarget(edge);
			
			List<DependencyData> before=DijkstraShortestPath.findPathBetween(graph, source, target); //IN general the shortest path is 1, but there are some backreferences and therefore the shortest path is 0 i n two cases in LLL
			
			if(before.size() == 0 ) //In this case we will not remove this edge, as we can not test if this lead to a disconnectd graph
				continue;
						
			graph.removeEdge(edge);	//Remove this edge
			List<DependencyData> after=DijkstraShortestPath.findPathBetween(graph, source, target); //IN general the shortest path is 1, but there are some backreferences and therefore the shortest path is 0 i n two cases in LLL
			
			if(after == null)	//If Edge disconnected the graph, induce it again
				graph.addEdge(source, target, edge);
			
			
			//Sanity check
			after=DijkstraShortestPath.findPathBetween(graph, source, target); 
			if(after== null || after.size() < before.size() ){
				System.out.println("Error in " +this.toString() +" constraint not satisfied");
				System.exit(1);
			}
//			System.out.println("Length  " +before.size() +"-" +after.size());
			
			
		}

		return dg;
	}
	

}
