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
package org.itc.irst.tcc.sre.util;

import org.apache.log4j.Logger;
import org.apache.log4j.PropertyConfigurator;
import org.apache.commons.digester.*;
import java.io.*;
import java.util.*;


/**
 * Factory class for vending standard <code>Stemmer</code>
 * objects. Wherever  possible, this factory will hand out
 * references to shared <code>Stemmer</code> instances.
 *
 * @author		Claudio Giuliano
 * @version 	1.0
 * @since			1.0
 */
public class StemmerFactory
{	
	/**
	 * Define a static logger variable so that it references the
	 * Logger instance named <code>StemmerFactory</code>.
	 */
	static Logger logger = Logger.getLogger(StemmerFactory.class.getName()); 

	/**
	 * A prototype for a stemmer factory such that only
	 * one instance class can ever exist.
	 */
	private static StemmerFactory stemmerFactory;

	//
	private Properties initParams;
		
	/**
	 * Constructs a <code>StemmerFactory</code> object.
	 *
	 */
	private StemmerFactory()
	{
		initParams = new Properties();		
		
		try
		{
			Digester digester = new Digester();
			digester.push(this);
			
			digester.addCallMethod("jsre-config/stemmer-list/stemmer", "addStemmer", 2);
			digester.addCallParam("jsre-config/stemmer-list/stemmer/stemmer-name", 0);
			digester.addCallParam("jsre-config/stemmer-list/stemmer/stemmer-class", 1);

			String configFile = System.getProperty("config.file");
			if (configFile == null)
			{
				logger.debug("StemmerFactory uses the default config file: jsre-config.xml");
				digester.parse("jsre-config.xml");
			}
			else
			{
				logger.debug("StemmerFactory uses the config file: " + configFile);
				digester.parse(configFile);
			}
		}
		catch (Exception e)
		{
			logger.error(e);
		}
		
	} // end constructor

	//
	public void addStemmer(String stemmerName, String stemmerClass)
	{
		logger.debug("Add stemmer: " + stemmerName + ", " + stemmerClass);
		initParams.setProperty(stemmerName.toUpperCase(), stemmerClass);
	} // end addStemmer
	
	/**
	 * Returns the <i>id</i> of the specified stemmer and adds
	 * the stemmer to the lexicon if it is not present yet.
	 * <p>
	 * If the
	 * lexicon is read only, stemmers not already present in the
	 * lexicon will not be added and a <code>null</code> <i>id</i>
	 * will be returned.
	 *
	 * @param name	the string representation of the stemmer.
	 * @return 			the <i>id</i> of the specified stemmer.
	 */
	public Stemmer getInstance(String name) throws StemmerNotFoundException
	{
		//logger.debug("stemmerFactory.getInstance: " + name);
		String stemmerClass = initParams.getProperty(name.toUpperCase());
		Stemmer stemmer = null;
		try
		{
			stemmer = (Stemmer) (Class.forName(stemmerClass)).newInstance();
			//stemmer.set(initParams);
		}
		catch (Exception e)
		{
			throw new StemmerNotFoundException(name + " stemmer not found.");
		}

		return stemmer;
	} // end getInstance


	/**
	 * Returns a <code>String</code> object representing this
	 * <code>StemmerFactory</code>.
	 *
	 * @return a string representation of this object.
	 */
	public String toString()
	{
		return "StemmerFactory";
	} // end toString
	
	/**
	 * Returns <code>StemmerFactory</code> object; only
	 * one <code>StemmerFactory</code> instance can
	 * exist.
	 *
	 * @return	<code>StemmerFactory</code> object
	 */
	public static synchronized StemmerFactory getStemmerFactory()
	{
		//logger.debug("StemmerFactory.getStemmerFactory");
		if (stemmerFactory == null)
		{
			stemmerFactory = new StemmerFactory();
		}
		
		return stemmerFactory;
	} // end getStemmerFactory

	//
	public static void main(String args[]) throws Exception
	{
		String logConfig = System.getProperty("log-config");
		if (logConfig == null)
			logConfig = "log-config.txt";

		PropertyConfigurator.configure(logConfig);

		if (args.length < 2)
		{
			System.err.println("java -mx512M org.itc.irst.tcc.sre.util.StemmerFactory stemmer word+");
			System.exit(0);
		}

		StemmerFactory stemmerFactory = StemmerFactory.getStemmerFactory();
		Stemmer stemmer = stemmerFactory.getInstance(args[0]);
		
		for (int i=1;i<args.length;i++)
			System.out.println(args[i] + " ==> " + stemmer.stem(args[i]));
			
	} // end main
	
} // end class StemmerFactory