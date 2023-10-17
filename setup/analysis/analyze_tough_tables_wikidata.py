# Command: 'python3 analysis.py (load|new)'
# 'load': Show the stats already computed once
# 'new': Re-compute the stats

import os
import sys
import json
import csv
from stats import Stats
import save_stats as ss
from plot import plot
import neo4j_connector.py as neo4j

def analyze_tough_tables():
    dir = '/home/setup/tough_tables/ToughTablesR2-WD/Test/tables/'
    gt_file = '/home/setup/tough_tables/ToughTablesR2-WD/Test/gt/cea_gt.csv'
    files = os.listdir(dir)
    rows = 0
    columns = 0
    entities = 0
    entity_density = 0
    entity_set = set()
    entity_map = dict()
    stats = Stats()
    type_pred = neo4j.type_predicate()

    with open(gt_file, 'r') as fd:
        handle = csv.reader(fd)

        for line in handle:
            table = line[0]
            ents = line[3]

            for entity in ents.split(' '):
                entity_set.add(entity)

            if table not in entity_map.keys():
                entity_map[table] = 1

            else:
                entity_map[table] += 1

    for table in entity_map.keys():
        entities += entity_map[table]

    for file in files:
        with open(dir + file, 'r') as fd:
            handle = csv.reader(fd)
            table_id = file.replace('.csv', '')
            table_cells = 0
            tmp_columns = 0

            for line in handle:
                rows += 1
                tmp_columns = len(line)
                table_cells += len(line)

            columns += tmp_columns

            if table_id in entity_map[table_id]:
                entity_density += float(entity_map[table_id]) / table_cells

    stats.set_tables(len(files))
    stats.set_rows(rows / len(files))
    stats.set_columns(columns / len(files))
    stats.set_entity_density(entity_density / len(files))

    type_distribution = dict()
    stats.set_num_entities(entities / len(entity_map.keys()))

    for entity in entity_set:
        types = neo4j.entity_types(entity, type_pred)

        for type in types:
            type = type.split('/')[-1].split('#')[-1]

            if type not in type_distribution.keys():
                type_distribution[type] = 0

            type_distribution[type] += 1

    plot(type_distribution, 25, 12, 11, '/plots/ToughTables-Wikidata.pdf')
    return stats

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Missing argument \'load\' or \'new\'')
        exit(1)

    stats_tough_tables_dbpedia = None

    if sys.argv[1] == 'load':
        stats_tough_tables_dbpedia = ss.load_stats('/plots/.ToughTables_Wikidata.stats')

        if stats_tough_tables_dbpedia is None:
            print('Stats could not be loaded. You need to use the \'new\' command.')
            exit(1)

    print('\nAnalyzing ToughTables... (Wikidata)')

    if sys.argv[1] == 'new':
        stats_tough_tables_dbpedia = analyze_tough_tables()
        ss.write_stats('/plots/.ToughTables_Wikidata.stats', stats_tough_tables_dbpedia)

    stats_tough_tables_dbpedia.print()
