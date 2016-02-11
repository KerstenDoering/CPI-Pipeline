/*
 * This is free software.
 * 
 * Creating and using a model relies on the
 * "jsre-config.xml" configuration file.
 * This class tries to solve the problem of
 * manually editing the configuration file.
 * 
 * Roughly, it works as follows:
 * 1) Initializing with original "jsre-config.xml"
 * 2) Adjust the parameters with class-methods
 *    (useModelFile, setParams, ...)
 * 3) Set the config file with 'setConfigFile'
 * [4) Save the config file using 'saveConfigFile']
 * 
 * This is a quick and dirty solution. The
 * class reads the whole configuration file into
 * a string and then uses regular expressions to replace
 * values. A more robust (more complicated)
 * solution would include the use of 'DOM' or
 * similar packages.
 * 
 * TODO: better exception handling
 * TODO: catch possible stack-overflow when reading config file
 * TODO: increase robustness of the regular expressions (spaces 'n shit)
 */

import java.io.*;
import java.util.Properties;
import java.util.regex.*;

import org.itc.irst.tcc.sre.util.UnZipModel;

public class Configurator {

//Name of the configuration-file (e.g. 'jsre-config.xml')
private String templateConfigFilename;	
private Properties modelParam; // Parameters of the model

private File configFile; // The new configuration-file
private String configString; // String containing the data of the configuration-file

public Configurator(String configFile) {
	this.templateConfigFilename = configFile;
	modelParam = new Properties();
	readConfigFile();
}

public void setConfigFile() {
	setAll();
	createTempFile();
	setSystemProperty();
}

/*
 * Read the parameters from the model
 * file.
 */
public void useModelFile(String modelFilename) {
	File mf = new File(modelFilename);
	UnZipModel model;
	try {
		model = new UnZipModel(mf);
		File paramFile = model.get("param");
		modelParam.load(new FileInputStream(paramFile));
	} catch (Exception e) {
		e.printStackTrace();
	}
}

/*
 * Convenience function
 */
private void setSystemProperty() {
	setSystemProperty("config.file");
}

/*
 * Set a system property. This is used by the
 * package to locate the configuration file.
 */
private void setSystemProperty(String property) {
	//"config.file"
	System.out.println("[Configurator] Setting configuration file: " + getTempFilename());	
	System.setProperty(property, configFile.getPath());
}

/*
 * Create a temporary file that holds
 * the modified configuration.
 */
private void createTempFile() {
	try {
		// Name the file "config<foobar>.tmp"
		configFile = File.createTempFile("config",".tmp");
		configFile.deleteOnExit();
		saveConfigFile(configFile);
	} catch (Exception e) {
		e.printStackTrace();
	}
}

/*
 * Load the whole config-file into a String (configString).
 * TODO: Catch possible stack-overflow caused by long files.
 */
private void readConfigFile() {
	try {
		StringBuffer fileData = new StringBuffer();
		BufferedReader reader = new BufferedReader(new FileReader(templateConfigFilename));
		char[] buf = new char[1024];
		int numRead=0;
		while((numRead=reader.read(buf)) != -1){
			String readData = String.valueOf(buf, 0, numRead);
			fileData.append(readData);
		}
		reader.close();
		configString = fileData.toString();
	} catch (IOException e) {
		e.printStackTrace();
	}
}

/*
 * If you want to keep the config file ...
 */
public void saveConfigFile(String filename) {
	File file = new File(filename);
	saveConfigFile(file);
}

/*
 * TODO: rename either of the saveConfigFile fcts.
 */
private void saveConfigFile(File file) {
	try {
		PrintWriter out = new PrintWriter(file);
		out.println(configString);
		out.close();
	} catch (Exception e) {
		e.printStackTrace();
	}
}

/*
 * Use regular expressions to replace
 * values in the config.
 */
private void setAll() {
	// set n-gram and window-size in all elements
	Pattern p_nGram = Pattern.compile("(<param-name>n-gram</param-name>\\s*<param-value>)(\\d+)(</param-value>)");
	Matcher m = p_nGram.matcher(configString);
	StringBuffer result = new StringBuffer();
	while (m.find()) {
		m.appendReplacement(result, m.group(1) + modelParam.getProperty("n-gram") + m.group(3));
	}
	m.appendTail(result);
	//System.out.println(result);
	configString = result.toString();
	
	
	// Do the same again for 'window-size'
	// TODO: wrap this up in a function
	Pattern p_wSize = Pattern.compile("(<param-name>window-size</param-name>\\s*<param-value>)(\\d+)(</param-value>)");
	m = p_wSize.matcher(configString);
	result = new StringBuffer();
	while (m.find()) {
		m.appendReplacement(result, m.group(1) + modelParam.getProperty("window-size") + m.group(3));
	}
	m.appendTail(result);
	//System.out.println(result);
	configString = result.toString();
}

public void setNGramAndWindowSize(String nGram, String windowSize) {
	modelParam.setProperty("n-gram", nGram);
	modelParam.setProperty("window-size", windowSize);
}

public void setParams(Properties p) {
	modelParam = p;
}

public String getTempFilename() {
	return configFile.getPath();
}

}
