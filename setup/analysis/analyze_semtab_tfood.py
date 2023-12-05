# Command: 'python3 analysis.py (load|new)'
# 'load': Show the stats already computed once
# 'new': Re-compute the stats

import os
import sys
import json
import csv
import statistics
from analysis.stats import Stats
import analysis.save_stats as ss
from analysis.plot import plot
import analysis.neo4j_connector as neo4j

def analyze_semtab(orientation):
    base = '/home/benchmarks/semtab/tfood/' + orientation + '/'
    table_dir = base + 'tables/'
    gt_file = base + 'gt/cea_gt.csv'
    files = os.listdir(table_dir)
    stats = Stats()
    rows = 0
    columns = 0
    entity_density = 0
    entities = set()
    type_pred = neo4j.type_predicate('wikidata')

    with open(gt_file, 'r') as fd:
        handle = csv.reader(fd, delimiter = ',')
        table_entities = dict()

        for line in handle:
            table_id = line[0]
            entity = line[3]
            entities.add(entity)

            if table_id not in table_entities.keys():
                table_entities[table_id] = 0

            table_entities[table_id] += 1

        stats.set_num_entities(statistics.mean(table_entities.values()))

    for file in files:
        table_cells = 0
        table_id = file.replace('.csv', '')

        with open(table_dir + file, 'r') as fd:
            handle = csv.reader(fd, delimiter = ',')
            tmp_columns = 0

            for line in handle:
                rows += 1
                tmp_columns = len(line)
                table_cells += len(line)

            rows -= 1
            columns += tmp_columns

            if table_id in table_entities.keys():
                entity_density += float(table_entities[table_id]) / table_cells

    stats.set_tables(len(files))
    stats.set_rows(rows / len(files))
    stats.set_columns(columns / len(files))
    stats.set_entity_density(entity_density / len(files))

    type_distribution = dict()

    for entity in entities:
        types = neo4j.entity_types(entity, type_pred)

        for type in types:
            type = type.split('/')[-1]

            if type not in type_distribution.keys():
                type_distribution[type] = 0

            type_distribution[type] += 1

    stats.set_type_distribution(type_distribution)
    return stats

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Missing argument \'load\' or \'new\'')
        exit(1)

    stats_semtab = None

    if sys.argv[1] == 'load':
        stats_tfood_horizontal = ss.load_stats('/plots/.semtab_tfood_horizontal.stats')
        stats_tfood_entity = ss.load_stats('/plots/.semtab_tfood_entity.stats')

        if stats_tfood_horizontal is None or stats_tfood_entity is None:
            print('Stats could not be loaded. You need to use the \'new\' command.')
            exit(1)

    print('\nAnalyzing SemTab (tFood - Wikidata)...')

    if sys.argv[1] == 'new':
        stats_tfood_horizontal = analyze_semtab('horizontal')
        stats_tfood_entity = analyze_semtab('entity')
        ss.write_stats('/plots/.semtab_tfood_horizontal.stats', stats_tfood_horizontal)
        ss.write_stats('/plots/.semtab_tfood_entity.stats', stats_tfood_entity)

    print('SemTab (tFood horizontal - Wikidata) stats:')
    stats_tfood_horizontal.print()
    plot(stats_tfood_horizontal.type_distribution(), 10, 14, 30, '/plots/SemTab_tFood_horizontal_Wikidata.pdf')

    print('SemTab (tFood entity - Wikidata) stats:')
    stats_tfood_entity.print()
    plot(stats_tfood_entity.type_distribution(), 10, 14, 30, '/plots/SemTab_tFood_entity_Wikidata.pdf')
