# Command: 'python3 analysis.py (load|new)'
# 'load': Show the stats already computed once
# 'new': Re-compute the stats

import os
import sys
import json
import csv
import pickle
from stats import Stats

def analyze_tough_tables(kg):
    kg_dir = ''

    if kg == 'dbpedia':
        kg_dir = 'ToughTablesR2-DBP/'

    else:
        kg_dir = 'ToughTablesR2-WD/'

    dir = '/home/setup/tough_tables/' + kg_dir + 'Test/tables/'
    files = os.listdir(dir)
    rows = 0
    columns = 0
    entities = 0
    entity_map = dict()
    stats = Stats()

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

    gt_file = '/home/setup/tough_tables/' + kg_dir + 'Test/gt/cea_gt.csv'

    with open(gt_file, 'r') as fd:
        handle = csv.reader(fd)

        for line in handle:
            table = line[0]

            if table not in entity_map.keys():
                entity_map[table] = 1

            else:
                entity_map[table] += 1

    for table in entity_map.keys():
        entities += entity_map[table]

    stats.set_num_entities(entities / len(entity_map.keys()))
    return stats

# Returns array of Stats instances, one for each benchmark
# 1: ToughTables - DBpedia
# 2: ToughTables - Wikidata
def load_stats():
    stats = list()

    with open('.ToughTables_DBpedia.stats', 'rb') as file:
        tt = pickle.load(file)
        stats.append(tt)

    with open('.ToughTables_Wikidata.stats', 'rb') as file:
        tt = pickle.load(file)
        stats.append(tt)

    return stats

def write_stats(filename, stats):
    with open(filename, 'wb') as file:
        pickle.dump(stats, file, pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Missing argument \'load\' or \'new\'')
        exit(1)

    all_stats = None
    stats_tough_tables_dbpedia = None
    stats_tough_tables_wikidata = None

    if sys.argv[1] == 'load':
        all_stats = load_stats()

        if all_stats is None:
            print('No stats have been loaded. You need to use the \'new\' command.')
            exit(1)

        stats_tough_tables_dbpedia = all_stats[0]
        stats_tough_tables_wikidata = all_stats[1]

    print('\nAnalyzing ToughTables...')

    if sys.argv[1] == 'new':
        stats_tough_tables_dbpedia = analyze_tough_tables('dbpedia')
        stats_tough_tables_wikidata = analyze_tough_tables('wikidata')
        write_stats('.ToughTables_DBpedia.stats', stats_tough_tables_dbpedia)
        write_stats('.ToughTables_Wikidata.stats', stats_tough_tables_wikidata)

    print('Tough Tables DBpedia stats:')
    stats_tough_tables_dbpedia.print()
    print('\nTough Tables Wikidata stats:')
    stats_tough_tables_wikidata.print()
