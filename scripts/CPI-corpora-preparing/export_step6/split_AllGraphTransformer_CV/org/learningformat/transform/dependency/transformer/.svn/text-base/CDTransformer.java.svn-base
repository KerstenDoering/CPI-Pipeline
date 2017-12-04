package org.learningformat.transform.dependency.transformer;

import java.util.HashSet;
import java.util.Set;

import org.jgrapht.DirectedGraph;
import org.learningformat.api.Token;
import org.learningformat.transform.dependency.DependencyGraph;
import org.learningformat.transform.dependency.DependencyGraph.DependencyData;

/**
 * Class transforms a depency Tree by removing irrelevant edges, like nn and appos depencies and 
 * shortcutting them with the ancestors
 * 
 * @author philippe
 *
 */
public class CDTransformer implements DependencyGraphTransformer{

	private boolean nn=false;
	private boolean appos=false;
	private Set<String> collaps = new HashSet<String>();
	
	public CDTransformer(boolean nn, boolean appos) {
		super();
		this.nn = nn;
		this.appos = appos;
		setCollaps();
	}
	
	/**
	 * Dummy constructor which setts both collapsings to true
	 */
	public CDTransformer(){
		super();
		this.nn=true;
		this.appos = true;
		setCollaps();
	}
	

	//Does this affect something when executed recoursively?
	@Override	
	public DependencyGraph transform(DependencyGraph dg) {

		dg.setName("CD_" +(nn?"n_":"") +(appos?"a":"") );
		DirectedGraph<Token, DependencyData> graph = dg.getGraph();
		
		Set<Token> remove = new HashSet<Token>();
		for(DependencyData edge:graph.edgeSet()){//Iterate Edges
			
			if(collaps.contains(edge.getType())){	//Candidate for removal
			
				Token source= graph.getEdgeSource(edge);
				Token target= graph.getEdgeTarget(edge);
				
				if(!source.isEntity() && target.isEntity()) { //TODO: First part of criterion does make sense, but the second part?					
					remove.add(source);	
					System.out.println("Removed " +source.getId() +" ");
				}				
			}
		}
		
		//Now modify the graph
		for(Token token:remove){
			Set<DependencyData> inEdges  = graph.incomingEdgesOf(token);
			Set<DependencyData> outEdges = graph.outgoingEdgesOf(token);
			
			//Propagate the new edges; 
			//TODO Currently we propage new edges, but maybe we should do this only fopr inDegree=1?
			for (DependencyData inEdge:inEdges){
				for(DependencyData outEdge:outEdges){
					graph.addEdge(graph.getEdgeSource(inEdge), graph.getEdgeTarget(outEdge), new DependencyData(inEdge.getId(), inEdge.getType()));
				}
			}
		}
		
		//Now remove the edges
		for(Token token:remove){
			graph.removeVertex(token);
		}
		
		return dg;
	}
	
	private void setCollaps(){
		if(nn)
			collaps.add("nn");
		
		if(appos)
			collaps.add("appos");
	}

}
