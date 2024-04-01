from SPARQLWrapper import SPARQLWrapper, JSON
import sys

entity = sys.argv[1]
graph = sys.argv[2]
url = sys.argv[3]
sparql = SPARQLWrapper(url.replace(' ', ''))
sparql.setReturnFormat(JSON)
query = 'ASK { GRAPH <' + graph + '> { <' + entity + '> ?p ?o } }'

try:
    sparql.setQuery(query)
    exists = sparql.query().convert()['boolean']
    print(exists)

except Exception as e:
    print('Exception: ' + str(e))
