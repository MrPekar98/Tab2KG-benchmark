from bbw import bbw
import sys
import os
import pandas as pd

OUTPUT_DIR = '/results/bbw/'

if __name__ == '__main__':
    if len(sys.argv < 2):
        print('Missing table directory')
        exit(1)

    try:
        dir = sys.argv[1]
        os.mkdir(OUTPUT_DIR)

        if not dir.endswith('/'):
            dir += '/'

        tables = os.listdir(dir)

        for table in tables:
            df = pd.read_csv(dir + table)
            [cpa_list, cea_list, nomatch] = bbw.contextual_matching(bbw.preprocessing(df))
            [cpa, cea, cta] = bbw.postprocessing(cpa_list, cea_list)

            cea.to_csv(OUTPUT_DIR + table, sep = ',', index = False)

    except Exception as e:
        print(str(e))
