# Command: 'python3 analysis.py (load|new)'
# 'load': Show the stats already computed once
# 'new': Re-compute the stats

import os
import sys
import json
import csv
import pickle
from stats import Stats

def analyze_wikitables(version, kg):
    stats = Stats()
    rows = 0
    columns = 0
    entities = 0
    entity_set = set()
    dir = '../../benchmarks/' + kg + '/wikitables_' + str(version) + '/'
    table_files = os.listdir(dir)

    for table_file in table_files:
        with open(dir + table_file, 'r') as file:
            table = json.load(file)['table']
            rows += len(table)

            if len(table) > 0:
                columns = len(table[0])

        for row in table_file:
            for column in row:
                if len(column['entity']) > 0:
                    entities += 1
                    entity_set.add(column['entity'])

    stats.set_rows(rows / len(table_files))
    stats.set_columns(columns / len(table_files))
    stats.set_num_entities(entities / len(table_files))

    type_distribution = dict()

    for entity in entity_set:
        types = 

    return stats

# Returns array of Stats instances, one for each benchmark
# 1: Wikitables 2013 - DBpedia
# 2: Wikitables 2019 - DBpedia
# 3: Wikitables 2013 - Wikidata
# 4: Wikitables 2019 - Wikidata
def load_stats():
    stats = list()

    with open('.Wikitables2013_DBpedia.stats', 'rb') as file:
        wiki = pickle.load(file)
        stats.append(wiki)

    with open('.Wikitables2019_DBpedia.stats', 'rb') as file:
        wiki = pickle.load(file)
        stats.append(wiki)

    with open('.Wikitables2013_Wikidata.stats', 'rb') as file:
        wiki = pickle.load(file)
        stats.append(wiki)

    with open('.Wikitables2019_Wikidata.stats', 'rb') as file:
        wiki = pickle.load(file)
        stats.append(wiki)

    return stats

def write_stats(filename, stats):
    with open(filename, 'wb') as file:
        pickle.dump(stats, file, pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Missing argument \'load\' or \'new\'')
        exit(1)

    all_stats = None
    stats_wikitables_dbpedia_2013 = None
    stats_wikitables_dbpedia_2019 = None
    stats_wikitables_wikidata_2013 = None
    stats_wikitables_wikidata_2019 = None

    if sys.argv[1] == 'load':
        all_stats = load_stats()

        if all_stats is None:
            print('No stats have been loaded. You need to use the \'new\' command.')
            exit(1)

        stats_wikitables_dbpedia_2013 = all_stats[0]
        stats_wikitables_dbpedia_2019 = all_stats[1]
        stats_wikitables_wikidata_2013 = all_stats[2]
        stats_wikitables_wikidata_2019 = all_stats[3]

    print('\nAnalyzing Wikitables...')

    if sys.argv[1] == 'new':
        stats_wikitables_dbpedia_2013 = analyze_wikitables(2013, 'dbpedia')
        stats_wikitables_dbpedia_2019 = analyze_wikitables(2019, 'dbpedia')
        stats_wikitables_wikidata_2013 = analyze_wikitables(2013, 'wikidata')
        stats_wikitables_Wikidata_2019 = analyze_wikitables(2019, 'wikidata')
        write_stats('.Wikitables2013_DBpedia.stats', stats_wikitables_dbpedia_2013)
        write_stats('.Wikitables2019_DBpedia.stats', stats_wikitables_dbpedia_2019)
        write_stats('.Wikitables2013_Wikidata.stats', stats_wikitables_wikidata_2013)
        write_stats('.Wikitables2019_Wikidata.stats', stats_wikitables_Wikidata_2019)

    print('Wikitables 2013 stats (DBpedia):')
    stats_wikitables_dbpedia_2013.print()
    print('\nWikitables 2019 stats (DBpedia):')
    stats_wikitables_dbpedia_2019.print()
    print('Wikitables 2013 stats (Wikidata):')
    stats_wikitables_wikidata_2013.print()
    print('Wikitables 2019 stats (Wikidata):')
    stats_wikitables_Wikidata_2019.print()
