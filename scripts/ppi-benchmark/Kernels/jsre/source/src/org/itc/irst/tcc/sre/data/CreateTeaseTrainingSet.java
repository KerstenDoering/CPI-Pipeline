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
package org.itc.irst.tcc.sre.data;

import java.util.*;
import java.io.*;

import org.apache.log4j.Logger;
import org.apache.log4j.PropertyConfigurator;

import org.itc.irst.tcc.sre.kernel.expl.AbstractMapping;
import org.itc.irst.tcc.sre.kernel.expl.ContextMappingFactory;
import org.itc.irst.tcc.sre.kernel.KernelNotFoundException;
import org.itc.irst.tcc.sre.util.svm_train;
import org.itc.irst.tcc.sre.util.UnZipModel;
import org.itc.irst.tcc.sre.util.FeatureIndex;
import org.itc.irst.tcc.sre.util.svm_predict;
import org.itc.irst.tcc.sre.util.Evaluator;
import org.itc.irst.tcc.sre.data.*;

/**
 * TO DO
 *
 * @author 	Claudio Giuliano
 * @version %I%, %G%
 * @since		1.0
 */
public class CreateTeaseTrainingSet
{
	/**
	 * Define a static logger variable so that it references the
	 * Logger instance named <code>CreateTeaseTrainingSet</code>.
	 */
	static Logger logger = Logger.getLogger(CreateTeaseTrainingSet.class.getName()); 

	//
	private File inputFile;
	
	//
	private File outputFile;
	
	//
	public CreateTeaseTrainingSet(File inputFile, File outputFile) throws IOException
	{
		this.inputFile = inputFile;
		this.outputFile = outputFile;
		run();
	} // end constructor
	
	// read the data set
	private void run() throws IOException
	{
		PrintWriter pw = new PrintWriter(new FileWriter(outputFile));
		LineNumberReader lr = new LineNumberReader(new FileReader(inputFile)); 
		String line = null;
		int j  = 0;	
		//String t = null;
		while ((line = lr.readLine()) != null)
		{
			logger.info(j + " " + line);
			pw.print("1");
			pw.print("\t");
			pw.print(++j);
			pw.print(".tease\t");
			String[] s = line.split(" ");
			for (int i=0;i<s.length - 1;i++)
			{
			
				String[] t = s[i].split("/");
				if (i != 0)
					pw.print(" ");
		
				pw.print(i);
				pw.print("&&");
				pw.print(t[0]); // form
				pw.print("&&");
				pw.print(t[1]); // lemma
				pw.print("&&");
				pw.print(t[2]); // pos
				pw.print("&&");
				pw.print(t[3]); // NE  | O
				pw.print("&&");
				pw.print(t[4]); // target | O
				
			}
			pw.print("\n");
		} // end while
		lr.close();
		pw.flush();
		pw.close();
	}	// end run


	//
	public static void main(String args[]) throws Exception
	{
		String logConfig = System.getProperty("log-config");
		if (logConfig == null)
			logConfig = "log-config.txt";
			
		PropertyConfigurator.configure(logConfig);
		
		int parm = 2;
		
		if (args.length != parm)
		{
			System.out.println("java org.itc.irst.tcc.sre.CreateTeaseTrainingSet in out");
			System.exit(-1);
		}

		File inputFile = new File(args[0]);
		File outputFile = new File(args[1]);
		
		CreateTeaseTrainingSet mapper = new CreateTeaseTrainingSet(inputFile, outputFile);
	
	} // end main


} // end class CreateTeaseTrainingSet