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
import neo4j_connector as neo4j

def analyze_wikitables(version, kg):
    stats = Stats()
    rows = 0
    columns = 0
    entities = 0
    entity_set = set()
    dir = '/home/benchmarks/' + kg + '/wikitables_' + str(version) + '/'
    table_files = os.listdir(dir)
    type_pred = neo4j.type_predicate()

    for table_file in table_files:
        with open(dir + table_file, 'r') as file:
            table = json.load(file)['table']
            rows += len(table)

            if len(table) > 0:
                columns += len(table[0])

        for row in table:
            for column in row:
                if len(column['entity']) > 0:
                    entities += 1
                    entity_set.add(column['entity'])

    stats.set_tables(len(table_files))
    stats.set_rows(rows / len(table_files))
    stats.set_columns(columns / len(table_files))
    stats.set_num_entities(entities / len(table_files))

    type_distribution = dict()

    for entity in entity_set:
        types = neo4j.entity_types(entity, type_pred)

        for type in types:
            type = type.split('/')[-1].split('#')[-1]

            if type not in type_distribution.keys():
                type_distribution[type] = 0

            type_distribution[type] += 1

    plot(type_distribution, 25, 12, 11, '/plots/Wikitables-DBpedia_' + str(version) + '.pdf')
    return stats

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Missing argument \'load\' or \'new\'')
        exit(1)

    stats_wikitables_dbpedia_2013 = None
    stats_wikitables_dbpedia_2019 = None

    if sys.argv[1] == 'load':
        stats_wikitables_dbpedia_2013 = ss.load_stats('/plots/.Wikitables2013_DBpedia.stats')
        stats_wikitables_dbpedia_2019 = ss.load_stats('/plots/.Wikitables2019_DBpedia.stats')

        if stats_wikitables_dbpedia_2013 is None or stats_wikitables_dbpedia_2019 is None:
            print('Stats could not be loaded. You need to use the \'new\' command.')
            exit(1)

    print('\nAnalyzing Wikitables...')

    if sys.argv[1] == 'new':
        stats_wikitables_dbpedia_2013 = analyze_wikitables(2013, 'dbpedia')
        stats_wikitables_dbpedia_2019 = analyze_wikitables(2019, 'dbpedia')
        ss.write_stats('/plots/.Wikitables2013_DBpedia.stats', stats_wikitables_dbpedia_2013)
        ss.write_stats('/plots/.Wikitables2019_DBpedia.stats', stats_wikitables_dbpedia_2019)

    print('Wikitables 2013 stats (DBpedia):')
    stats_wikitables_dbpedia_2013.print()
    print('\nWikitables 2019 stats (DBpedia):')
    stats_wikitables_dbpedia_2019.print()
