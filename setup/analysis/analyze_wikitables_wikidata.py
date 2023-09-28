# Command: 'python3 analysis.py (load|new)'
# 'load': Show the stats already computed once
# 'new': Re-compute the stats

import os
import sys
import json
import csv
import pickle
import statistics
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from stats import Stats
from neo4j import GraphDatabase
from collections import Counter

URI = 'bolt://localhost:7687'
AUTH = ('neo4j', 'admin')

def query_types(tx, entity, predicate):
    result = tx.run('MATCH (a:Resource)-[l:' + predicate + ']->(b:Resource) WHERE a.uri in [$entity] RETURN b.uri as type', entity = entity)
    return list(result)

def predicates(tx):
    result = tx.run('CALL db.relationshipTypes() YIELD relationshipType RETURN relationshipType as predicate')
    return list(result)

def type_predicate():
    with GraphDatabase.driver(URI, auth = AUTH) as driver:
        with driver.session(database = 'neo4j') as session:
            preds = session.execute_read(predicates)

            for predicate in preds:
                pred = predicate.data()['predicate']

                if pred.endswith('P31'):
                    return pred

            return None

def entity_types(entity, predicate):
    types = set()

    with GraphDatabase.driver(URI, auth = AUTH) as driver:
        with driver.session(database = 'neo4j') as session:
            results = session.execute_read(query_types, entity, predicate)

            for type in results:
                types.add(type.data()['type'])

            return types

def analyze_wikitables(version, kg):
    stats = Stats()
    rows = 0
    columns = 0
    entities = 0
    entity_set = set()
    dir = '/home/benchmarks/' + kg + '/wikitables_' + str(version) + '/'
    table_files = os.listdir(dir)
    type_pred = type_predicate()

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
        types = entity_types(entity, type_pred)

        for type in types:
            type = type.split('/')[-1]

            if type not in type_distribution.keys():
                type_distribution[type] = 0

            type_distribution[type] += 1

    counter = Counter(type_distribution)
    type_distribution = {k:v for k, v in counter.most_common()[:25]}
    fig, ax = plt.subplots(figsize = (12, 11))
    data = pd.DataFrame()
    data['Entity types'] = list(type_distribution.keys())
    data['Type frequency'] = list(type_distribution.values())
    plot = sns.barplot(data, x = 'Entity types', y = 'Type frequency', ax = ax)
    plot.set_xticklabels(plot.get_xticklabels(), rotation = 30, horizontalalignment = 'right')
    plt.savefig('/plots/Wikitables-Wikidata_' + str(version) + '.pdf')

    return stats

# Returns array of Stats instances, one for each benchmark
# 1: Wikitables 2013 - Wikidata
# 2: Wikitables 2019 - Wikidata
def load_stats():
    stats = list()

    with open('/plots/.Wikitables2013_Wikidata.stats', 'rb') as file:
        wiki = pickle.load(file)
        stats.append(wiki)

    with open('/plots/.Wikitables2019_Wikidata.stats', 'rb') as file:
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
    stats_wikitables_wikidata_2013 = None
    stats_wikitables_wikidata_2019 = None

    if sys.argv[1] == 'load':
        all_stats = load_stats()

        if all_stats is None:
            print('No stats have been loaded. You need to use the \'new\' command.')
            exit(1)

        stats_wikitables_wikidata_2013 = all_stats[0]
        stats_wikitables_wikidata_2019 = all_stats[1]

    print('\nAnalyzing Wikitables...')

    if sys.argv[1] == 'new':
        stats_wikitables_wikidata_2013 = analyze_wikitables(2013, 'wikidata')
        stats_wikitables_Wikidata_2019 = analyze_wikitables(2019, 'wikidata')
        write_stats('/plots/.Wikitables2013_Wikidata.stats', stats_wikitables_wikidata_2013)
        write_stats('/plots/.Wikitables2019_Wikidata.stats', stats_wikitables_Wikidata_2019)

    print('Wikitables 2013 stats (Wikidata):')
    stats_wikitables_wikidata_2013.print()
    print('Wikitables 2019 stats (Wikidata):')
    stats_wikitables_Wikidata_2019.print()
