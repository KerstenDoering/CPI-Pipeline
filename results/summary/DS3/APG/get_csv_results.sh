psql -c "\copy (select corpus, c, tp, fn, tn, fp, total, auc, precision_, recall, f_measure from ppicv where c = 2 and corpus = 'DS3') TO 'output/DS3_c_2.csv' WITH CSV" -h localhost -d ppi -U ppi
psql -c "\copy (select corpus, c, tp, fn, tn, fp, total, auc, precision_, recall, f_measure from ppicv where c = 1 and corpus = 'DS3') TO 'output/DS3_c_1.csv' WITH CSV" -h localhost -d ppi -U ppi
psql -c "\copy (select corpus, c, tp, fn, tn, fp, total, auc, precision_, recall, f_measure from ppicv where c = 0.5 and corpus = 'DS3') TO 'output/DS3_c_05.csv' WITH CSV" -h localhost -d ppi -U ppi
psql -c "\copy (select corpus, c, tp, fn, tn, fp, total, auc, precision_, recall, f_measure from ppicv where c = 0.25 and corpus = 'DS3') TO 'output/DS3_c_025.csv' WITH CSV" -h localhost -d ppi -U ppi
