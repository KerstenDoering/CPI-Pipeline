Follow these steps to reproduce the exact cross-validation results for CPI-DS_IV and CPI-DS_NIV. If you only want to reproduce the main cross-validation results of CPI-DS or your own cross-validation results, you only need step 1 and 2.
1 - make clean-APG
2 - copy splits as described in ReadMe.rst ("scripts/splitting/APG_CPI-DS")
3 - modify both the modified scripts in this directory:
  - edit line 25 and 66 with "<830" in Fscore.py, as well as line 57 and 370 in Run_APG_Kernel.py, and also edit line 29 with "CPI-DS_NIV" in Run_APG_Kernel.py, if you want to process CPI-DS_NIV
  - do these changes with ">=830" and "CPI-DS_IV" for CPI-DS_IV 
4 - copy the two modified scripts (Fscore.py--> scripts/ppi-benchmark/Kernels/airola/source/measures/ and Run_APG_Kernel.py --> scripts/) and replace the orginal one
5 - run "make experiment Kernel=APG expTyp=CV InputFile=CPI-DS.xml" Processors=4 (note that the input file is the same for all runs (CPI-DS, CPI-DS_IV and CPI-DS_NIV) to get the results of all datasets, because we always train on CPI-DS)
