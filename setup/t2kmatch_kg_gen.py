import os
import sys
import csv

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Missing arguments')
        exit(0)

    kg_dir = sys.argv[1]
    output_dir = sys.argv[2]
    kg = sys.argv[3]
    files = os.listdir(kg_dir)
    entities = dict()
    predicate_types = dict()
    labels = dict()
    classes = dict()
    entity_substr = ''

    if kg == 'dbpedia':
        entity_substr = 'resource'

    elif kg == 'wikidata':
        entity_substr = '/Q'

    else:
        print('KG \'' + kg + '\' was not recognized')
        exit(1)

    if not kg_dir.endswith('/'):
        kg_dir += '/'

    if not output_dir.endswith('/'):
        output_dir += '/'

    print('Indexing KG...')

    for file in files:
        with open(kg_dir + file, 'r') as input_fd:
            for line in input_fd:
                triple = line.split(' ')
                subject = triple[0].replace('<', '').replace('>', '')
                predicate = triple[1].replace('<', '').replace('>', '')
                object = triple[2].replace('<', '').replace('>', '')

                if entity_substr in subject:
                    if subject not in entities.keys():
                        entities[subject] = set()

                    entities[subject].add((predicate, object))

                if 'rdf-schema#label' in predicate:
                    labels[subject] = object.split('@')[0]

                if '^^' in object:
                    predicate_types[predicate] = object.split('^^')[1]

                if '#range' in predicate and 'ontology' in subject:
                    predicate_types[subject] = object

                if '#type' in predicate and 'ontology' in object:
                    if object not in classes.keys():
                        classes[object] = set()

                    classes[object].add(subject)

    print('Done indexing KG\nWriting KG...')

    for class_name in classes.keys():
        header_predicate_postfix = ['URI', 'rdf-schema#label']
        header_predicate_full = ['URI', 'http://www.w3.org/2000/01/rdf-schema#label']
        header_predicate_type_postfix = ['URI', 'rdf-schema#Literal']
        header_predicate_type_full = ['http://www.w3.org/2002/07/owl#Thing', 'http://www.w3.org/2000/01/rdf-schema#Literal']

        with open(output_dir + class_name.split('/')[-1] + '.csv', 'w') as output_fd:
            writer = csv.writer(output_fd, delimiter = ',')
            ents = classes[class_name]

            for entity in ents:
                if entity in entities.keys():
                    for predicate_object in entities[entity]:
                        if predicate_object[0] not in header_predicate_full and predicate_object[0] in predicate_types.keys():
                            header_predicate_type_full.append(predicate_types[predicate_object[0]])
                            header_predicate_type_postfix.append(predicate_types[predicate_object[0]].split('/')[-1])
                            header_predicate_full.append(predicate_object[0])
                            header_predicate_postfix.append(predicate_object[0].split('/')[-1])

            writer.writerow(header_predicate_postfix)
            writer.writerow(header_predicate_full)
            writer.writerow(header_predicate_type_postfix)
            writer.writerow(header_predicate_type_full)

            for entity in ents:
                row = [entity]

                if entity in labels:
                    row.append(labels[entity])

                else:
                    row.append('NULL')

                if entity in entities.keys():
                    for i in range(len(header_predicate_full)):
                        found = False

                        for predicate_object in entities[entity]:
                            if predicate_object[0] == header_predicate_full[i]:
                                found = True
                                row.append(predicate_object[1])

                        if not found:
                            row.append('NULL')

                    writer.writerow(row)

    print('Done writing KG')
