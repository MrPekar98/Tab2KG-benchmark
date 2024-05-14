from enum import Enum
import json
from pprint import pprint
import time
from urllib import parse, request
import pandas as pd
import numpy as np
import os
import sys
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import csv

class KG(Enum):
        DBpedia = 0
        Wikidata = 1
        Google = 2
        All = 3

class URI_KG(object):
    dbpedia_uri_resource = 'http://dbpedia.org/resource/'
    dbpedia_uri_property = 'http://dbpedia.org/property/'

    dbpedia_uri = 'http://dbpedia.org/ontology/'
    wikidata_uri ='http://www.wikidata.org/'
    schema_uri = 'http://schema.org/'

    uris = list()
    uris.append(dbpedia_uri)
    uris.append(wikidata_uri)
    uris.append(schema_uri)

    uris_resource = list()
    uris_resource.append(dbpedia_uri_resource)
    uris_resource.append(wikidata_uri)

    avoid_predicates=set()
    avoid_predicates.add("http://dbpedia.org/ontology/wikiPageDisambiguates")
    avoid_predicates.add("http://dbpedia.org/ontology/wikiPageRedirects")
    avoid_predicates.add("http://dbpedia.org/ontology/wikiPageWikiLink")
    avoid_predicates.add("http://dbpedia.org/ontology/wikiPageID")

    def __init__(self):
        ''''
        '''

class KGEntity(object):
    def __init__(self, enity_id, label, description, types, source):

        self.ident = enity_id
        self.label = label
        self.desc = description #sometimes provides a very concrete type or additional semantics
        self.types = types  #set of semantic types
        self.source = source  #KG of origin such as dbpedia, wikidata or google KG

    def __repr__(self):
        return "<id: %s , label: %s, description: %s, types: %s, source: %s>" % (self.ident, self.label,self.desc, self.types, self.source)

    def __str__(self):
        return "<id: %s , label: %s, description: %s, types: %s, source: %s>" % (self.ident, self.label, self.desc, self.types, self.source)

    def getId(self):
        return self.ident

    '''
    One can retrieve all types or filter by KG: DBpedia, Wikidata and Google (Schema.org)
    '''
    def getTypes(self, kgfilter=KG.All):
        if kgfilter==KG.All:
            return self.types
        else:
            kg_uri = URI_KG.uris[kgfilter.value]
            filtered_types = set()
            for t in self.types:
                if t.startswith(kg_uri):
                    filtered_types.add(t)

            return filtered_types

    def getLabel(self):
        return self.label

    def getDescription(self):
        return self.desc

    def getSource(self):
        return self.sourcec

    def addType(self, cls):
        self.types.add(cls)

    def addTypes(self, types):
        self.types.update(types)

class KGLookup(object):
    '''
    classdocs
    '''
    def __init__(self, lookup_url):
        self.service_url = lookup_url

    def getJSONRequest(self, params, attempts=1):
        try:
            #urllib has been split up in Python 3.
            #The urllib.urlencode() function is now urllib.parse.urlencode(),
            #and the urllib.urlopen() function is now urllib.request.urlopen().
            #url = service_url + '?' + urllib.urlencode(params)
            url = self.service_url + '?' + parse.urlencode(params)
            #print(url)
            #response = json.loads(urllib.urlopen(url).read())

            req = request.Request(url)
            req.add_header('Accept', 'application/json')
            response = json.loads(request.urlopen(req).read())

            return response

        except:
            print("Lookup '%s' failed. Attempts: %s" % (url, str(attempts)))
            time.sleep(60) #to avoid limit of calls, sleep 60s
            attempts-=1
            if attempts>0:
                return self.getJSONRequest(params, attempts)
            else:
                return None

'''
Wikidata web search API
'''
class WikidataAPI(KGLookup):
    '''
    classdocs
    '''
    def __init__(self, endpoint):
        '''
        Constructor
        '''
        self._endpoint = endpoint
        super().__init__(self.getURL())

    def getURL(self):
        return self._endpoint + 'search'

    def __createParams(self, query, limit, type='item'):
        params = {
            'format' : 'json',
            'query': query.replace(' ', '%20'),
            'k': limit,
            'postfix_scoring': 'false',
            'fuzzy': 'true'
        }

        return params

    def getKGName(self):
        return 'Wikidata'

    '''
    Returns list of ordered entities according to relevance: wikidata
    '''
    def __extractKGEntities(self, json, filter=''):
        entities = list()

        for element in json['output']:
            #empty list of type from wikidata lookup
            types = set()

            description=''
            if 'description' in element:
                description = element['description']

            label=''
            if 'label' in element:
                label = element['label']

            kg_entity = {'uri': element['entity'], 'label': label, 'description': description}
            entities.append(kg_entity)

        #for entity in entities:
        #    print(entity)
        return entities

    def getKGEntities(self, query, limit, type='item', filter=''):
        json = self.getJSONRequest(self.__createParams(query, limit, type))

        if json==None:
            print("None results for", query)
            return list()

        return self.__extractKGEntities(json, filter) #Optionally filter by URI

class DBpediaAPI(KGLookup):
    '''
    classdocs
    '''
    def __init__(self, endpoint):
        '''
        Constructor
        '''
        self._endpoint = endpoint
        super().__init__(self.getURL())

    def getURL(self):
        return self._endpoint + 'search'

    def getKGName(self):
        return 'DBpedia'

    def __createParams(self, query, limit, type='item'):
        params = {
            'k' : limit,
            'query': query.replace(' ', '%20'),
            'format': 'json',
            'fuzzy': 'true'
        }

        return params

    '''
    Returns list of ordered entities according to relevance: wikidata
    '''
    def __extractKGEntities(self, json, filter=''):
        entities = list()

        for element in json['output']:
            #empty list of type from wikidata lookup
            types = set()

            description=''
            if 'description' in element:
                description = element['description']

            label=''
            if 'label' in element:
                label = element['label']

            entities.append({'uri': element['entity'], 'label': label, 'description': description})

        #for entity in entities:
        #    print(entity)
        return entities

    def getKGEntities(self, query, limit, type='item', filter=''):
        json = self.getJSONRequest(self.__createParams(query, limit, type))

        if json==None:
            print("None results for", query)
            return list()

        return self.__extractKGEntities(json, filter) #Optionally filter by URI

def capitalize_word(word):
    return word.capitalize()

def remove_special_signs(word):
    result = ""
    for w in word:
        if w.isalpha() or w=="'" or w.isspace() or w== "©" or w == "Ã":
            result += w
    return result

def replace_space(word):
    try:
        return word.replace(" ", "_")
    except:
        print(word)
        return word

def cosine(cell, entity):
    cell = cell.replace('_', ' ')

    for k in range(0, 1):
        cell_list = word_tokenize(cell)
        entity_list = word_tokenize(entity)
        sw = stopwords.words('english')
        cell_set = {w for w in cell_list if not w in sw}
        entity_set = {w for w in entity_list if not w in sw}
        rvector = cell_set.union(entity_set)
        l1 = []
        l2 = []
        c = 0
        cosines = []

        for w in rvector:
            if w in cell_set:
                l1.append(1)

            else:
                l1.append(0)

            if w in entity_set:
                l2.append(1)

            else:
                l2.append(0)

        for i in range(len(rvector)):
            c += l1[i] * l2[i]

        try:
            return c / float((sum(l1) * sum(l2))**0.5)

        except ZeroDivisionError:
            return 0

if __name__ == '__main__':
    if len(sys.argv) < 6:
        print('Specify KG, table directory, output directory, number of candidates to generate, and endpoint hostname')
        exit(1)

    kg = sys.argv[1]
    kg_type = -1
    output_dir = sys.argv[3]
    candidates = int(sys.argv[4])
    endpoint = sys.argv[5]

    if kg == 'wikidata':
        print(URI_KG.uris[KG.Wikidata.value])
        print(KG.Wikidata.value)
        kg_type = KG.Wikidata.value

    elif kg == 'dbpedia':
        print(URI_KG.uris[KG.DBpedia.value])
        print(KG.DBpedia.value)
        kg_type = KG.DBpedia.value

    else:
        print('KG argument \'' + kg + '\' was not recognized')
        exit(1)

    table_dir = sys.argv[2]

    if not os.path.exists(table_dir):
        print('Table directory \'' + table_dir + '\' does not exist')
        exit(1)

    if not table_dir.endswith('/'):
        table_dir += '/'

    if not output_dir.endswith('/'):
        output_dir += '/'

    runtimes = dict()
    api = None
    limit = candidates
    type = 'item'
    table_list = os.listdir(table_dir)
    table_counter = 1

    if kg_type == KG.Wikidata.value:
        api = WikidataAPI(endpoint)

    elif kg_type == KG.DBpedia.value:
        api = DBpediaAPI(endpoint)

    for table in table_list:
        linked_rows = list()
        input_table = pd.read_csv(table_dir + table)
        start = time.time() * 1000

        for row_index, row in input_table.iterrows():
            column_index = 0

            for column in row:
                if isinstance(column, (float, int)):
                    continue

                entities = api.getKGEntities(column, limit, type)

                if len(entities) > 0:
                    max_cos = -1
                    max_entity = None

                    for entity in entities:
                        if 'uri' in entity.keys() and 'label' in entity.keys():
                            cos = cosine(column, entity['label'])

                            if cos > max_cos:
                                max_cos = cos
                                max_entity = entity['uri']

                    if not max_entity is None:
                        linked_rows.append([row_index, column_index, max_entity])

                column_index += 1

        duration = time.time() * 1000 - start
        runtimes[table.replace('.csv', '')] = duration

        print(' ' * 100, end = '\r')
        print('Table ' + str(table_counter) + '/' + str(len(table_list)), end = '\r')
        table_counter += 1

        with open(output_dir + table, 'w') as result_file:
            writer = csv.writer(result_file, delimiter = ',')

            for row in linked_rows:
                writer.writerow(row)

    with open(output_dir + 'runtimes.csv', 'w') as file:
        writer = csv.writer(file, delimiter = ',')
        writer.writerow(['table', 'miliseconds'])

        for table in runtimes.keys():
            writer.writerow([table, runtimes[table]])
