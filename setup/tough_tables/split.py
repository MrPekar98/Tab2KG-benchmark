base = '/home/tough_tables/'
filename = base + 'wikidata/wikidata.nt'
line_counter = 1
entities = set()

with open(filename, 'r') as input:
    for line in input:
        split = line.split(' ')
        subject = split[0]
        predicate = split[1]
        object = split[2]
        pred_type = predicate.split('/')[-1].replace('>', '')
        entities.add(subject)

        with open(base + 'wikidata/' + pred_type + '.ttl', 'a') as output:
            output.write(line)

        print(' ' * 100, end = '\r')
        print('Line', line_counter, end = '\r')
        line_counter += 1

with open(base + 'wikidata/entities.ttl', 'w') as entity_file:
    for entity in entities:
        entity_file.write(entity + ' <http://xmlns.com/foaf/0.1/name> "null" .\n')
