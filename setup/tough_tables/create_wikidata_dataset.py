import neo4j_connector as neo4j
import csv

input = '/home/tough_tables/ToughTablesR2-DBP/Test/gt/cea_gt.csv'
gt_file = '/home/setup/tough_tables/ToughTablesR2-WD/gt/cea_gt.csv'
URI = 'bolt://localhost:7687'
AUTH = ('neo4j', 'admin')

def query(tx, entity):
    results = tx.run('MATCH (n1:Resource)-[r:owl__sameAs]->(n2:Resource) WHERE n1.uri IN [$entity] RETURN n2.uri AS uri', entity = entity)
    return list(results)

with open(input, 'r') as input_file:
    reader = csv.reader(input_file, delimiter = ',')

    with open(gt_file, 'w') as file:
        writer = csv.writer(file, delimiter = ',')

        with GraphDatabase.driver(URI, auth = AUTH) as driver:
            with driver.session(database = 'neo4j') as session:
                for line in reader:
                    dbp_entities = line[-1].split(' ')
                    wd_entities = ''

                    for entity in dbp_entities:
                        results = session.execute_read(query, entity)

                        for result in results:
                            wd_entity = result.data()['uri']

                            if 'wikidata' in wd_entity and 'dbpedia' not in wd_entity:
                                wd_entities += wd_entity + ' '

                    wd_entities = wd_entities[0:len(wd_entities) - 1]
                    writer.writerow([line[0], line[1], line[2], wd_entities])
