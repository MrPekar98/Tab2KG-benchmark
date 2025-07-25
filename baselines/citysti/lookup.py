import json
from pprint import pprint
import time
from urllib import parse, request
from entity import KGEntity
import os

class Lookup(object):
    '''
    classdocs
    '''
    def __init__(self, lookup_url):
        self.service_url = lookup_url

    def getJSONRequest(self, params):
        try:
            #urllib has been split up in Python 3.
            #The urllib.urlencode() function is now urllib.parse.urlencode(),
            #and the urllib.urlopen() function is now urllib.request.urlopen().
            #url = service_url + '?' + urllib.urlencode(params)
            #url = self.service_url + '?' + parse.urlencode(params)
            url = self.service_url + '?query=' + params['query'] + '&k=' + str(params['k']) + '&format=' + params['format'] + '&fuzzy=' + params['fuzzy']
            #print(url)
            #response = json.loads(urllib.urlopen(url).read())

            req = request.Request(url)
            #Customize headers. For example dbpedia lookup returns xml by default
            req.add_header('Accept', 'application/json')

            #print(request.urlopen(req).read())
            response = json.loads(request.urlopen(req).read())

            return response

        except:
            print("Lookup '%s' failed.")

'''
DBpedia lookup access
'''
class DBpediaLookup(Lookup):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        super().__init__(self.getURL())

    def getURL(self):
        #OLD lookup: https://github.com/dbpedia/lookup
        #return "http://lookup.dbpedia.org/api/search/KeywordSearch"

        #NEW lookup: https://github.com/dbpedia/lookup-application
        #return "http://akswnc7.informatik.uni-leipzig.de/lookup/api/search"
        return "http://" + os.getenv("ENDPOINT") + ":7000/search"

        #TODO: prefix search allows for partial searches
        #return "http://lookup.dbpedia.org/api/search/PrefixSearch"

    def __createParams(self, query, limit, query_cls=''):
        params = {
            'query': query.replace(' ', '%20'),
            'k': limit,
            'format': 'json',
            'fuzzy': 'true'
        }

        return params

    def getKGName(self):
        return 'DBpedia'

    '''
    Returns list of ordered entities according to relevance: dbpedia
    '''
    def __extractKGEntities(self, json, filter=''):
        entities = list()

        for element in json['output']:
            types = set()

            if 'type' in element:
                for t in element['type']:
                    if t != 'http://www.w3.org/2002/07/owl#Thing':
                        if t.startswith('http://dbpedia.org/ontology/') or t.startswith('http://www.wikidata.org/entity/') or t.startswith('http://schema.org/'): 
                            types.add(t)

            description=''
            if 'description' in element:
                description = element['description']

            ##Expected only one
            uri=''
            if 'entity' in element:
                uri = element['entity']

            ##Expected only one
            label=''
            if 'label' in element:
                label = element['label']

            kg_entity = KGEntity(
                uri,
                label,
                description,
                types,
                self.getKGName()
                )

            #We filter according to given URI
            if filter=='' or uri==filter:
                entities.append(kg_entity)
            #print(kg_entity)

        #for entity in entities:
        #    print(entity)
        return entities

    def getKGEntities(self, query, limit, filter=''):
        json = self.getJSONRequest(self.__createParams(query, limit))

        if json==None:
            print("None results for", query)
            return list()

        return self.__extractKGEntities(json, filter) #Optionally filter by URI

'''
Wikidata web search API
'''
class WikidataAPI(Lookup):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        super().__init__(self.getURL())

    def getURL(self):
        return "http://" + os.getenv("ENDPOINT") + ":7000/search"

    def __createParams(self, query, limit, type='item'):
        params = {
            'format' : 'json',
            'query': query.replace(' ', '%20'),
            'k': limit,
            'fuzzy' : 'true'
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

            kg_entity = KGEntity(
                element['entity'],
                element['label'],
                description,
                types,
                self.getKGName()
                )

            #We filter according to givem URI
            if filter=='' or element['concepturi']==filter:
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

'''
Entity search for Google KG
'''
class GoogleKGLookup(Lookup):
    def __init__(self):
        '''
        Constructor
        '''
        super().__init__(self.getURL())
        self.api_key = 'AIzaSyA6Bf9yuMCCPh7vpElzrfBvE2ENCVWr-84'
        #open('.api_key').read()

    #def getAPIKey(self):
    #    return self.api_key

    def getURL(self):
        return 'https://kgsearch.googleapis.com/v1/entities:search'

    def __createParams(self, query, limit):
        params = {
            'query': query,
            'limit': limit,
            'indent': True,
            'key': self.api_key,
        }

        return params

    def getKGName(self):
        return 'GoogleKG'

    '''
    Returns list of ordered entities according to relevance: google
    '''
    def __extractKGEntities(self, json, filter=''):
        entities = list()

        for element in json['itemListElement']:
            types = set()

            for t in element['result']:
                if t != 'Thing':
                    types.add("http://schema.org/"+t)

            description=''
            if 'description' in  element['result']:
                description = element['result']['description']

            kg_entity = KGEntity(
                element['result']['@id'],
                element['result']['name'],
                description,
                types,
                self.getKGName()
                )

            #We filter according to givem URI
            if filter=='' or element['result']['@id']==filter:
                entities.append(kg_entity)
            #print(kg_entity)

        #for entity in entities:
        #    print(entity)
        return entities

    def getKGEntities(self, query, limit, filter=''):
        json = self.getJSONRequest(self.__createParams(query, limit))

        if json==None:
            print("None results for", query)
            return list()

        return self.__extractKGEntities(json, filter) #Optionally filter by URI

if __name__ == '__main__':
    #query="Chicago Bulls"
    #query="Congo"
    query="United Kingdom"

    #Max entities to be returned matching the keyword query
    limit=5

    print("Entities matching the keyword: " + query)
    print("Entities from Google KG:")
    kg = GoogleKGLookup()
    entities = kg.getKGEntities(query, limit)
    for ent in  entities:
        print(ent)

    print("\n")

    dbpedia = DBpediaLookup()
    entities = dbpedia.getKGEntities(query, limit)
    print("Entities from DBPedia:")
    for ent in  entities:
        print(ent)

    print("\n")

    type="item"
    #type="property"
    wikidata = WikidataAPI()
    entities = wikidata.getKGEntities(query, limit, type)
    print("Entities from Wikidata:")
    for ent in  entities:
        print(ent)
