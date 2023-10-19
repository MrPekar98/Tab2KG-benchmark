import sys
import os
import json
import csv
from neo4j import GraphDatabase

if len(sys.argv) < 2:
    print('Missing version year')
    exit(1)

version = sys.argv[1]
gt_file = '/benchmarks/wikitables_20' + version + '/gt/dbpedia/gt.csv'
gt_out = '/benchmarks/wikitables_20' + version + '/gt/wikidata/gt.csv'
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

print('All CSV tables for Wikitables aldready exist. Generating ground truth for Wikidata')

with open(gt_file, 'r') as in_file:
    reader = csv.reader(in_file, delimiter = ',')

    with open(gt_out, 'w') as out_file:
        writer = csv.writer(out_file, delimiter = ',')

        for row in reader:
            table_id = row[0]
            table_row = row[1]
            table_column = row[2]
            dbpedia_entity = row[3]
            wikidata_entity = get_uri(dbpedia_entity)

            if not wikidata_entity is None:
                writer.writerow([table_id, table_row, table_column, wikidata_entity])
