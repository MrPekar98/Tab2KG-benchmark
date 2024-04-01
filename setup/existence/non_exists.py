import sys

gt_file = sys.argv[1]
kg_file = sys.argv[2]
kg_entities = set()
non_existent = set()

with open(kg_file, 'r') as file:
    for line in file:
        entity = line.strip().split('/')[-1]
        kg_entities.add(entity)

with open(gt_file, 'r') as file:
    for line in file:
        entity = line.strip().split('/')[-1]

        if entity not in kg_entities:
            non_existent.add(entity)

for entity in non_existent:
    print(entity)
