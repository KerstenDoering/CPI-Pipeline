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

import java.io.*;
import java.text.*;

import org.apache.log4j.Logger;
import org.apache.log4j.PropertyConfigurator;

/**
 * This class given a file of good/bad values in CSV format
 * append the micro avarage figures at the end of the file.
 *
 * @author 	Claudio Giuliano
 * @version %I%, %G%
 * @since		1.0
 */
public class MicroAvarage
{
	/**
	 * Define a static logger variable so that it references the
	 * Logger instance named <code>MicroAvarage</code>.
	 */
	static Logger logger = Logger.getLogger(MicroAvarage.class.getName()); 

	/**
	 *
	 */
	public MicroAvarage(File f)
	{
		DecimalFormat decFormatter = new DecimalFormat("0.000");
		
		try
		{
			LineNumberReader lnr = new LineNumberReader(new FileReader(f));
		
			double tp = 0, fp = 0, fn = 0, total = 0;
			String line;
			
			// skip the first line
			line = lnr.readLine();
				
			while ((line = lnr.readLine()) != null)
			{
				String[] s = line.split("\t");
				tp += Double.parseDouble(s[0]);
				fp += Double.parseDouble(s[1]);
				fn += Double.parseDouble(s[2]);
				total += Double.parseDouble(s[3]);
			} // end while
			lnr.close();
		
			double p = tp / (tp + fp);
			double r = tp / (tp + fn);
			double f1 = (2 * p * r) / (p + r);
			double acc = (total - fp - fn) / total;

			FileWriter fw = new FileWriter(f, true);
			fw.write((int) tp + "\t" + (int) fp + "\t" + (int) fn + "\t" + (int) total + "\t" + decFormatter.format(p) + "\t" + decFormatter.format(r) + "\t"  + decFormatter.format(f1) + "\t" +  decFormatter.format(acc) + "\n");
			//fw.write((int) tp + "\t" + (int) fp + "\t" + (int) fn + "\t" + (int) total + "\t" + decFormatter.format(p) + "\t" + decFormatter.format(r) + "\t"  + decFormatter.format(f1) + "\n");
			fw.flush();
			fw.close();
		}
		catch (Exception e)
		{
			logger.error(e);
		}
	} // end constructor

	//
	public static void main(String[] args)
	{
		String logConfig = System.getProperty("log-config");
		if (logConfig == null)
			logConfig = "log-config.txt";
			
		PropertyConfigurator.configure(logConfig); 	

		if (args.length != 1)
		{
			System.err.println("Wrong number of parameters " + args.length);
			System.err.println("Usage: java org.itc.irst.tcc.kre.util.MicroAvarage");
			System.exit(-1);
		}
		
		new MicroAvarage(new File(args[0]));
	} // end main
	
} // end class MicroAvarage
