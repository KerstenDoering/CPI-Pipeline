package org.learningformat.transform.dependency;

import java.io.IOException;
import java.io.Writer;

import org.learningformat.api.Entity;
import org.learningformat.api.Token;
import org.learningformat.transform.dependency.DependencyGraph.DependencyData;

/**
 * <code><pre>
digraph graphname {
     // The label attribute can be used to change the label of a node
     a [label="Foo"];
     // Here, the node shape is changed.
     b [shape=box];
     // These edges both have different line properties
     a -> b -> c [color=blue];
     b -> d [style=dotted];
 }
 </code></pre>
 */
public class GraphVizWriter {

	
	public static void writeDot(DependencyGraph dg, Writer w) throws IOException {
		w.write("digraph sentence {\n");
		w.write("// graph \n");
		w.write("  graph [" + label(dg.getName()) +"];\n");
		w.write("// nodes \n");
		for (Token t : dg.getGraph().vertexSet())
		{
			if(t.getEntity() != null && t.getEntity().size() != 0){	
//				String color="red";
				String color= "\"" +toRGBA(t.getEntity().iterator().next(),0.5) +"\"";
				String style= t.getEntity().size()==1?"ellipse":"polygon";
				w.write("  " + nodeLabel(t) + " [" + label(t.getText()) + "] [style=filled, " +"shape=" +style  + " ,fillcolor=" +color +"];\n");
			}
			else
				w.write("  " + nodeLabel(t) + " [" + label(t.getText()) + "];\n");
		}
		w.write("// edges \n");
		for (DependencyData e : dg.getGraph().edgeSet())
		{
			w.write("  " + 
					nodeLabel(dg.getGraph().getEdgeSource(e)) + " -> " +
					nodeLabel(dg.getGraph().getEdgeTarget(e)) + " [" + label(e.getType()) + "];\n");
		}
		w.write("}\n");
	}
	
	private static String nodeLabel(Object o)
	{
		if(o instanceof Token){
			Token token = (Token) o;
			return "n_" +token.getId();
		}
			
		
		return "n_" + Integer.toHexString(o.hashCode());
	}
	
	private static String escapeDotString(String s)
	{
		if (s == null)
			return null;
		return s.replaceAll("\"", "\\\"").replaceAll("\n", " ");
	}
	
	private static String label(String label)
	{
		return "label=\"" + escapeDotString(label) +"\"";
	}
	
	/**
	 * Generate an RGBA color to be used in color attributes in .dot file.
	 * @param o Object 
	 * @param alpha should be between 0 and 1.
	 * @return
	 */
	private static String toRGBA(Entity o, double alpha)
	{
		if (alpha < 0 || alpha > 1)
			throw new IllegalArgumentException("alpha should be between 0 and 1");
		if (o == null)
			throw new NullPointerException();
		
		int h = mix(o.getId().hashCode());
		int r = (h & 0xFF);
		int g = ((h >> 8) & 0xFF);
		int b = ((h >> 16) & 0xFF);
		int a = (int)(alpha * 256) & 0xFF;
		
		int rgba = (r << 24) | (g << 16) | (b << 8) | a;
		return String.format("#%08X", rgba);
	}
	
	/**
	 * Robert Jenkins' 32 bit integer hash function
	 * @param a
	 * @return
	 */
	private static int mix(int a)
	{
	   a = (a+0x7ed55d16) + (a<<12);
	   a = (a^0xc761c23c) ^ (a>>19);
	   a = (a+0x165667b1) + (a<<5);
	   a = (a+0xd3a2646c) ^ (a<<9);
	   a = (a+0xfd7046c5) + (a<<3);
	   a = (a^0xb55a4f09) ^ (a>>16);
	   return a;
	}		
}
