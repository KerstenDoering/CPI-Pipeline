#    Copyright (c) 2016, Kersten Doering <kersten.doering@gmail.com>

cd generate_XML_files
cat DS1/training_dataset_sorted.csv DS2/training_dataset_sorted.csv > DS3/training_dataset_sorted.csv
cd ..

cd splitting
cat DS1/test-1 DS2/test-1 > DS3/test-1
cat DS1/test-2 DS2/test-2 > DS3/test-2
cat DS1/test-3 DS2/test-3 > DS3/test-3
cat DS1/test-4 DS2/test-4 > DS3/test-4
cat DS1/test-5 DS2/test-5 > DS3/test-5
cat DS1/test-6 DS2/test-6 > DS3/test-6
cat DS1/test-7 DS2/test-7 > DS3/test-7
cat DS1/test-8 DS2/test-8 > DS3/test-8
cat DS1/test-9 DS2/test-9 > DS3/test-9
cat DS1/test-10 DS2/test-10 > DS3/test-10
cd ..
