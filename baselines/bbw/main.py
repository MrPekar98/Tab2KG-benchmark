import bbw
import sys
import csv
import time
import pandas as pd
import os

runtimes = list()
tables_dir = sys.argv[1]
output_dir = sys.argv[2]
bbw.endpoint = sys.argv[3]
bbw.virtuoso = sys.argv[4]

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

for table_file in os.listdir(tables_dir):
    file = tables_dir + table_file
    start = time.time() * 1000
    df = pd.read_csv(file, header = None, dtype = str)
    [web_table, url_table, label_table, cpa, cea, cta] = bbw.annotate(df)
    end = time.time() * 1000 - start
    runtimes.append([file.replace('.csv', ''), end])
    cea.to_csv(output_dir + table_file)

with open(output_dir + 'runtimes.csv', 'w') as handle:
    writer = csv.writer(handle)
    writer.writerow(['table', 'miliseconds'])

    for time in runtimes:
        writer.writerow(time)
