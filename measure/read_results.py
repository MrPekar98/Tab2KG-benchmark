import csv
import os
import sys

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

# Read candidate generation results of EmbLookup
def read_emblookup_candidates(file_path, kg):
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
            prefix = 'http://dbpedia.org/resource/'

            if kg == 'wikidata':
                prefix = 'http://www.wikidata.org/entity/'

            elif kg != 'dbpedia':
                raise Exception('KG not recognized')

            candidates = [(prefix + entity.replace('"', '').replace('<', '').replace('>', '').lower()) for entity in parsed_row[3].split(' ')]
            tuple.append(candidates)
            results.append(tuple)

        return results

# Results of bbw
def read_bbw(files_dir):
    results = list()
    files = os.listdir(files_dir)

    for file in files:
        if 'runtime' in file:
            continue

        with open(files_dir + '/' + file, 'r') as input:
            reader = csv.reader(input)
            header_skipped = False

            for row in reader:
                if not header_skipped:
                    header_skipped = True
                    continue

                tuple = [file.replace('.csv', ''), int(row[2]), int(row[3]), row[4].lower()]
                results.append(tuple)

    return results

# Candidate generation results of bbw
def read_bbw_candidates(files_dir):
    results = list()
    files = os.listdir(files_dir)

    for file in files:
        with open(files_dir + '/' + file, 'r') as input:
            csv.field_size_limit(sys.maxsize)
            reader = csv.reader(input)
            header_skipped = False

            for row in reader:
                if not header_skipped:
                    header_skipped = True
                    continue

                tuple = [file.replace('.csv', ''), int(row[0]), int(row[1]), [entity.lower() for entity in row[2].split(' ')]]
                results.append(tuple)

    return results

# Results of keyword-kg-linker
def read_keyword_kg_linker(files_dir):
    results = list()
    files = os.listdir(files_dir)

    for file in files:
        with open(files_dir + file, 'r', encoding = 'ISO-8859-1') as input:
            reader = csv.reader(input)
            header_skipped = False
            row_count = 1
            file_id = file.replace('.csv', '')

            for row in reader:
                if not header_skipped:
                    header_skipped = True
                    continue

                column_count = 0

                for column in row:
                    tuple = [file_id, row_count, column_count, column]
                    results.append(tuple)
                    column_count += 1

                row_count += 1

    return results

# Results key-kg-linker candidate generation
def read_keyword_kg_linker_candidates(files_dir):
    results = read_keyword_kg_linker(files_dir)
    copy = list()

    for result in results:
        tuple = [result[0], result[1], result[2], [entity for entity in result[3].split('#')]]
        copy.append(tuple)

    return copy

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

# Results of LexMa candidate generation
def read_lexma_candidates(result_files_dir):
    results = list()
    files = os.listdir(result_files_dir)

    for result_file in files:
        with open(result_files_dir + result_file, 'r') as input:
            reader = csv.reader(input)

            for row in reader:
                tuple = [result_file.replace('.csv', ''), int(row[0]) + 1, int(row[1]), [entity.lower() for entity in row[2].split(' ')]]
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

# Results of MAGIC candidate generation
def read_magic_candidates(result_file_dir):
    results = list()
    files = os.listdir(result_file_dir)

    for result_file in files:
        with open(result_file_dir + result_file, 'r') as input:
            reader = csv.reader(input)

            for row in reader:
                tuple = [row[0], int(row[1]) + 1, int(row[2]) + 1, [entity.lower() for entity in row[3].split(' ')]]
                results.append(tuple)

    return results

# Results of CitySTI
def read_citysti(result_file):
    results = list()

    with open(result_file, 'r') as handle:
        reader = csv.reader(handle)

        for row in reader:
            tuple = [row[0], int(row[1]), int(row[2]), row[3].lower()]
            results.append(tuple)

    return results

def read_citysti_candidates(result_file):
    results = list()

    with open(result_file, 'r') as handle:
        reader = csv.reader(handle)

        for row in reader:
            tuple = [row[0], int(row[1]), int(row[2]), [entity.lower() for entity in row[3].split('#')]]
            results.append(tuple)

    return results
