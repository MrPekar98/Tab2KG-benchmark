# Command: 'python3 analysis.py (load|new)'
# 'load': Show the stats already computed once
# 'new': Re-compute the stats

import os
import sys
import json
import csv
import pickle
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from stats import Stats
from neo4j import GraphDatabase
from collections import Counter

URI = 'bolt://localhost:7687'
AUTH = ('neo4j', 'admin')

def query_types(tx, entity, predicate):
    result = tx.run('MATCH (a:Resource)-[l:' + predicate + ']->(b:Resource) WHERE a.uri in [$entity] RETURN b.uri as type', entity = entity)
    return list(result)

def predicates(tx):
    results = tx.run('CALL db.relationshipTypes() YIELD relationshipType RETURN relationshipType as predicate')
    return list(results)

def type_predicate():
    with GraphDatabase.driver(URI, auth = AUTH) as driver:
        with driver.session(database = 'neo4j') as session:
            preds = session.execute_read(predicates)

            for predicate in preds:
                pred = predicate.data()['predicate']

                if 'type' in pred and 'rdf' in pred:
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

def analyze_tough_tables():
    dir = '/home/setup/tough_tables/ToughTablesR2-DBP/Test/tables/'
    files = os.listdir(dir)
    rows = 0
    columns = 0
    entities = 0
    entity_set = set()
    entity_map = dict()
    stats = Stats()
    type_pred = type_predicate()

    for file in files:
        with open(dir + file, 'r') as fd:
            handle = csv.reader(fd)
            tmp_columns = 0

            for line in handle:
                rows += 1
                tmp_columns = len(line)

            columns += tmp_columns

    stats.set_tables(len(files))
    stats.set_rows(rows / len(files))
    stats.set_columns(columns / len(files))

    gt_file = '/home/setup/tough_tables/ToughTablesR2-DBP/Test/gt/cea_gt.csv'

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

    type_distribution = dict()
    stats.set_num_entities(entities / len(entity_map.keys()))

    for entity in entity_set:
        types = entity_types(entity, type_pred)

        for type in types:
            type = type.split('/')[-1].split('#')[-1]

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
    plt.savefig('/plots/ToughTables-DBpedia.pdf')

    return stats

# Returns array of Stats instances, one for each benchmark
# 1: ToughTables - DBpedia
# 2: ToughTables - Wikidata
def load_stats():
    with open('/plots/.ToughTables_DBpedia.stats', 'rb') as file:
        tt = pickle.load(file)
        return tt

def write_stats(filename, stats):
    with open(filename, 'wb') as file:
        pickle.dump(stats, file, pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Missing argument \'load\' or \'new\'')
        exit(1)

    stats_tough_tables_dbpedia = None

    if sys.argv[1] == 'load':
        stats_tough_tables_dbpedia = load_stats()

        if stats_tough_tables_dbpedia is None:
            print('No stats have been loaded. You need to use the \'new\' command.')
            exit(1)

    print('\nAnalyzing ToughTables... (DBpedia)')

    if sys.argv[1] == 'new':
        stats_tough_tables_dbpedia = analyze_tough_tables()
        write_stats('/plots/.ToughTables_DBpedia.stats', stats_tough_tables_dbpedia)

    stats_tough_tables_dbpedia.print()
