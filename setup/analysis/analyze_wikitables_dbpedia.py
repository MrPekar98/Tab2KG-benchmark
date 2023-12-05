# Command: 'python3 analysis.py (load|new)'
# 'load': Show the stats already computed once
# 'new': Re-compute the stats

import os
import sys
import csv
import statistics
from analysis.stats import Stats
from analysis.plot import plot
import analysis.save_stats as ss
import analysis.neo4j_connector as neo4j

def analyze_wikitables(version, kg):
    stats = Stats()
    rows = 0
    columns = 0
    entities = 0
    entity_density = 0
    entity_set = set()
    analysis_map = dict()
    dir = '/home/benchmarks/wikitables_' + str(version) + '/tables/'
    gt = '/home/benchmarks/wikitables_' + str(version) + '/gt/dbpedia/gt.csv'
    table_files = os.listdir(dir)
    type_pred = neo4j.type_predicate(kg)

    for table_file in table_files:
        table_cells = 0

        with open(dir + table_file, 'r') as file:
            reader = csv.reader(file, delimiter = ',')
            tmp_column_size = 0
            table_id = table_file.replace('.csv', '')
            analysis_map[table_id] = dict()
            analysis_map[table_id]['cells'] = 0
            analysis_map[table_id]['entities'] = 0

            for line in reader:
                rows += 1
                analysis_map[table_id]['cells'] += len(line)
                tmp_column_size = len(line)

            if tmp_column_size > 0:
                columns += tmp_column_size

    with open(gt, 'r') as file:
        reader = csv.reader(file, delimiter = ',')

        for line in reader:
            entities += 1
            analysis_map[line[0]]['entities'] += 1
            entity_set.add(line[3])

    for table in analysis_map.keys():
        entity_density += float(analysis_map[table]['entities']) / analysis_map[table]['cells']

    stats.set_tables(len(table_files))
    stats.set_rows(rows / len(table_files))
    stats.set_columns(columns / len(table_files))
    stats.set_num_entities(entities / len(table_files))
    stats.set_entity_density(entity_density / len(table_files))

    type_distribution = dict()

    for entity in entity_set:
        types = neo4j.entity_types(entity, type_pred)

        for type in types:
            type = type.split('/')[-1].split('#')[-1]

            if type not in type_distribution.keys():
                type_distribution[type] = 0

            type_distribution[type] += 1

    stats.set_type_distribution(type_distribution)
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
    plot(stats_wikitables_dbpedia_2013.type_distribution(), 10, 14, 30, '/plots/Wikitables-DBpedia_2013.pdf')

    print('\nWikitables 2019 stats (DBpedia):')
    stats_wikitables_dbpedia_2019.print()
    plot(stats_wikitables_dbpedia_2019.type_distribution(), 10, 14, 30, '/plots/Wikitables-DBpedia_2019.pdf')
