./get_csv_results.sh
cd output/
python average.py
cat CPI-DS_NIV*average.csv > CPI-DS_NIV_average.csv
python header.py
