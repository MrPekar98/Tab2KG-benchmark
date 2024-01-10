import csv
from data import *
import read_results as rr
from quality import evaluate_quality

print('Reading experiment results...')

#bbw_hardtables = rr.read_bbw(BBW + 'semtab_hardtables')
#bbw_tfood = rr.read_bbw(BBW + 'tfood')
#bbw_toughtables = rr.read_bbw(BBW + 'toughtables_wd')
#bbw_wikitables_2013 = rr.read_bbw(BBW + 'wikitables_2013')
#bbw_wikitables_2019 = rr.read_bbw(BBW + 'wikitables_2019')

#emblookup_hardtables = rr.read_emblookup(EMBLOOKUP + 'semtab_hardtables/results.csv', 'wikidata')
#emblookup_tfood = rr.read_read_emblookup(EMBLOOKUP + 'tfood/results.csv', 'wikidata')
emblookup_toughtables_dbp = rr.read_emblookup(EMBLOOKUP + 'toughtables_dbp/results.csv', 'dbpedia')
#emblookup_toughtables_wd = rr.read_emblookup(EMBLOOKUP + 'toughtables_wd/results.csv', 'wikidata')
#emblookup_wikitables_2013_dbp = rr.read_emblookup(EMBLOOKUP + 'wikitables_2013_dbp/results.csv', 'dbpedia')
#emblookup_wikitables_2013_wd = rr.read_emblookup(EMBLOOKUP + 'wikitables_2013_wd/results.csv', 'wikidata')
#emblookup_wikitables_2019_dbp = rr.read_emblookup(EMBLOOKUP + 'wikitables_2019_dbp/results.csv', 'dbpedia')
#emblookup_wikitables_2019_wd = rr.read_emblookup(EMBLOOKUP + 'wikitables_2019_wd/results.csv', 'wikidata')

#lexma_hardtables = rr.read_lexma(LEXMA + 'hardtables/output.csv')
#lexma_tfood = rr.read_lexma(LEXMA + 'tfood/output.csv')
lexma_toughtables_dbp = rr.read_lexma(LEXMA + 'toughtables_dbp/output.csv')
#lexma_toughtables_wd = rr.read_lexma(LEXMA + 'toughtables_wd/output.csv')
#lexma_wikitables_2013_dbp = rr.read_lexma(LEXMA + 'wikitables_2013_dbp/output.csv')
#lexma_wikitables_2013_wd = rr.read_lexma(LEXMA + 'wikitables_2013_wd/output.csv')
#lexma_wikitables_2019_dbp = rr.read_lexma(LEXMA + 'wikitables_2019_dbp/output.csv')
#lexma_wikitables_2019_wd = rr.read_lexma(LEXMA + 'wikitables_2019_wd/output.csv')

print('Reading ground truth...')

#hardtables_gt = ground_truth(SEMTAB_HARDTABLES_GT)
#tfood_gt = ground_truth(SEMTAB_TFOOD_GT)
toughtables_dbp = ground_truth(TOUGH_TABLES_DBPEDIA_GT)
#toughtables_wd = ground_truth(TOUGH_TABLES_WIKIDATA_GT)
#wikitables_2013_dbp = ground_truth(WIKITABLES_2013_DBPEDIA_GT)
#wikitables_2013_wd = ground_truth(WIKITABLES_2013_WIKIDATA_GT)
#wikitables_2019_dbp = ground_truth(WIKITABLES_2019_DBPEDIA_GT)
#wikitables_2019_wd = ground_truth(WIKITABLES_2019_WIKIDATA_GT)

# TODO: Add the rest

print('Evaluating results...')

"""results_hardtables = {
    'bbw': bbw_hardtables,
    'EMBLOOKUP': emblookup_hardtables,
    'LexMa': lexma_hardtables
}
evaluate_quality('/measure', 'hardtables', results_hardtables, hardtables_gt)

results_tfood = {
    'bbw': bbw_tfood,
    'EMBLOOKUP': emblookup_tfood,
    'LexMa': lexma_tfood
}
evaluate_quality('/measure', 'tfood', results_tfood, tfood_gt)

results_toughtables_wd = {
    'bbw': bbw_toughtables,
    'EMBLOOKUP': emblookup_toughtables_wd,
    'LexMa': lexma_toughtables_wd
}
evaluate_quality('./', 'toughtables_wd', results_toughtables_wd, toughtables_wd)
"""
results_toughtables_dbp = {
    'EMBLOOKUP': emblookup_toughtables_dbp,
    'LexMa': lexma_toughtables_dbp
}
evaluate_quality('./', 'toughtables_dbp', results_toughtables_dbp, toughtables_dbp)

"""results_wikitables_2013_dbp = {
    'EMBLOOKUP': emblookup_wikitables_2013_dbp,
    'LexMa': lexma_wikitables_2013_dbp
}
evaluate_quality('./', 'wikitables_2013_dbp', results_wikitables_2013_dbp, wikitables_2013_dbp)

results_wikitables_2013_wd = {
    'bbw': bbw_wikitables_2013,
    'EMBLOOKUP': emblookup_wikitables_2013_wd,
    'LexMa': lexma_wikitables_2013_wd
}
evaluate_quality('./', 'wikitables_2013_wd', results_wikitables_2013_wd, wikitables_2013_wd)

results_wikitables_2019_dbp = {
    'EMBLOOKUP': emblookup_wikitables_2019_dbp,
    'LexMa': lexma_wikitables_2019_dbp
}
evaluate_quality('./', 'wikitables_2019_dbp', results_wikitables_2019_dbp, wikitables_2019_dbp)

results_wikitables_2019_wd = {
    'bbw': bbw_wikitables_2019,
    'EMBLOOKUP': emblookup_wikitables_2019_wd,
    'LexMa': lexma_wikitables_2019_wd
}
evaluate_quality('./', 'wikitables_2019_wd', results_wikitables_2019_wd, wikitables_2019_wd)
"""
print('Done')
