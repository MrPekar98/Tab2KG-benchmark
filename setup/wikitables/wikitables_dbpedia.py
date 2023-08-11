import os
import json
from neo4j import GraphDatabase

tables_dir = 'wikitables/'
out_dir = 'benchmark/wikitables/'
tables = os.listdir(tables_dir)
progress = 0

def query(tx, link):
    result = tx.run('MATCH (a:Resource)-[l:ns109__isPrimaryTopicOf]->(b:Resource) WHERE b.uri in [$link] RETURN a.uri as mention', link = link)
    return list(result)

def get_uri(link):
    URI = 'bolt://localhost:7687'
    AUTH = ('neo4j', 'admin')

    with GraphDatabase.driver(URI, auth = AUTH) as driver:
        driver.verify_connectivity()


        with driver.session(database = 'neo4j') as session:
            uris = session.execute_read(query, link)

            for uri in uris:
                return uri.data()['mention']

            return None

for table in tables:
    print(' ' * 100, end = '\r')
    print('Progress: ' + str((progress / len(tables)) * 100)[0:5] + '%', end = '\r')
    progress += 1

    with open(tables_dir + table, 'r') as file:
        tab = json.load(file)
        new_table = {'table': list()}

        with open(out_dir + table, 'w') as out_file:
            for row in tab['rows']:
                j_row = list()

                for column in row:
                    j_column = dict()
                    j_column['text'] = column['text']
                    j_column['entity'] = ''

                    if len(column['links']) > 0:
                        uri = get_uri(column['links'][0].replace('http://www.', 'http://en.'))

                        if not uri is None:
                            j_column['entity'] = uri

                    j_row.append(j_column)

                new_table['table'].append(j_row)

            json.dump(new_table, out_file)
