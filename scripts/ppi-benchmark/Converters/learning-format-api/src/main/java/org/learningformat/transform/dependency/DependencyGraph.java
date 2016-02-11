/**
 * 
 */
package org.learningformat.transform.dependency;

import org.jgrapht.DirectedGraph;
import org.jgrapht.EdgeFactory;
import org.jgrapht.graph.DefaultDirectedGraph;
import org.learningformat.api.Dependency;
import org.learningformat.api.Token;

public class DependencyGraph
{
	public static class DependencyData
	{
		protected String id;
		protected String type;

		public DependencyData(String id, String type) {
			super();
			this.id = id;
			this.type = type;
		}

		public DependencyData(Dependency dep) {
			this.id = dep.getId();
			this.type = dep.getType();
		}

		public String getId() {
			return id;
		}

		public String getType() {
			return type;
		}

		public void setId(String id) {
			this.id = id;
		}

		public void setType(String type) {
			this.type = type;
		}
		
	}	
	private DirectedGraph<Token, DependencyData> graph;
	private String name;
			

	public DependencyGraph()
	{
		this(null);
	}

	public DependencyGraph(String name)
	{
		this(name,
			new DefaultDirectedGraph<Token, DependencyData>(new EdgeFactory<Token, DependencyData>() {
				@Override
				public DependencyData createEdge(Token sourceVertex,	Token targetVertex) {
					return new DependencyData(null, null);
				}}));
	}

	public DependencyGraph(String name, DirectedGraph<Token, DependencyData> graph) {
		this.graph = graph;
		this.name = name;
	}

	public DirectedGraph<Token, DependencyData> getGraph() {
		return graph;
	}

	public void setGraph(DirectedGraph<Token, DependencyData> graph) {
		this.graph = graph;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}
}