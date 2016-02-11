/*
 * Copyright 2005 FBK-irst (http://www.fbk.eu)
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.itc.irst.tcc.sre.kernel.expl;

import org.apache.log4j.Logger;
import org.apache.log4j.PropertyConfigurator;
import java.io.*;
import java.util.*;
import java.text.*;
import org.itc.irst.tcc.sre.data.ExampleSet;
import org.itc.irst.tcc.sre.data.Sentence;
import org.itc.irst.tcc.sre.data.SentenceSetCopy;
import org.itc.irst.tcc.sre.data.VectorSet;
import org.itc.irst.tcc.sre.util.Vector;
import org.itc.irst.tcc.sre.util.SparseVector;
import org.itc.irst.tcc.sre.util.FeatureIndex;


/**
 * TO DO
 *
 * @author 	Claudio Giuliano
 * @version %I%, %G%
 * @since		1.0
 */
public class ComboMapping extends AbstractMapping
{
	/**
	 * Define a static logger variable so that it references the
	 * Logger instance named <code>ComboMapping</code>.
	 */
	static Logger logger = Logger.getLogger(ComboMapping.class.getName()); 
	
	//
	protected AbstractMapping[] mappingArray;
	
	//
	protected ContextMappingFactory mappingFactory;
	
	//
	protected int[] mappingSize;
	
	//
	private int subspaceCount;
	
	//
	public ComboMapping()
	{
		logger.debug("ComboMapping.ComboMapping");
		mappingFactory = ContextMappingFactory.getContextMappingFactory();
		subspaceCount = 0;
	} // end constructor
	
	//
	public void setParameters(Properties parameters)
	{
		logger.debug("ComboMapping.setParameters");
		List argList = new ArrayList();
		Iterator it = parameters.keySet().iterator();
		while (it.hasNext())
		{
			String arg = (String) it.next();
			if (arg.startsWith("arg"))
				argList.add(parameters.getProperty(arg));
		} // end while
		
		if (argList.size() > 0)
			init(argList);
	} // end setParameters

	//
	private void init(List argList)
	{
		logger.debug("ComboMapping.init");
		
		//
		mappingArray = new AbstractMapping[argList.size()];
		
		logger.debug("ComboMapping.number of basic kernels: " + argList.size());
		
		for (int i=0;i<argList.size();i++)
		{
			String argName = (String) argList.get(i);
			try
			{
				mappingArray[i] = mappingFactory.getInstance(argName);
				// how to set up basic kernel parameters?
				// the kernel parameters are set by the factory
				// and are taken from the basic kernel mapping
				logger.debug(argName + ":" + mappingArray[i]);
			}
			catch (MappingNotFoundException ex)
			{
				logger.error(ex);
			}
			
		} // end for i
		
		logger.debug("\n***");
		mappingSize = new int[mappingArray.length];
		for (int j=0;j<mappingArray.length;j++)
		{
			mappingSize[j] = mappingArray[j].subspaceCount();
			subspaceCount += mappingSize[j];
			
			logger.debug(j + ":" + mappingArray[j] + ":" + mappingSize[j]);
		}
		
		logger.debug("subspaceCount: " + subspaceCount);
		logger.debug("***");

	} // end setParameters
	
	//
	public int subspaceCount()
	{		
		return subspaceCount;
	} // end subspaceCount
	
	
	//
	public Vector[] map(Object x, Object id, FeatureIndex[] index) throws IllegalArgumentException
	{
		//logger.debug("ComboMapping.map");

		FeatureIndex[][] mappingIndex = new FeatureIndex[mappingArray.length][];
		for (int i=0;i<mappingArray.length;i++)
		{
			mappingIndex[i] = new FeatureIndex[mappingSize[i]];
		}	
		
		// copy the whole feature index into the
		// single feature indexes
		int srcPos = 0;
		for (int i=0;i<mappingArray.length;i++)
		{
			if (i != 0)
				srcPos += mappingSize[i - 1];
				
			System.arraycopy(index, srcPos, mappingIndex[i], 0, mappingSize[i]);
		}	// end for i

		Vector[] subspaces = new SparseVector[subspaceCount()];
		
		// copy the single mapping spaces into the
		// whole mapping space 
		Vector[][] mappingSpace = new Vector[mappingArray.length][];
		for (int i=0;i<mappingArray.length;i++)
		{
			mappingSpace[i] = mappingArray[i].map(x, id, mappingIndex[i]);
		}	// end for i
		
		srcPos = 0;
		for (int i=0;i<mappingArray.length;i++)
		{
			if (i != 0)
				srcPos += mappingSize[i - 1];
				
			System.arraycopy(mappingSpace[i], 0, subspaces, srcPos, mappingSize[i]);
		}	// end for i
		
		//
		return subspaces;
	} // end map
	
} // end class ComboMapping
