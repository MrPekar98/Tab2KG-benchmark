# Command: 'python3 analysis.py (load|new)'
# 'load': Show the stats already computed once
# 'new': Re-compute the stats

import os
import sys
import json
import csv
import pickle
from stats import Stats

def analyze_web_data_commons():
    dir = '../webcommons/tables/'
    gt_dir = '../webcommons/instance/'
    table_files = os.listdir(dir)
    gt_files = os.listdir(gt_dir)
    stats = Stats()
    rows = 0
    columns = 0
    entities = 0
    entity_list = list()

    for table_file in table_files:
        try:
            with open(dir + table_file, 'r') as file:
                obj = json.load(file)
                table = obj['relation']
                rows += len(table[0]) - 1
                columns += len(table)

                if table_file.replace('json', 'csv') in gt_files:
                    with open(gt_dir + table_file.replace('json', 'csv'), 'r') as gt_file:
                        gt_map = dict()
                        row_index = 0
                        handle = csv.reader(gt_file)

                        for line in handle:
                            entity = line[0]
                            index = int(line[2])
                            gt_map[index] = entity

                        for row_val in table[obj['keyColumnIndex']]:
                            if row_index in gt_map.keys():
                                entities += 1
                                entity_list.append(gt_map[row_index])

                            row_index += 1

        except UnicodeDecodeError as e:
            continue

    stats.set_rows(rows / len(table_files))
    stats.set_columns(columns / len(table_files))
    stats.set_num_entities(entities / len(table_files))

    return stats

# Returns stats
def load_stats():
    with open('.WebDataCommons.stats', 'rb') as file:
        webcommons = pickle.load(file)
        return webcommons

def write_stats(filename, stats):
    with open(filename, 'wb') as file:
        pickle.dump(stats, file, pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Missing argument \'load\' or \'new\'')
        exit(1)

    stats_web_data_commons = None

    if sys.argv[1] == 'load':
        stats_web_data_commons = load_stats()

        if all_stats is None:
            print('No stats have been loaded. You need to use the \'new\' command.')
            exit(1)

    print('Analyzing WebDataCommons...')

    if sys.argv[1] == 'new':
        stats_web_data_commons = analyze_web_data_commons()
        write_stats('.WebDataCommons.stats', stats_web_data_commons)

    print('WebDataCommons stats:')
    stats_web_data_commons.print()
