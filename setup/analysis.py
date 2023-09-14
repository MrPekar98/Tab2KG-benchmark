# Command: 'python3 analysis.py (load|new)'
# 'load': Show the stats already computed once
# 'new': Re-compute the stats

import os
import sys
import json
import csv
import pickle

class Stats:
    def __init__(self):
        self.__rows = 0
        self.__columns = 0
        self.__entities = 0
        self.__entities_in_kg = 0

    def rows(self):
        return self.__rows

    def columns(self):
        return self.__columns

    def entities(self):
        return self.__entities

    def entity_coverage(self):
        return self.__entities_in_kg

    def set_rows(self, rows):
        self.__rows = rows

    def set_columns(self, columns):
        self.__columns = columns

    def set_num_entities(self, num):
        self.__entities = num

    def set_num_covered_entities(self, num):
        self.__entities_in_kg = num

    def print(self):
        print('Avg #rows: ' + str(self.__rows))
        print('Avg #columns: ' + str(self.__columns))
        print('Avg #entities: ' + str(self.__entities))

        if self.__entities > 0:
            print('Avg ground truth entity coverage: ' + str((self.__entities_in_kg / self.__entities) * 100))

        else:
            print('Avg ground truth entity coverage: 0.0%')

def analyze_web_data_commons():
    dir = 'webcommons/tables/'
    gt_dir = 'webcommons/instance/'
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

def analyze_tough_tables(kg):
    kg_dir = ''

    if kg == 'dbpedia':
        kg_dir = 'ToughTablesR2-DBP/'

    else:
        kg_dir = 'ToughTablesR2-WD/'

    dir = 'tough_tables/' + kg_dir + 'Test/tables/'
    files = os.listdir(dir)
    rows = 0
    columns = 0
    entities = 0
    entity_map = dict()
    stats = Stats()

    for file in files:
        with open(dir + file, 'r') as fd:
            handle = csv.reader(fd)
            tmp_columns = 0

            for line in handle:
                rows += 1
                tmp_columns = len(line)

            columns += tmp_columns

    stats.set_rows(rows / len(files))
    stats.set_columns(columns / len(files))

    gt_file = 'tough_tables/' + kg_dir + 'Test/gt/cea_gt.csv'

    with open(gt_file, 'r') as fd:
        handle = csv.reader(fd)

        for line in handle:
            table = line[0]

            if table not in entity_map.keys():
                entity_map[table] = 1

            else:
                entity_map[table] += 1

    for table in entity_map.keys():
        entities += entity_map[table]

    stats.set_num_entities(entities / len(entity_map.keys()))
    return stats

def analyze_semtab():
    dir = 'semtab/DataSets/Test/tables/'
    files = os.listdir(dir)
    stats = Stats()
    rows = 0
    columns = 0

    for file in files:
        with open(dir + file, 'r') as fd:
            handle = csv.reader(fd)
            tmp_columns = 0

            for line in handle:
                rows += 1
                tmp_columns = len(line)

            columns += tmp_columns

    stats.set_rows(rows / len(files))
    stats.set_columns(columns / len(files))

    return stats

def analyze_wikitables(version, kg):
    stats = Stats()
    rows = 0
    columns = 0
    entities = 0
    dir = '../benchmarks/' + kg + '/wikitables_' + str(version) + '/'
    table_files = os.listdir(dir)

    for table_file in table_files:
        with open(dir + table_file, 'r') as file:
            table = json.load(file)['table']
            rows += len(table)

            if len(table) > 0:
                columns = len(table[0])

        for row in table_file:
            for column in row:
                if len(column['entity']) > 0:
                    entities += 1

    stats.set_rows(rows / len(table_files))
    stats.set_columns(columns / len(table_files))
    stats.set_num_entities(entities / len(table_files))

    return stats

# Returns array of Stats instances, one for each benchmark
# 1: WebDataCommons
# 2: ToughTables - DBpedia
# 3: ToughTables - Wikidata
# 4: SemTab
# 5: Wikitables 2013 - DBpedia
# 6: Wikitables 2019 - DBpedia
# 7: Wikitables 2013 - Wikidata
# 8: Wikitables 2019 - Wikidata
def load_stats():
    stats = list()

    with open('.WebDataCommons.stats', 'rb') as file:
        webcommons = pickle.load(file)
        stats.append(webcommons)

    with open('.ToughTables_DBpedia.stats', 'rb') as file:
        tt = pickle.load(file)
        stats.append(tt)

    with open('.ToughTables_Wikidata.stats', 'rb') as file:
        tt = pickle.load(file)
        stats.append(tt)

    with open('.SemTab.stats', 'rb') as file:
        semtab = pickle.load(file)
        stats.append(semtab)

    with open('.Wikitables2013_DBpedia.stats', 'rb') as file:
        wiki = pickle.load(file)
        stats.append(wiki)

    with open('.Wikitables2019_DBpedia.stats', 'rb') as file:
        wiki = pickle.load(file)
        stats.append(wiki)

    with open('.Wikitables2013_Wikidata.stats', 'rb') as file:
        wiki = pickle.load(file)
        stats.append(wiki)

    with open('.Wikitables2019_Wikidata.stats', 'rb') as file:
        wiki = pickle.load(file)
        stats.append(wiki)

    return stats

def write_stats(filename, stats):
    with open(filename, 'wb') as file:
        pickle.dump(stats, file, pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Missing argument \'load\' or \'new\'')
        exit(1)

    all_stats = None
    stats_web_data_commons = None
    stats_tough_tables_dbpedia = None
    stats_tough_tables_wikidata = None
    stats_semtab = None
    stats_wikitables_dbpedia_2013 = None
    stats_wikitables_dbpedia_2019 = None
    stats_wikitables_wikidata_2013 = None
    stats_wikitables_wikidata_2019 = None

    if sys.argv[1] == 'load':
        all_stats = load_stats()

        if all_stats is None:
            print('No stats have been loaded. You need to use the \'new\' command.')
            exit(1)

        stats_web_data_commons = all_stats[0]
        stats_tough_tables_dbpedia = all_stats[1]
        stats_tough_tables_wikidata = all_stats[2]
        stats_semtab = all_stats = all_stats[3]
        stats_wikitables_dbpedia_2013 = all_stats[4]
        stats_wikitables_dbpedia_2019 = all_stats[5]
        stats_wikitables_wikidata_2013 = all_stats[6]
        stats_wikitables_wikidata_2019 = all_stats[7]

    print('Analyzing WebDataCommons...')

    if sys.argv[1] == 'new':
        stats_web_data_commons = analyze_web_data_commons()
        write_stats('.WebDataCommons.stats', stats_web_data_commons)

    print('WebDataCommons stats:')
    stats_web_data_commons.print()

    print('\nAnalyzing ToughTables...')

    if sys.argv[1] == 'new':
        stats_tough_tables_dbpedia = analyze_tough_tables('dbpedia')
        stats_tough_tables_wikidata = analyze_tough_tables('wikidata')
        write_stats('.ToughTables_DBpedia.stats', stats_tough_tables_dbpedia)
        write_stats('.ToughTables_Wikidata.stats', stats_tough_tables_wikidata)

    print('Tough Tables DBpedia stats:')
    stats_tough_tables_dbpedia.print()
    print('\nTough Tables Wikidata stats:')
    stats_tough_tables_wikidata.print()

    print('\nAnalyzing SemTab...')

    if sys.argv[1] == 'new':
        stats_semtab = analyze_semtab()
        write_stats('.SemTab.stats', stats_semtab)

    print('SemTab stats:')
    stats_semtab.print()

    print('\nAnalyzing Wikitables...')

    if sys.argv[1] == 'new':
        stats_wikitables_dbpedia_2013 = analyze_wikitables(2013, 'dbpedia')
        stats_wikitables_dbpedia_2019 = analyze_wikitables(2019, 'dbpedia')
        stats_wikitables_wikidata_2013 = analyze_wikitables(2013, 'wikidata')
        stats_wikitables_Wikidata_2019 = analyze_wikitables(2019, 'wikidata')
        write_stats('.Wikitables2013_DBpedia.stats', stats_wikitables_dbpedia_2013)
        write_stats('.Wikitables2019_DBpedia.stats', stats_wikitables_dbpedia_2019)
        write_stats('.Wikitables2013_Wikidata.stats', stats_wikitables_wikidata_2013)
        write_stats('.Wikitables2019_Wikidata.stats', stats_wikitables_Wikidata_2019)

    print('Wikitables 2013 stats (DBpedia):')
    stats_wikitables_dbpedia_2013.print()
    print('\nWikitables 2019 stats (DBpedia):')
    stats_wikitables_dbpedia_2019.print()
    print('Wikitables 2013 stats (Wikidata):')
    stats_wikitables_wikidata_2013.print()
    print('Wikitables 2019 stats (Wikidata):')
    stats_wikitables_Wikidata_2019.print()
