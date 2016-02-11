package org.learningformat.standoff;

import java.io.IOException;
import java.util.HashSet;
import java.util.Iterator;

import org.learningformat.api.Entity;
import org.learningformat.standoff.PairGenerator.OrderedPairClassifier;
import org.learningformat.standoff.PairGenerator.PairClassification;
import org.learningformat.standoff.PairGenerator.PairClassifier;
import org.learningformat.util.CSVDictReader;
import org.learningformat.util.UndirectedPair;
import org.learningformat.util.CSVDictReader.DictRow;

/**
 * Predicts entity mention pairs known to interact as {@link PairClassification#TRUE positive} pairs. 
 * @author illes
 *
 */
public class KnowledgeBasePairClassifier implements PairClassifier {
	
	@Override
	public PairClassification classify(Entity e1, Entity e2) {
		if (OrderedPairClassifier.wrongOrder(e1, e2))
			return PairClassification.IGNORE;
		
		final String id1 = toKBIdentifier(e1.getOrigId());
		final String id2 = toKBIdentifier(e2.getOrigId());

//		System.out.println("E1:" + id1 + " (from '" + e1.getOrigId() +"')");
//		System.out.println("E2:" + id2 + " (from '" + e2.getOrigId() +"')");

		final boolean prediction = kb.interacts(id1, id2);
		
		return PairClassification.fromBoolean(prediction);
	}
	
	final KnowledgeBase kb;
	
	public KnowledgeBasePairClassifier(KnowledgeBase kb)
	{
		this.kb = kb;
	}
	
	static String toKBIdentifier(String origId)
	{
		return origId.split("@")[0];
	}
	
	static boolean isEmpty(String str)
	{
		return str == null || str.length() == 0 || str.trim().length() == 0;
	}
	
	interface KnowledgeBase {
		boolean interacts(String id1, String id2);
		int size();
	}
	
	public static class UndirectedKnowledgeBaseEntry extends UndirectedPair<String>
	{
		public UndirectedKnowledgeBaseEntry(String id1, String id2) {
			super(id1, id2);
		}

		public String first()
		{
			return id1;
		}
		
		public String second()
		{
			return id1;
		}
	}
	
	/**
	 * Always classifies <code>(x,y)</code> the same as <code>(y,x)</code> .
	 * @author illes
	 *
	 */
	static class UndirectedKnowledgeBase implements KnowledgeBase, Iterable<UndirectedKnowledgeBaseEntry> {
		
		HashSet<UndirectedKnowledgeBaseEntry> kb = new HashSet<UndirectedKnowledgeBaseEntry>();
		
		/**
		 * Returns <code>true</code> if either (id1, id2) or (id2, id1) are present in the knowledge base. 
		 */
		@Override
		public boolean interacts(String id1, String id2) {
			return kb.contains(new UndirectedPair<String>(id1, id2));
		}

		/**
		 * Populate knowledge base.
		 * @param id1
		 * @param id2
		 */
		public void add(String id1, String id2) {
			kb.add(new UndirectedKnowledgeBaseEntry(id1, id2));
		}

		@Override
		public Iterator<UndirectedKnowledgeBaseEntry> iterator() {
			return kb.iterator();
		}
				
		/** 
		 * Populate from a tuple reader.
		 * @param csv
		 * @return
		 * @throws IOException
		 */
		public static UndirectedKnowledgeBase from(CSVDictReader csv) throws IOException
		{
			UndirectedKnowledgeBase ret = new UndirectedKnowledgeBase();			
			DictRow row;
			while ((row = csv.readNext()) != null)
			{
				String id1 = row.get("id1"); // TODO externalize
				String id2 = row.get("id2"); // TODO externalize
				if (!isEmpty(id1) && !isEmpty(id2))
					ret.add(id1.trim(),id2.trim());
				else if (!isEmpty(id1) || !isEmpty(id2))
					System.err.println("WARNING: skipping incomplete pair 1:'"+id1+"', 2:'"+id2+"' in row " + row.toString());
				else
					System.err.println("WARNING: skipping empty pair 1:'"+id1+"', 2:'"+id2+"' in row " + row.toString());
			}
			return ret;
		}

		@Override
		public int size() {
			return kb.size();
		}
	}


}
