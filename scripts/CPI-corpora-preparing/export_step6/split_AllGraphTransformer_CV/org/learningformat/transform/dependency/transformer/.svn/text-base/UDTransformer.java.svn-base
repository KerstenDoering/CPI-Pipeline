package org.learningformat.transform.dependency.transformer;

import org.jgrapht.DirectedGraph;
import org.learningformat.api.Token;
import org.learningformat.transform.dependency.DependencyGraph;
import org.learningformat.transform.dependency.DependencyGraph.DependencyData;

public class UDTransformer implements DependencyGraphTransformer{

	private boolean subj;	//subj, nsubj*, csubj*
	private boolean obj;	//obj, dobj, iobj, pobj
	private boolean prep;	//prep *, agent, prepc
	private boolean nn;	//nn, appos
	

	public UDTransformer(boolean subj, boolean obj, boolean prep, boolean nn) {
		super();
		this.subj = subj;
		this.obj = obj;
		this.prep = prep;
		this.nn = nn;
	}

	public UDTransformer(){
		super();
		this.subj=true;
		this.obj=true;
		this.prep=true;
		this.nn=true;
	}

	
	@Override
	public DependencyGraph transform(DependencyGraph dg) {
		dg.setName("UD_" +(subj?"s":"") +(obj?"o":"") +(prep?"p":"") +(nn?"n":"") );
		DirectedGraph<Token, DependencyData> graph = dg.getGraph();
		for(DependencyData edge:graph.edgeSet()){//Iterate Edges
			String type = edge.getType().toLowerCase();
	
			//TODO  Check if these ifs are correct; looks good maybe xsubj not?
//			"nsubj"	10188
//			"nsubjpass"	3248
//			"xsubj"	552
//			"csubj"	38
//			"csubjpass"	16
			if(type.contains("subj"))	
				edge.setType("subj");
			
//			"dobj"	7904
//			"pobj"	560
//			"iobj"	172
			else if(type.toLowerCase().contains("obj"))
				edge.setType("obj");
			
			else if(type.contains("prep") || type.equals("agent"))
				edge.setType("prep");
			
			else if(type.equals("appos"))
				edge.setId("nn");
			
		}
		return dg;
	}

}
