import csv

BASE = '../results/'
BBW = BASE + 'bbw/'
EMBLOOKUP = BASE + 'emblookup/'
KEYWORD_KG_LINKER = BASE + 'keyword-kg-linker/'
LEXMA = BASE + 'lexma/'
MAGIC = BASE + 'magic/'

BENCHMARKS_BASE = '../benchmarks/'
SEMTAB_HARDTABLES_GT = BENCHMARKS_BASE + 'semtab/HardTables/gt/cea_gt.csv'
SEMTAB_TFOOD_GT = BENCHMARKS_BASE + 'semtab/tfood/horizontal/gt/cea_gt.csv'
TOUGH_TABLES_DBPEDIA_GT = BENCHMARKS_BASE + 'toughtables/dbpedia/gt/cea_gt.csv'
TOUGH_TABLES_WIKIDATA_GT = BENCHMARKS_BASE + 'toughtables/wikidata/gt/cea_gt.csv'
WIKITABLES_2013_DBPEDIA_GT = BENCHMARKS_BASE + 'wikitables_2013/gt/dbpedia/gt.csv'
WIKITABLES_2013_WIKIDATA_GT = BENCHMARKS_BASE + 'wikitables_2013/gt/wikidata/gt.csv'
WIKITABLES_2019_DBPEDIA_GT = BENCHMARKS_BASE + 'wikitables_2019/gt/dbpedia/gt.csv'
WIKITABLES_2019_WIKIDATA_GT = BENCHMARKS_BASE + 'wikitables_2019/gt/wikidata/gt.csv'

# Ground truth output is given in a similar format as the results of each approach
# It's a map from table ID to tuples on the following format:
#     [ROW_ID, COLUMN_ID, LINK]
#
# However, LINKS can consist of multiple ground truth entities
# Hence, the ground truth list consists of tuples of *at least* 4 elements
def ground_truth(gt_path):
    gt = dict()

    with open(gt_path, 'r') as gt_file:
        reader = csv.reader(gt_file)

        for row in reader:
            table_id = row[0]
            tuple = [int(row[1]), int(row[2])]

            if table_id not in gt.keys():
                gt[table_id] = list()

            if gt_path in (TOUGH_TABLES_DBPEDIA_GT, TOUGH_TABLES_WIKIDATA_GT):
                tuple.extend(entity.lower() for entity in row[3].split(' '))

            else:
                tuple.append(row[3].lower())

            if gt_path in (WIKITABLES_2013_DBPEDIA_GT, WIKITABLES_2013_WIKIDATA_GT, WIKITABLES_2019_DBPEDIA_GT, WIKITABLES_2019_WIKIDATA_GT):
                tuple[0] += 1

            gt[table_id].append(tuple)

    return gt
