./get_csv_results.sh
cd output/
python average.py
cat CPI-DS*average.csv > CPI-DS_average.csv
python header.py
