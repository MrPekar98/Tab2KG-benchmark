from neo4j import GraphDatabase

URI = 'bolt://localhost:7687'
AUTH = ('neo4j', 'admin')

def _query_types(tx, entity, predicate):
    result = tx.run('MATCH (a:Resource)-[l:' + predicate + ']->(b:Resource) WHERE a.uri in [$entity] RETURN b.uri as type', entity = entity)
    return list(result)

def _predicates(tx):
    result = tx.run('CALL db.relationshipTypes() YIELD relationshipType RETURN relationshipType as predicate')
    return list(result)

def type_predicate(kg):
    with GraphDatabase.driver(URI, auth = AUTH) as driver:
        with driver.session(database = 'neo4j') as session:
            preds = session.execute_read(_predicates)

            for predicate in preds:
                pred = predicate.data()['predicate']

                if (kg == 'wikidata' and pred.endswith('P31')) or (kg == 'dbpedia' and 'type' in pred and 'rdf' in pred):
                    return pred

            return None

def entity_types(entity, predicate):
    types = set()

    with GraphDatabase.driver(URI, auth = AUTH) as driver:
        with driver.session(database = 'neo4j') as session:
            results = session.execute_read(_query_types, entity, predicate)

            for type in results:
                types.add(type.data()['type'])

            return types
