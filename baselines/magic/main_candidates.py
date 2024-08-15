import glob
import pandas as pd
from tqdm import tqdm
import json
import requests
import os
import sys
import time
import csv
import re

skip_list_db = ['http://schema.org/', 'http://www.w3.org/2004/02/skos/core', 'http://www.w3.org/2002/07/owl#sameAs',
            'http://dbpedia.org/property/wikiPageUsesTemplate','http://dbpedia.org/ontology/wikiPageWikiLink',
                'http://purl.org/dc/terms/subject', 'http://www.w3.org/2002/07/owl#Thing']
skip_list_wiki = ['http://schema.org/', 'http://www.w3.org/2004/02/skos/core', 'http://www.wikidata.org/prop/P',
            'http://www.wikidata.org/prop/direct-normalized/P','http://www.wikidata.org/entity/statement/']

global g

class DBMagic:
    def __init__(self, endpoint_ip):
        self.endpoint = endpoint_ip

    def search_entity_api(self, entity):
        data = []

        try:
            response = requests.get('http://' + self.endpoint + ':7000/search?query=' + entity.replace(' ', '%20') + '&fuzzy=true')
            js = json.loads(response.text)

            if 'output' in js.keys():
                for output in js['output']:
                    entity = output['entity']
                    data.append(entity)

        except:
            data = []

        return data

class WikiMagic:
    def __init__(self, endpoint_ip):
        self.endpoint = endpoint_ip

    def search_entity_api(self, entity):
        data = []

        try:
            response = requests.get('http://' + self.endpoint + ':7000/search?query=' + entity.replace(' ', '%20') + '&postfix_scoring=false&fuzzy=true')
            js = json.loads(response.text)

            if 'output' in js.keys():
                for output in js['output']:
                    entity = output['entity']
                    data.append(entity)

        except:
            data = []

        return data

def file_columns(file):
    with open(file, 'r') as file:
        reader = csv.reader(file)
        return len(next(reader))

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print('Usage: python main.py <KG> <CSV CORPUS> <RESULT DIRECTORY> <KEYWORD SEARCH ENDPOINT IP>')
        exit(1)

    kg = sys.argv[1]
    corpus = sys.argv[2]
    output = sys.argv[3]
    endpoint_ip = sys.argv[4]

    if not corpus.endswith('/'):
        corpus += '/'

    if not output.endswith('/'):
        output += '/'

    api = None

    if kg == 'dbpedia':
        api = DBMagic(endpoint_ip)

    elif kg == 'wikidata':
        api = WikiMagic(endpoint_ip)

    for file in tqdm(glob.glob(corpus + '*.csv')):
        with open(file, 'r') as input_handle:
            with open(output + file.split('/')[-1], 'w') as out_handle:
                writer = csv.writer(out_handle)
                column_count = file_columns(file)
                name = file.split('/')[-1].split('.')[0]
                annotator = None
                print('Linking ' + name)

                for i in range(column_count):
                    df = pd.read_csv(file, index_col = i)
                    j = 0

                    for k, row in df.iterrows():
                        if i < len(row) and isinstance(row[i], (str)):
                            candidates = api.search_entity_api(re.sub("[\(\[].*?[\)\]]", "", row[i]))
                            cand_str = ""

                            for candidate in candidates:
                                cand_str += candidate + ' '

                            cand_str = cand_str[:-1]
                            tuple = [name.replace('.csv', ''), j, i, cand_str]
                            writer.writerow(tuple)

                        j += 1
