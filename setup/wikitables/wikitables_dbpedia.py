import sys
import os
import json
import csv
from neo4j import GraphDatabase

if len(sys.argv) < 2:
    print('Missing version year')
    exit(1)

version = sys.argv[1]
tables_dir = '/home/wikitables/wikitables_20' + version + '/'
out_dir = '/benchmarks/wikitables_20' + version + '/'
tables = os.listdir(tables_dir)
URI = 'bolt://localhost:7687'
AUTH = ('neo4j', 'admin')
isPrimaryTopicOf = None
progress = 0

def query(tx, link):
    result = tx.run('MATCH (a:Resource)-[l:' + isPrimaryTopicOf + ']->(b:Resource) WHERE b.uri in [$link] RETURN a.uri as mention', link = link)
    return set(result)

def predicate_query(tx):
    result = tx.run('CALL db.relationshipTypes() YIELD relationshipType RETURN relationshipType as predicate')
    return list(result)

def get_predicate():
    with GraphDatabase.driver(URI, auth = AUTH) as driver:
        driver.verify_connectivity()

        with driver.session(database = 'neo4j') as session:
            predicates = session.execute_read(predicate_query)

            for predicate in predicates:
                pred = predicate.data()['predicate']

                if 'isPrimaryTopicOf' in pred:
                    return pred

            return None

def get_uri(link):
    with GraphDatabase.driver(URI, auth = AUTH) as driver:
        driver.verify_connectivity()

        with driver.session(database = 'neo4j') as session:
            uris = session.execute_read(query, link)

            for uri in uris:
                return uri.data()['mention']

            return None

isPrimaryTopicOf = get_predicate()

if isPrimaryTopicOf is None:
    print('Could not find predicate')
    exit(1)

with open(out_dir + 'gt/dbpedia/gt.csv', 'w') as out_gt:
    for table in tables:
        print(' ' * 100, end = '\r')
        print('Progress: ' + str((progress / len(tables)) * 100)[0:5] + '%', end = '\r')
        progress += 1
        table_id = table.replace('.json', '')

        with open(tables_dir + table, 'r') as file:
            tab = json.load(file)
            new_table = {'table': list()}

            with open(out_dir + 'tables/' + table_id + '.csv', 'w') as out_file:
                writer = csv.writer(out_file, delimiter = ',')
                header = []

                for column in tab['headers']:
                    header.append(column['text'])

                writer.writerow(header)

                gt_writer = csv.writer(out_gt, delimiter = ',')
                row_idx = 0

                for row in tab['rows']:
                    table_row = []
                    column_idx = 0
                    j_row = list()

                    for column in row:
                        table_row.append(column['text'])

                        if len(column['links']) > 0:
                            uri = get_uri(column['links'][0].replace('http://www.', 'http://en.'))

                            if not uri is None:
                                gt_writer.writerow([table_id, row_idx, column_idx, uri])

                        column_idx += 1

                    writer.writerow(table_row)
                    row_idx += 1

sub_out_dir = out_dir + 'tables_subset/'
out_tables = os.listdir(out_dir + 'tables/')
i = 0
os.makedirs(sub_out_dir)

for table in out_tables:
    shutil.copy(out_dir + 'tables/' + table, sub_out_dir + table)
    i += 1

    if i == 10000:
        break

print('Done')
