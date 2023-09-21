# Command: 'python3 analysis.py (load|new)'
# 'load': Show the stats already computed once
# 'new': Re-compute the stats

import os
import sys
import json
import csv
import pickle
from stats import Stats

# TODO: Needs to be re-written, as we now use HardTables from SemTab 2022
def analyze_semtab():
    dir = '/home/setup/semtab/HardTablesR2/DataSets/HardTablesR2/Test/tables/'
    files = os.listdir(dir)
    stats = Stats()
    rows = 0
    columns = 0

    for file in files:
        with open(dir + file, 'r') as fd:
            handle = csv.reader(fd)
            tmp_columns = 0

            for line in handle:
                rows += 1
                tmp_columns = len(line)

            columns += tmp_columns

    stats.set_rows(rows / len(files))
    stats.set_columns(columns / len(files))

    return stats

# Returns SemTab stats
def load_stats():
    with open('.SemTab.stats', 'rb') as file:
        semtab = pickle.load(file)
        return semtab

def write_stats(filename, stats):
    with open(filename, 'wb') as file:
        pickle.dump(stats, file, pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Missing argument \'load\' or \'new\'')
        exit(1)

    stats_semtab = None

    if sys.argv[1] == 'load':
        stats_semtab = load_stats()

        if all_stats is None:
            print('No stats have been loaded. You need to use the \'new\' command.')
            exit(1)

    print('\nAnalyzing SemTab...')

    if sys.argv[1] == 'new':
        stats_semtab = analyze_semtab()
        write_stats('.SemTab.stats', stats_semtab)

    print('SemTab stats:')
    stats_semtab.print()
