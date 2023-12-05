from bbw import bbw
import sys
import os
import pandas as pd
import time
import csv

OUTPUT_DIR = '/results/bbw/'

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Missing table directory and/or name of output directory')
        exit(1)

    dir = sys.argv[1]
    output = OUTPUT_DIR + sys.argv[2]
    times = dict()

    if not dir.endswith('/'):
        dir += '/'

    if not output.endswith('/'):
        output += '/'

    tables = os.listdir(dir)
    print('Linking tables in ' + dir)

    if not os.path.exists(output):
        os.mkdir(output)

    for table in tables:
        try:
            start = time.time() * 1000
            df = pd.read_csv(dir + table, dtype = str)
            [cpa_list, cea_list, nomatch] = bbw.contextual_matching(bbw.preprocessing(df))
            [cpa, cea, cta] = bbw.postprocessing(cpa_list, cea_list)
            duration = time.time() * 1000 - start

            cea.to_csv(output + table, sep = ',', index = False)
            times[table] = duration

        except Exception as e:
            print(str(e))

    with open(output + 'runtimes.csv', 'w') as file:
        writer = csv.writer(file, delimiter = ',')
        writer.writerow(['table', 'miliseconds'])

        for table in times.keys():
            writer.writerow([table, times[table]])
