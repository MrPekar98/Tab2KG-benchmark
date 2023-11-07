from enum import Enum
import json
from pprint import pprint
import time
from urllib import parse, request
import pandas as pd
import numpy as np
import os
import sys

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

    def getJSONRequest(self, params, attempts=3):
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
    def __init__(self):
        '''
        Constructor
        '''
        super().__init__(self.getURL())

    def getURL(self):
        return "https://www.wikidata.org/w/api.php"

    def __createParams(self, query, limit, type='item'):
        params = {
            'action': 'wbsearchentities',
            'format' : 'json',
            'search': query,
            'type': type,
            'limit': limit,
            'language' : 'en'
        }

        return params

    def getKGName(self):
        return 'Wikidata'

    '''
    Returns list of ordered entities according to relevance: wikidata
    '''
    def __extractKGEntities(self, json, filter=''):
        entities = list()

        for element in json['search']:
            #empty list of type from wikidata lookup
            types = set()

            description=''
            if 'description' in element:
                description = element['description']

            kg_entity = element['concepturi']

            #We filter according to givem URI
            if filter=='' or element['concepturi']==filter:
                entities.append(kg_entity)

        #for entity in entities:
        #    print(entity)
        return entities

    def getKGEntities(self, query, limit, type='item', filter=''):
        json = self.getJSONRequest(self.__createParams(query, limit, type), 3)

        if json==None:
            print("None results for", query)
            return list()

        return self.__extractKGEntities(json, filter) #Optionally filter by URI

class DBpediaAPI(KGLookup):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        super().__init__(self.getURL())

    def getURL(self):
        return "https://lookup.dbpedia.org/api/search"

    def getKGName(self):
        return 'DBpedia'

    def __createParams(self, query, limit, type='item'):
        params = {
            'format' : 'json',
            'query': query,
            'type': type,
        }

        return params

    '''
    Returns list of ordered entities according to relevance: wikidata
    '''
    def __extractKGEntities(self, json, filter=''):
        entities = list()

        for element in json['docs']:
            #empty list of type from wikidata lookup
            types = set()

            description=''
            if 'description' in element:
                description = element['description']

            kg_entity = element['resource']

            #We filter according to givem URI
            if filter=='' or element['resource']==filter:
                entities.append(kg_entity)

        #for entity in entities:
        #    print(entity)
        return entities

    def getKGEntities(self, query, limit, type='item', filter=''):
        json = self.getJSONRequest(self.__createParams(query, limit, type), 3)

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

def get_entity(df,  row_id, column_id):
    try:
        cell = df.iloc[row_id, column_id]
        #cell = remove_special_signs(cell)
        cell = capitalize_word(cell)
        cell = replace_space(cell)
        return cell
    except:
        return np.nan

def function_for_row(row):
    global first_table
    global table_dir
    table_id = row["Table_id"]
    if first_table == table_id:
        df = pd.read_csv(table_dir + table_id + '.csv', header = None)
    else:
        df = pd.read_csv(table_dir + table_id + '.csv', header = None)
        first_table = table_id
    df.head()

    row_id = row["Row_id"]
    column_id = row["Column_id"]
    cell = get_entity(df, row_id, column_id,)
    row["Cell"]=cell
    return row

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Specify KG and then table directory')
        exit(1)

    kg = sys.argv[1]
    kg_type = -1

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

    df = pd.read_csv('Test/target/cea_target.csv', header=None, nrows=10)
    df.columns=["Table_id", "Row_id", "Column_id"] # Assign the header to the dataframe
    df["Cell"] = ""
    df = df.sort_values("Table_id").reset_index(drop=True)
    first_table = df["Table_id"].unique()[0]
    df = df.apply(function_for_row, axis=1)
    df["KG_Entity"]=''

    for i in range(0, len(df.index)):
        query = df.loc[i]["Cell"]
        limit=1
        type="item"

        if kg_type == KG.Wikidata.value:
            wikidata = WikidataAPI()
            entities = wikidata.getKGEntities(query, limit, type)
            df["KG_Entity"][i] = entities

        elif kg_type == KG.DBpedia.value:
            dbpedia = DBpediaAPI()
            entities = dbpedia.getKGEntities(query, limit, type)
            df["KG_Entity"][i] = entities

    df.to_csv('result.csv')
