import sys
import os
import json
from neo4j import GraphDatabase

if len(sys.argv) < 2:
    print('Missing version year')
    exit(1)

version = sys.argv[1]
tables_dir = '/benchmarks/dbpedia/wikitables_20' + version + '/'
out_dir = '/benchmarks/wikidata/wikitables_20' + version + '/'
tables = os.listdir(tables_dir)
URI = 'bolt://localhost:7687'
AUTH = ('neo4j', 'admin')
sameAs = None
progress = 0

def query(tx, link):
    result = tx.run('MATCH (a:Resource)-[l:' + sameAs + ']->(b:Resource) WHERE a.uri in [$link] RETURN b.uri as mention', link = link)
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

                if 'sameAs' in pred:
                    return pred

            return None

def get_uri(link):
    with GraphDatabase.driver(URI, auth = AUTH) as driver:
        driver.verify_connectivity()

        with driver.session(database = 'neo4j') as session:
            uris = session.execute_read(query, link)

            for uri in uris:
                mention = uri.data()['mention']

                if 'wikidata' in mention:
                    return mention

            return None

sameAs = get_predicate()

if sameAs is None:
    print('Could not find predicate')
    exit(1)

for table in tables:
    print(' ' * 100, end = '\r')
    print('Progress: ' + str((progress / len(tables)) * 100)[0:5] + '%', end = '\r')
    progress += 1

    with open(tables_dir + table, 'r') as file:
        tab = json.load(file)
        new_table = {'table': list()}

        with open(out_dir + table, 'w') as out_file:
            for row in tab['table']:
                j_row = list()

                for column in row:
                    j_column = dict()
                    j_column['text'] = column['text']
                    j_column['entity'] = ''

                    if len(column['entity']) > 0:
                        uri = get_uri(column['entity'])

                        if not uri is None:
                            j_column['entity'] = uri

                    j_row.append(j_column)

                new_table['table'].append(j_row)

            json.dump(new_table, out_file)
