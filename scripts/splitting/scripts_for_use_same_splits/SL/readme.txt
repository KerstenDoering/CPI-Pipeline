This step must be do to use the same splits and want to CV for CPI-DS_IV and CPI-DS_IV datasets not for CPI-DS.
1- make clean-SL
2- copy splits as descrip in github (don't forget to name the splits DS1.txt DS2.txt ....)
3- modify both the modified scripts in this directory as follow:
   - modify both scripts where you can find something like <830, like this : for CPI-DS_IV >=830, and for CPI-DS_NIV <830.
   - modify the line realnameDS='CPI-DS_NIV'  in Run_SL_Kernel.py accordinding to the name of the current dataset. 
4- copy the two modified scripts (Fscore.py--> scripts/ppi-benchmark/Experiments/SL/measures/ and Run_SL_Kernel.py --> scripts/) and replace the orginal one.
5- then run make experiment Kernel=SL expTyp=CV InputFile=CPI-DS.xml Processors=4  (note the inputFile for all runs is same, this command is same to get the results of all datasets (CPI-DS, CPI-DS_IV and CPI-DS_NIV))

