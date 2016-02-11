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

import org.apache.log4j.Logger;
import org.apache.log4j.PropertyConfigurator;
import java.io.*;

/**
 * TO DO
 *
 * @author 	Claudio Giuliano
 * @version %I%, %G%
 * @since		1.0
 */
public class InputFormatConverter
{	
	/**
	 * Define a static logger variable so that it references the
	 * Logger instance named <code>InputFormatConverter</code>.
	 */
	static Logger logger = Logger.getLogger(InputFormatConverter.class.getName()); 
		
	/**
	 * Creates a <code>InputFormatConverter</code> object.
	 */ 
	public InputFormatConverter(File in)
	{
		logger.debug("InputFormatConverter.InputFormatConverter: " + in);
				
		try
		{
						
			LineNumberReader lnr = new LineNumberReader(new FileReader(in));
	
			String s;
			while ((s = lnr.readLine()) != null)
			{
				String[] fld = s.split("\t");
				
			} // end while
				
			lnr.close();
		}
		catch (IOException e)
		{
			logger.error(e);
		}
	} // end constructor

	//
	public static void main(String args[]) throws Exception
	{
		String logConfig = System.getProperty("log-config");
		if (logConfig == null)
			logConfig = "log-config.txt";
			
		PropertyConfigurator.configure(logConfig); 	

		if (args.length != 1)
		{
			System.err.println("java -mx512M org.itc.irst.tcc.sre.data.SenteceShuffler in");
			System.exit(-1);
		}

	
	} // end main


} // end class InputFormatConverter