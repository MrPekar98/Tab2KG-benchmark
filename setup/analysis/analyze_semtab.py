# Command: 'python3 analysis.py (load|new)'
# 'load': Show the stats already computed once
# 'new': Re-compute the stats

import os
import sys
import json
import csv
import statistics
from stats import Stats
import save_stats as ss
from plot import plot
import neo4j_connector.py as neo4j

def analyze_semtab():
    base = '/home/setup/semtab/HardTablesR2/DataSets/HardTablesR2/Test/'
    table_dir = base + 'tables/'
    gt_file = base + 'gt/cea_gt.csv'
    files = os.listdir(table_dir)
    stats = Stats()
    rows = 0
    columns = 0
    entities = set()
    type_pred = neo4j.type_predicate()

    with open(gt_file, 'r') as fd:
        handle = csv.reader(fd)
        table_entities = dict()

        for line in handle:
            table_id = line[0]
            entity = line[3]
            entities.add(entity)

            if table_id not in table_entities.keys():
                table_entities[table_id] = 0

            table_entities[table_id] += 1

        stats.set_num_entities(statistics.mean(table_entities.values()))

    for file in files:
        with open(table_dir + file, 'r') as fd:
            handle = csv.reader(fd)
            tmp_columns = 0

            for line in handle:
                rows += 1
                tmp_columns = len(line)

            rows -= 1
            columns += tmp_columns

    stats.set_tables(len(files))
    stats.set_rows(rows / len(files))
    stats.set_columns(columns / len(files))

    type_distribution = dict()

    for entity in entities:
        types = neo4j.entity_types(entity, type_pred)

        for type in types:
            type = type.split('/')[-1]

            if type not in type_distribution.keys():
                type_distribution[type] = 0

            type_distribution[type] += 1

    plot(type_distribution, 25, 12, 11, '/plots/SemTab.pdf')
    return stats

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Missing argument \'load\' or \'new\'')
        exit(1)

    stats_semtab = None

    if sys.argv[1] == 'load':
        stats_semtab = ss.load_stats('/plots/.SemTab.stats')

        if stats_semtab is None:
            print('Stats could not be loaded. You need to use the \'new\' command.')
            exit(1)

    print('\nAnalyzing SemTab...')

    if sys.argv[1] == 'new':
        stats_semtab = analyze_semtab()
        ss.write_stats('/plots/.SemTab.stats', stats_semtab)

    print('SemTab stats:')
    stats_semtab.print()