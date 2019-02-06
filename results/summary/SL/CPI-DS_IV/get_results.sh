python generate_selects_psql.py
./get_csv_results.sh
cd output/
python average.py
cat CPI-DS_IV*average.csv > CPI-DS_IV_average.csv
python header.py
