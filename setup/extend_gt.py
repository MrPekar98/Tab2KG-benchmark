import sys
import csv
import shutil
import os
import subprocess
from neo4j import GraphDatabase

def query(tx, entity, kg):
    result = tx.run('MATCH (s:Resource)-[p:owl__sameAs]->(o:Resource) WHERE s.uri IN [$entity] RETURN o.uri AS entity', entity = entity)
    return set(filter(lambda x: kg in x.data()['entity'], list(result)))

progress = 0
gt_file = sys.argv[1]
kg = sys.argv[2]
NEO4J_URI = 'bolt://localhost:7687'
NEO4J_AUTH = ('neo4j', 'admin')

file_lines = int(subprocess.check_output('cat ' + gt_file + ' | wc -l', shell = True).strip())

with GraphDatabase.driver(NEO4J_URI, auth = NEO4J_AUTH) as neo4j_driver:
    neo4j_driver.verify_connectivity()

    with neo4j_driver.session(database = 'neo4j') as session:
        with open('temp_gt.csv', 'w') as handle_out:
            writer = csv.writer(handle_out)

            with open(gt_file, 'r') as handle_in:
                reader = csv.reader(handle_in)

                for row in reader:
                    print(' ' * 100, end = '\r')
                    print('Collecting alternative GT entities: ' + str((progress / file_lines) * 100)[:5] + '%', end = '\r')
                    progress += 1

                    gt_entity = row[3]
                    alternative_entities = session.execute_read(query, gt_entity, kg)
                    all_gt_entities = [gt_entity]
                    all_gt_entities.extend([entity.data()['entity'] for entity in alternative_entities])
                    gt_str = ''

                    for entity in all_gt_entities:
                        gt_str += entity + ' '

                    gt_str[:len(gt_str) - 1]
                    writer.writerow([row[0], row[1], row[2], gt_str])

os.remove(gt_file)
shutil.move('temp_gt.csv', gt_file)
