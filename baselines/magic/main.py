from MAGIC import Magic
from rdflib_hdt import HDTStore
from ink.base.connectors import AbstractConnector
from rdflib import Graph
import awena
import glob
import pandas as pd
from tqdm import tqdm
import json
import requests
import os
import sys
import time
import csv

skip_list_db = ['http://schema.org/', 'http://www.w3.org/2004/02/skos/core', 'http://www.w3.org/2002/07/owl#sameAs',
            'http://dbpedia.org/property/wikiPageUsesTemplate','http://dbpedia.org/ontology/wikiPageWikiLink',
                'http://purl.org/dc/terms/subject', 'http://www.w3.org/2002/07/owl#Thing']
skip_list_wiki = ['http://schema.org/', 'http://www.w3.org/2004/02/skos/core', 'http://www.wikidata.org/prop/P',
            'http://www.wikidata.org/prop/direct-normalized/P','http://www.wikidata.org/entity/statement/']

global g

class DBMagic(Magic):
    def __init__(self, endpoint_ip, connector, structured_file, header, index_col, main_col):
        super().__init__(connector, structured_file, header, index_col, main_col,'http://dbpedia.org/property/','http://www.w3.org/1999/02/22-rdf-syntax-ns#type§', skip_list_db)
        self.endpoint = endpoint_ip

    def search_entity_api(self, entity):
        data = []

        try:
            response = requests.get('http://' + self.endpoint + ':7000/search?query=' + entity.replace(' ', '%20'))
            js = json.loads(response.text)

            if 'output' in js.keys():
                for output in js['output']:
                    entity = output['entity']
                    data.append(entity)

            else:
                data = []

        except:
            data = []

        return data

class WikiMagic(Magic):
    def __init__(self, connector, structured_file, header, index_col, main_col):
        super().__init__(connector, structured_file, header, index_col, main_col,'http://www.wikidata.org/prop/direct/', 'http://www.wikidata.org/prop/direct/P31§', skip_list_wiki)
        self.crawler = awena.Crawler('en', connector)

    def search_entity_api(self, entity):
        try:
            entity = entity.split(',')[0]
            data = ['http://www.wikidata.org/entity/' + x for x in self.crawler.search(entity)]

        except:
            data = []

        return data

class HDTConnector(AbstractConnector):
    def __init__(self):
        self.db_type = 'rdflib'

    def query(self, q_str):
        res = g.query(q_str)
        return json.loads(res.serialize(format="json"))['results']['bindings']

    def query_relation(self, ind, rel):
        q_str="""
        SELECT ?o ?l WHERE {
            <"""+str(ind)+"> <"+str(rel)+"> ?o"+""".
            ?o <http://www.w3.org/2000/01/rdf-schema#label> ?l .
            FILTER (langMatches( lang(?l), "EN" ) )
        }
        """
        res = g.query(q_str)
        return json.loads(res.serialize(format="json"))['results']['bindings']

    def query_column(self, rel):
        q_str="""
        SELECT ?s ?o ?l WHERE {
            ?s"""+" <"+str(rel)+"> ?o"+""".
        }
        ORDER BY RAND() 
        LIMIT 250
        """
        res = g.query(q_str)
        return json.loads(res.serialize(format="json"))['results']['bindings']

    def inv_query(self, q_str):
        return query(q_str)

def file_columns(file):
    with open(file, 'r') as file:
        reader = csv.reader(file)
        return len(next(reader))

def create_temp_file_by_column(file, column):
    dir = file.split
    new_name = file.replace('.csv', '_column-' + str(column) + '.csv')

    with open(file, 'r') as file:
        with open(new_name, 'w') as temp_file:
            reader = csv.reader(file)
            writer = csv.writer(temp_file, delimiter = ',')

            for row in reader:
                writer.writerow(row[column:])

    return new_name

def delete_temp_file(file, column):
    os.remove(file.replace('.csv', '_column-' + str(column) + '.csv'))

def clean_empty_results(dir):
    files = os.listdir(dir)

    for file in files:
        row_count = 0

        with open(dir + file, 'r') as csv_file:
            reader = csv.reader(csv_file)

            for row in reader:
                row_count += 1

        if row_count == 0:
            os.remove(dir + file)

if __name__ == '__main__':
    if len(sys.argv) < 6:
        print('Usage: python main.py <KG> <KG HDT FILE> <CSV CORPUS> <RESULT DIRECTORY> <KEYWORD SEARCH ENDPOINT IP>')
        exit(1)

    kg = sys.argv[1]
    hdt = sys.argv[2]
    corpus = sys.argv[3]
    output = sys.argv[4]
    endpoint_ip = sys.argv[5]

    if not corpus.endswith('/'):
        corpus += '/'

    if not output.endswith('/'):
        output += '/'

    store = HDTStore(hdt)
    g = Graph(store)
    connector = HDTConnector()
    runtimes = dict()

    for file in tqdm(glob.glob(corpus + '*.csv')):
        column_count = file_columns(file)
        name = file.split('/')[-1].split('.')[0]
        annotator = None
        runtime_sum = 0
        print('Linking ' + name)

        for i in range(column_count):
            sub_file = create_temp_file_by_column(file, i)
            start = time.time() * 1000

            if kg == 'dbpedia':
                annotator = DBMagic(endpoint_ip, connector, sub_file, 0, None, 0)

            elif kg == 'wikidata':
                annotator = WikiMagic(connector, sub_file, 0, None, 0)

            annotator.annotate()
            annotator.export_files(output + name + '_column-' + str(i))

            runtime_sum += time.time() * 1000 - start
            delete_temp_file(file, i)

        duration = runtime_sum
        runtimes[name] = duration

        with open(output + 'runtimes.csv', 'w') as file:
            writer = csv.writer(file, delimiter = ',')
            writer.writerow(['table', 'miliseconds'])

            for table in runtimes.keys():
                writer.writerow([table, runtimes[table]])

    clean_empty_results(output)
