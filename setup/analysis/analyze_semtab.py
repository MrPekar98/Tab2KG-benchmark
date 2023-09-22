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
import matplotlib.pyplot as plt
import pandas as pd
from stats import Stats
from neo4j import GraphDatabase

def query_types(tx, entity, predicate):
    result = tx.run('MATCH (a:Resource)-[l:' + predicate + ']->(b:Resource) WHERE a.uri in [$entity] RETURN b.uri as type', entity = entity)
    return list(result)

def predicates(tx):
    results = tx.run('CALL db.relationshipTypes() YIELD relationshipType RETURN relationshipType as predicate')
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

def analyze_semtab():
    base = '/home/setup/semtab/HardTablesR2/DataSets/HardTablesR2/Test/'
    table_dir = base + 'tables/'
    gt_file = base + 'gt/cea_gt.csv'
    files = os.listdir(table_dir)
    stats = Stats()
    rows = 0
    columns = 0
    entities = set()
    type_pred = type_predicate()

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
        with open(dir + file, 'r') as fd:
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
        types = entity_types(entity, type_pred)

        for type in types:
            type = type.split('/')[-1]

            if type not in type_distribution.keys():
                type_distribution[type] = 0

            type_distribution[type] += 1

    median = statistics.median(type_distribution.values())
    type_distribution = dict((k, v) for k, v in type_distribution.items() if v > median)
    fig, ax = plt.subplots(figsize = (12, 11))
    data = pd.DataFrame()
    data['Entity types'] = list(type_distribution.keys())
    data['Type frequency'] = list(type_distribution.values())
    plot = sns.barplot(data, x = 'Entity types', y = 'Type frequency', ax = ax)
    plot.set_xticklabels(plot.get_xticklabels(), rotation = 30, horizontalalignment = 'right')
    plt.savefig('/plots/Wikitables-Wikidata_' + str(version) + '.pdf')

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
