import csv
import os

# Following functions return a list of tuples with results
# Each tuple is organized as follows:
#     [TABLE_ID, ROW_ID, COLUMN_ID, LINK]
#
# TABLE_ID: Identifier of table
# ROW_ID: Index of row
# COLUMN_ID: Index of column
# LINK: Entity link for entity mention in the position given by ROW_ID and COLUMN_ID

# Results of EmbLookup
def read_emblookup(file_path, kg):
    with open(file_path, 'r') as input:
        reader = csv.reader(input)
        results = list()

        for row in reader:
            parsed_row = None

            if len(row) == 1:
                parsed_row = row[0].split(',')
                parsed_row[1] = int(parsed_row[1])
                parsed_row[2] = int(parsed_row[2])

            else:
                parsed_row = row

            tuple = [parsed_row[0], int(parsed_row[1]) + 1, int(parsed_row[2])]
            entity = parsed_row[3].replace('"', '').replace('<', '').replace('>', '').lower()

            if kg == 'dbpedia':
                entity = 'http://dbpedia.org/resource/' + entity

            elif kg == 'wikidata':
                entity = 'http://www.wikidata.org/entity/' + entity

            else:
                raise Exception('KG not recognized')

            tuple.append(entity)
            results.append(tuple)

        return results

# Results of bbw
def read_bbw(files_dir):
    results = list()
    files = os.listdir(files_dir)

    for file in files:
        with open(files_dir + '/' + file, 'r') as input:
            reader = csv.reader(input)
            header_skipped = False

            for row in reader:
                if not header_skipped:
                    header_skipped = True
                    continue

                tuple = [file.replace('.csv', ''), int(row[1]), int(row[2]), row[3].lower()]
                results.append(tuple)

    return results

# Results of keyword-kg-linker
def read_keyword_kg_linker():
    pass

# Results of LexMa
def read_lexma(result_files_dir):
    results = list()
    files = os.listdir(result_files_dir)

    for result_file in files:
        if 'runtime' in result_file:
            continue

        with open(result_files_dir + result_file, 'r') as input:
            reader = csv.reader(input)

            for row in reader:
                tuple = [result_file.replace('.csv', ''), int(row[0]) + 1, int(row[1]), row[2].lower()]
                results.append(tuple)

    return results

# Results of MAGIC
def read_magic(result_files_dir):
    results = list()
    files = os.listdir(result_files_dir)

    for result_file in files:
        if not 'cea' in result_file:
            continue

        with open(result_files_dir + result_file, 'r') as input:
            reader = csv.reader(input)

            for row in reader:
                tuple = [row[0], int(row[1]) + 1, int(row[2]), row[3].lower()]
                results.append(tuple)

    return results
