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
bbw.virtusos = sys.argv[4]

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

for table_file in os.listdir(tables_dir):
    file = tables_dir + table_file
    df = pd.read_csv(file, header = None, dtype = str)
    filecsv = bbw.preprocessing(df)
    table_candidates = list()
    i = 0

    for index, row in df.iterrows():
         j = 0
         row_candidates = list()

         for column in list(df.columns.values):
             cell = row[column]

             if isinstance(cell, str):
                 candidates = bbw.lookup(cell, '')

                 if not candidates[0] is None:
                     row_candidates.append([i, j, set(candidates[0]['item'])])

             j += 1

         i += 1

         if len(row_candidates) > 0:
             table_candidates.append(row_candidates)

    with open(output_dir + '/' + table_file, 'w') as handle:
        writer = csv.writer(handle)

        for row in table_candidates:
            for column in row:
                candidates_str = ''

                for entity in column[2]:
                    candidates_str += entity + ' '

                writer.writerow([column[0], column[1], candidates_str])
