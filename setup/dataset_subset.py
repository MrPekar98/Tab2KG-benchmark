import sys
import shutil
import os
import csv

def count_entities(filename):
    entities = set()

    with open(filename, 'r') as file:
        reader = csv.reader(file)

        for row in reader:
            for item in row:
                if not isinstance(item, (int, float)):
                    entities.add(item)

    return len(entities)

subset_factor = float(sys.argv[1])
benchmark_dir = sys.argv[2]
table_dir = benchmark_dir + '/tables/'
output_table_dir = benchmark_dir + 'tables_subset/'
tables = list(os.listdir(table_dir))
num_entities = 0
progress = 0

if not os.path.exists(output_table_dir):
    os.mkdir(output_table_dir)

print('Counting entities...')

for table in tables:
    print(' ' * 100, end = '\r')
    print('Progress: ' + str(int((progress / len(tables)) * 100)) + '%', end = '\r')
    progress += 1
    num_entities += count_entities(table_dir + table)

collected_entities = 0
num_entities *= subset_factor
print('\nConstructing sub-dataset')

for table in tables:
    print(' ' * 100, end = '\r')
    print('Progress: ' + str(int((collected_entities / num_entities) * 100)) + '%', end = '\r')

    collected_entities += count_entities(table_dir + table)

    if collected_entities >= num_entities:
        break

    shutil.copyfile(table_dir + table, output_table_dir + table)

print()
