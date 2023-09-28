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

def analyze_web_data_commons():
    dir = '/home/setup/webcommons/tables/'
    gt_dir = '/home/setup/webcommons/instance/'
    table_files = os.listdir(dir)
    gt_files = os.listdir(gt_dir)
    stats = Stats()
    rows = 0
    columns = 0
    entities = 0
    entity_set = set()
    type_pred = type_predicate()

    for table_file in table_files:
        try:
            with open(dir + table_file, 'r') as file:
                obj = json.load(file)
                table = obj['relation']
                rows += len(table[0]) - 1
                columns += len(table)

                if table_file.replace('json', 'csv') in gt_files:
                    with open(gt_dir + table_file.replace('json', 'csv'), 'r') as gt_file:
                        gt_map = dict()
                        row_index = 0
                        handle = csv.reader(gt_file)

                        for line in handle:
                            entity = line[0]
                            index = int(line[2])
                            gt_map[index] = entity

                        for row_val in table[obj['keyColumnIndex']]:
                            if row_index in gt_map.keys():
                                entities += 1
                                entity_set.add(gt_map[row_index])

                            row_index += 1

        except UnicodeDecodeError as e:
            continue

    stats.set_rows(rows / len(table_files))
    stats.set_columns(columns / len(table_files))
    stats.set_num_entities(entities / len(table_files))
    stats.set_tables(len(table_files))

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
    plt.savefig('/plots/WebDataCommons.pdf')

    return stats

# Returns stats
def load_stats():
    with open('/plots/.WebDataCommons.stats', 'rb') as file:
        webcommons = pickle.load(file)
        return webcommons

def write_stats(filename, stats):
    with open(filename, 'wb') as file:
        pickle.dump(stats, file, pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Missing argument \'load\' or \'new\'')
        exit(1)

    stats_web_data_commons = None

    if sys.argv[1] == 'load':
        stats_web_data_commons = load_stats()

        if all_stats is None:
            print('No stats have been loaded. You need to use the \'new\' command.')
            exit(1)

    print('Analyzing WebDataCommons...')

    if sys.argv[1] == 'new':
        stats_web_data_commons = analyze_web_data_commons()
        write_stats('/plots/.WebDataCommons.stats', stats_web_data_commons)

    print('WebDataCommons stats:')
    stats_web_data_commons.print()
