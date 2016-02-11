import java.util.Properties;

import org.apache.log4j.Logger;
import org.apache.log4j.PropertyConfigurator;
import org.itc.irst.tcc.sre.Train;

public class runTrain {

	static Logger logger = Logger.getLogger(Train.class.getName()); 
		
	public static void main(String[] args) throws Exception {

		String logConfig = System.getProperty("log-config");
		if (logConfig == null)
			logConfig = "log-config.txt";
			
		PropertyConfigurator.configure(logConfig);
		
		Properties prop = new Properties();
				
		prop.setProperty("m", "256");
		prop.setProperty("cache-size", "256");
		
		prop.setProperty("k", "SL");
		prop.setProperty("kernel-type", "SL");
		
		prop.setProperty("c", "1"); 	
		prop.setProperty("svm-cost", "1"); 
		
		//set training file
//		prop.setProperty("example-file", "examples/relationship_training.csv");
		prop.setProperty("example-file", args[args.length - 2]);
		
		//set model file
//		prop.setProperty("model-file", "examples/relationship.model");	
		prop.setProperty("model-file", args[args.length - 1]);
		
//		//only check parameter combination window-size and n-gram
		for (int i=0;i<args.length;i++)
		{
			if (args[i].equals("-n") || args[i].equals("--n-gram"))
				prop.setProperty("n-gram", args[i+1]);
			
			else if (args[i].equals("-w") || args[i].equals("--window-size"))
				prop.setProperty("window-size", args[i+1]);
		}
				
		// Use original config as template
		Configurator c = new Configurator("jsre-config.xml");
		// Use properties from 'prop'
		c.setParams(prop);
		// Set the new config file to be used by Train, Predict etc.
		c.setConfigFile();
//		c.saveConfigFile("last_configuration_used.xml"); // optional
		
		Train train = new Train(prop);
		train.run();

		System.out.println("\n### training finished ###\n");

		System.out.println("window-size: " + prop.get("window-size"));
		System.out.println("n-gram: " + prop.get("n-gram"));
		
		System.out.println("model-file: " + prop.getProperty("model-file"));
//		System.out.println("model-file: " + args[args.length - 1]);
		System.out.println("train-file: " + args[args.length - 2]);
		
	}
}
