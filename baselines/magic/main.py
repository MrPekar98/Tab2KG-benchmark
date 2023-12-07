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
    def __init__(self, connector, structured_file, header, index_col, main_col):
        super().__init__(connector, structured_file, header, index_col, main_col,'http://dbpedia.org/property/','http://www.w3.org/1999/02/22-rdf-syntax-ns#type§', skip_list_db)

    def search_entity_api(self, entity):
        try:
            data = {'confidence': 0.1, 'text': entity}
            headers = {
                'Accept': 'application/json',
            }
            response = requests.post('http://localhost:2222/rest/candidates', headers=headers, data=data)
            js = json.loads(response.text)

            if isinstance(js['annotation']['surfaceForm'],list):
                data = []
                for s in js['annotation']['surfaceForm']:
                    if isinstance(s['resource'], list):
                        data.extend(['http://dbpedia.org/resource/'+r['@uri'] for r in s['resource']])
                    else:
                        data.extend(['http://dbpedia.org/resource/'+s['resource']['@uri']])
            else:
                if isinstance(js['annotation']['surfaceForm']['resource'], list):
                    data = ['http://dbpedia.org/resource/' + r['@uri'] for r in js['annotation']['surfaceForm']['resource']]
                else:
                    data = ['http://dbpedia.org/resource/' + js['annotation']['surfaceForm']['resource']['@uri']]

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
            print('DATA', data)

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

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print('Usage: python main.py <KG> <KG HDT FILE> <CSV CORPUS> <RESULT DIRECTORY>')
        exit(1)

    kg = sys.argv[1]
    hdt = sys.argv[2]
    corpus = sys.argv[3]
    output = sys.argv[4]

    if not corpus.endswith('/'):
        corpus += '/'

    if not output.endswith('/'):
        output += '/'

    store = HDTStore(hdt)
    g = Graph(store)
    connector = HDTConnector()
    runtimes = dict()

    counter = 0

    for file in tqdm(glob.glob(corpus + '*.csv')):
        if counter > 3:
            break

        counter += 1

        name = file.split('/')[-1].split('.')[0]
        annotator = None
        print('Linking ' + name)

        start = time.time() * 1000

        if kg == 'dbpedia':
            annotator = DBMagic(connector, file, 0, None, 0)

        elif kg == 'wikidata':
            annotator = WikiMagic(connector, file, 0, None, 0)

        annotator.annotate()
        annotator.export_files('test')

        duration = time.time() * 1000 - start
        runtimes[name] = duration

    with open(output + 'runtimes.csv', 'w') as file:
        writer = csv.writer(file, delimiter = ',')
        writer.writerow(['table', 'miliseconds'])

        for table in runtimes.keys():
            writer.writerow([table, runtimes[table]])
