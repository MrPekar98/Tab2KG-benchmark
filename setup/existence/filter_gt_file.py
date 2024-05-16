import csv
import sys
import os

entity_file = sys.argv[1]
gt_file = sys.argv[2]
is_toughtables = 'toughtables' in entity_file
entities = set()

with open(entity_file, 'r') as file:
    for line in file:
        entities.add(line.strip())

with open(gt_file, 'r') as in_file:
    with open(gt_file.replace('.csv', '_new.csv'), 'w') as out_file:
        reader = csv.reader(in_file)
        writer = csv.writer(out_file)

        for row in reader:
            entity_list = ''
            row_entities = row[3].split(' ')

            for entity in row_entities:
                if entity.split('/')[-1] in entities:
                    entity_list += entity + ' '

            if len(entity_list) > 0:
                entity_list = entity_list[:-1]
                writer.writerow[row[0], row[1], row[2], entity_list]

os.remove(gt_file)
os.rename(gt_file.replace('.csv', '_new.csv'), gt_file)
