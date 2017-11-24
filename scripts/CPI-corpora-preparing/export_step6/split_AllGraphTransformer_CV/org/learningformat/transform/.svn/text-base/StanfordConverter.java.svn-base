package org.learningformat.transform;

import java.io.IOException;
import java.io.StringReader;
import java.util.AbstractCollection;
import java.util.Collection;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.WeakHashMap;

import edu.stanford.nlp.trees.EnglishGrammaticalStructure;
import edu.stanford.nlp.trees.GrammaticalStructure;
import edu.stanford.nlp.trees.LabeledScoredTreeFactory;
import edu.stanford.nlp.trees.MemoryTreebank;
import edu.stanford.nlp.trees.PennTreeReader;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.trees.TreeGraphNode;
import edu.stanford.nlp.trees.TreeNormalizer;
import edu.stanford.nlp.trees.TreeReader;
import edu.stanford.nlp.trees.Treebank;
import edu.stanford.nlp.trees.TypedDependency;
import edu.stanford.nlp.util.Filters;


/**
 * Convert Stanford style parse trees to (collapsed) dependency trees
 * @author illes
 *
 */
public class StanfordConverter {
	
	final LabeledScoredTreeFactory lsrf =  new LabeledScoredTreeFactory();
	final MemoryTreebank tb = new MemoryTreebank(new TreeNormalizer());
	final boolean keepPunct;
	
	
	
	
	
	public StanfordConverter(boolean keepPunct) {
		super();
		this.keepPunct = keepPunct;
	}
	
	
	public static int getTokenIndex(TreeGraphNode node)
	{
		String label = node.toString();
		return Integer.parseInt(label.substring(label.lastIndexOf("-")+1));
	}
	
	public static String getWord(TreeGraphNode node)
	{
		String label = node.toString();
		return label.substring(0, label.lastIndexOf("-"));
	}
	
	public static String getDependencyType(TypedDependency td)
	{
		return td.reln().toString();
	}

	/**
	 * See {@link GrammaticalStructure#typedDependenciesCollapsed(boolean)}
	 * @param bracketing
	 * @return
	 */
	public List<TypedDependency> convertPrbToDependencies(String bracketing) 
	{
			TreeReader tr = new PennTreeReader(new StringReader(bracketing), lsrf);
			tb.clear();
			try {
				tb.add(tr.readTree());
			} catch (IOException e) {
				throw new IllegalArgumentException("error parsing bracketing: '" + bracketing +"'", e);
			}
			Collection<GrammaticalStructure> gsBank = new TreeBankGrammaticalStructureWrapper(tb, keepPunct);

			for (GrammaticalStructure gs : gsBank) {
//				Tree t;
//				if (gsBank instanceof TreeBankGrammaticalStructureWrapper) {
//					t = ((TreeBankGrammaticalStructureWrapper) gsBank)
//							.getOriginalTree(gs);
//				} else {
//					t = gs.root(); // recover tree
//				}

//				// print the grammatical structure, the basic, collapsed and
//				// CCprocessed
//
//				System.out
//						.println("============= parse tree =======================");
//				t.pennPrint();
//				System.out.println();
//
//				System.out
//						.println("------------- GrammaticalStructure -------------");
//				System.out.println(gs);
//
//				System.out
//						.println("------------- basic dependencies ---------------");
//				System.out.println(StringUtils.join(
//						gs.typedDependencies(false), "\n"));
//
//				System.out
//						.println("------------- non-collapsed dependencies (basic + extra) ---------------");
//				System.out.println(StringUtils.join(gs.typedDependencies(true),
//						"\n"));
//
//				System.out
//						.println("------------- collapsed dependencies -----------");
//				System.out.println(StringUtils.join(gs.typedDependenciesCollapsed(true), "\n"));
//
//				System.out
//						.println("------------- collapsed dependencies tree -----------");
//				System.out.println(StringUtils.join(gs
//						.typedDependenciesCollapsedTree(), "\n"));
//
//				System.out
//						.println("------------- CCprocessed dependencies --------");
//				System.out.println(StringUtils.join(gs
//						.typedDependenciesCCprocessed(true), "\n"));
//
//				System.out
//						.println("-----------------------------------------------");
//				// connectivity test
//				boolean connected = GrammaticalStructure.isConnected(gs
//						.typedDependenciesCollapsed(true));
//				System.out
//						.println("collapsed dependencies form a connected graph: "
//								+ connected);
//				if (!connected) {
//					System.out.println("possible offending nodes: "
//							+ GrammaticalStructure.getRoots(gs
//									.typedDependenciesCollapsed(true)));
//				}
			
				return gs.typedDependenciesCollapsed(true);
			}

			throw new IllegalStateException("treebank empty");
			
		}
	
//	for (TypedDependency i : gs.typedDependenciesCollapsed(true))
//	{
//		String govLabel = i.gov().toString();
//		int govHyphen = govLabel.lastIndexOf("-");
//		int govIndex = Integer.parseInt(govLabel.substring(govHyphen+1));
//		String govWord = govLabel.substring(0, govHyphen);
//		
//		System.out.println(i.reln().toString() +"\t"+ govLabel + "(" + govWord + "@" + govIndex);
//	}



	/**
	 * 
	 * 
	 * Allow a collection of trees, that is a Treebank, appear to be a
	 * collection of GrammaticalStructures.
	 * 
	 * @author danielcer
	 * @note from {@link EnglishGrammaticalStructure}
	 * @note License: GPL
	 * 
	 * 
	 */
	private static class TreeBankGrammaticalStructureWrapper extends
			AbstractCollection<GrammaticalStructure> {

		public final Treebank treebank;
		public final boolean keepPunct;
		private Map<GrammaticalStructure, Tree> origTrees = new WeakHashMap<GrammaticalStructure, Tree>();

		public TreeBankGrammaticalStructureWrapper(Treebank wrappedTreeBank,
				boolean keepPunct) {
			treebank = wrappedTreeBank;
			this.keepPunct = keepPunct;
		}

		@Override
		public Iterator<GrammaticalStructure> iterator() {
			return new gsIterator();
		}

		@SuppressWarnings("unused")
		public Tree getOriginalTree(GrammaticalStructure gs) {
			return origTrees.get(gs);
		}

		private class gsIterator implements Iterator<GrammaticalStructure> {
			Iterator<Tree> tbIterator = treebank.iterator();

			public boolean hasNext() {
				return tbIterator.hasNext();
			}

			public GrammaticalStructure next() {
				Tree t = tbIterator.next();

				GrammaticalStructure gs = (keepPunct ? new EnglishGrammaticalStructure(
						t, Filters.<String> acceptFilter())
						: new EnglishGrammaticalStructure(t));

				origTrees.put(gs, t);
				return gs;
			}

			public void remove() {
				tbIterator.remove();
			}

		}

		@Override
		public int size() {
			return treebank.size();
		}

	} // end static class TreebankGrammaticalStructureWrapper

}
