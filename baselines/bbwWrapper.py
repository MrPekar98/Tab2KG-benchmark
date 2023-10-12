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

        if not dir.endswith('/'):
            dir += '/'

        tables = os.listdir(dir)

        for table in tables:
            df = pd.read_csv(dir + table)
            [web_table, url_table, label_table, cpa, cea, cta] = bbw.annotate(df)

    except Exception as e:
        print(str(e))
