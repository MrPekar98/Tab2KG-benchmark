import os
import json
from neo4j import GraphDatabase

tables_dir = '/home/wikitables/wikitables/'
out_dir = '/benchmarks/wikidata/wikitables/'
tables = os.listdir(tables_dir)
wiki_predicate = None
sameas_predicate = None
progress = 0

def get_predicate(tx, predicate_sub_str):
    results = tx.run('MATCH (a:Resource)-[l]->(b:Resource) RETURN DISTINCT l as predicate')

    for result in list(results):
        predicate = result.data()['predicate']

        if predicate_sub_str in predicate:
            return predicate

    return None

def dbpedia_link(tx, link, predicate):
    result = tx.run('MATCH (a:Resource)-[l:$predicate]->(b:Resource) WHERE b.uri in [$link] RETURN a.uri as mention', link = link, predicate = predicate)
    return list(result)

def to_wikidata(tx, dbpedia_uri, predicarte):
    result = tx.run('MATCH (a.Resource)-(l:$predicate)->(b.Resource) WHERE a.uri in [$uri] RETURN b.uri as wikidata', predicate = predicate, uri = dbpedia_uri)
    return list(result)

def get_uri(link):
    global wiki_predicate
    global sameas_predicate
    URI = 'bolt://localhost:7687'
    AUTH = ('neo4j', 'admin')

    with GraphDatabase.driver(URI, auth = AUTH) as driver:
        driver.verify_connectivity()

        with driver.session(database = 'neo4j') as session:
            if wiki_predicate is None:
                wiki_predicate = session.execute_read(get_predicate, 'isPrimaryTopicOf')
                print('ISPRIMARYTOPICOF: ' + wiki_predicate)

            if sameas_predicate is None:
                sameas_predicate = session.execute_read(get_predicate, 'sameas')
                print('SAMEAS: ' + sameas_predicate)

            uris = session.execute_read(dbpedia_link, link, wiki_predicate)

            for uri in uris:
                wikidata_uris = session.execute_read(to_wikidata, uri, sameas_predicate)

                for wikidata_uri in wikidata_uris:
                    return wikidata_uri.data()['wikidata']

                return None

            return None

for table in tables:
    print(' ' * 100, end = '\r')
    print('Progress: ' + str((progress / len(tables)) * 100)[0:5] + '%', end = '\r')
    progress += 1

    print('\nHERE 1');

    with open(tables_dir + table, 'r') as file:
        tab = json.load(file)
        new_table = {'table': list()}
        print('HERE 2')

        with open(out_dir + table, 'w') as out_file:
            for row in tab['rows']:
                j_row = list()
                print('HERE 3')

                for column in row:
                    j_column = dict()
                    j_column['text'] = column['text']
                    j_column['entity'] = ''
                    print('HERE 4')

                    if len(column['links']) > 0:
                        print('HERE 5')
                        uri = get_uri(column['links'][0].replace('http://www.', 'http://en.'))
                        print('HERE 6')

                        if not uri is None:
                            j_column['entity'] = uri

                    j_row.append(j_column)

                new_table['table'].append(j_row)

            json.dump(new_table, out_file)
