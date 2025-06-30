import pandas as pd
import os
import csv

BASE = '/results/'
BBW = BASE + 'bbw/'
EMBLOOKUP = BASE + 'emblookup/'
KEYWORD_KG_LINKER = BASE + 'keyword-kg-linker/'
LEXMA = BASE + 'lexma/'
MAGIC = BASE + 'magic/'
CITYSTI = BASE + 'citysti/'
NAIVE = BASE + 'keyword-kg-linker/'

BENCHMARKS_BASE = '/benchmarks/'
SEMTAB_HARDTABLES = BENCHMARKS_BASE + 'semtab/HardTables/tables/'
SEMTAB_TFOOD = BENCHMARKS_BASE + 'semtab/tfood/horizontal/tables/'
TOUGH_TABLES_DBPEDIA = BENCHMARKS_BASE + 'toughtables/dbpedia/tables/'
TOUGH_TABLES_WIKIDATA = BENCHMARKS_BASE + 'toughtables/wikidata/tables/'
WIKITABLES_2013 = BENCHMARKS_BASE + 'wikitables_2013/tables/'
WIKITABLES_2019 = BENCHMARKS_BASE + 'wikitables_2019/tables/'
SEMTAB_HARDTABLES_GT = BENCHMARKS_BASE + 'semtab/HardTables/gt/cea_gt.csv'
SEMTAB_TFOOD_GT = BENCHMARKS_BASE + 'semtab/tfood/horizontal/gt/cea_gt.csv'
TOUGH_TABLES_DBPEDIA_GT = BENCHMARKS_BASE + 'toughtables/dbpedia/gt/cea_gt.csv'
TOUGH_TABLES_WIKIDATA_GT = BENCHMARKS_BASE + 'toughtables/wikidata/gt/cea_gt.csv'
WIKITABLES_2013_DBPEDIA_GT = BENCHMARKS_BASE + 'wikitables_2013/gt/dbpedia/gt.csv'
WIKITABLES_2013_WIKIDATA_GT = BENCHMARKS_BASE + 'wikitables_2013/gt/wikidata/gt.csv'
WIKITABLES_2019_DBPEDIA_GT = BENCHMARKS_BASE + 'wikitables_2019/gt/dbpedia/gt.csv'
WIKITABLES_2019_WIKIDATA_GT = BENCHMARKS_BASE + 'wikitables_2019/gt/wikidata/gt.csv'
TOUGH_TABLES_WIKIDATA_ENTITY_CELLS = BENCHMARKS_BASE + 'toughtables/wikidata/gt/entity_cells.txt'
WIKITABLES_2019_WIKIDATA_ENTITY_CELLS = BENCHMARKS_BASE + 'wikitables_2019/gt/wikidata/entity_cells.txt'

# Ground truth output is given in a similar format as the results of each approach
# It's a map from table ID to tuples on the following format:
#     [ROW_ID, COLUMN_ID, LINK]
#
# However, LINKS can consist of multiple ground truth entities
# Hence, the ground truth list consists of tuples of *at least* 4 elements
def ground_truth(gt_path):
    gt = dict()
    df = pd.read_csv(gt_path)

    for i, row in df.iterrows():
        table_id = row[0]
        tuple = [int(row[1]), int(row[2])]

        if table_id not in gt.keys():
            gt[table_id] = list()

        tuple.extend(entity.lower() for entity in row[3].split(' '))

        if gt_path in (WIKITABLES_2013_DBPEDIA_GT, WIKITABLES_2013_WIKIDATA_GT, WIKITABLES_2019_DBPEDIA_GT, WIKITABLES_2019_WIKIDATA_GT):
            tuple[0] += 1

        elif gt_path in SEMTAB_TFOOD:
            gt_row = int(row[2])
            gt_column = int(row[1])
            tuple[0] = gt_row
            tuple[1] = gt_column

        gt[table_id].append(tuple)

    return gt

def avg_rows(dir):
    files = os.listdir(dir)
    count = 0

    for file in files:
        with open(dir + '/' + file) as handle:
            reader = csv.reader(handle)

            for row in reader:
                count += 1

    return count / len(files)

def entity_cells(file):
    cells = dict()

    with open(file, 'r') as handle:
        for line in handle:
            split = line.strip().split(',')
            id = split[0]

            if not id in cells.keys():
                cells[id] = list()

            row = int(split[1])
            column = int(split[2])
            cells[id].append((row, column))

    return cells
