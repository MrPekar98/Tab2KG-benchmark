import csv
from data import *
import read_results as rr
from quality import evaluate_quality
from runtime import linked_tables, linked_tables_emblookup

print('Reading experiment results...')

bbw_hardtables = rr.read_bbw(BBW + 'semtab_hardtables')
bbw_tfood = rr.read_bbw(BBW + 'tfood')
bbw_toughtables = rr.read_bbw(BBW + 'toughtables_wd')
bbw_wikitables_2013 = rr.read_bbw(BBW + 'wikitables_2013')
bbw_wikitables_2019 = rr.read_bbw(BBW + 'wikitables_2019')

emblookup_hardtables = rr.read_emblookup(EMBLOOKUP + 'semtab_hardtables/results.csv', 'wikidata')
emblookup_tfood = rr.read_read_emblookup(EMBLOOKUP + 'tfood/results.csv', 'wikidata')
emblookup_toughtables_dbp = rr.read_emblookup(EMBLOOKUP + 'toughtables_dbp/results.csv', 'dbpedia')
emblookup_toughtables_wd = rr.read_emblookup(EMBLOOKUP + 'toughtables_wd/results.csv', 'wikidata')
emblookup_wikitables_2013_dbp = rr.read_emblookup(EMBLOOKUP + 'wikitables_2013_dbp/results.csv', 'dbpedia')
emblookup_wikitables_2013_wd = rr.read_emblookup(EMBLOOKUP + 'wikitables_2013_wd/results.csv', 'wikidata')
emblookup_wikitables_2019_dbp = rr.read_emblookup(EMBLOOKUP + 'wikitables_2019_dbp/results.csv', 'dbpedia')
emblookup_wikitables_2019_wd = rr.read_emblookup(EMBLOOKUP + 'wikitables_2019_wd/results.csv', 'wikidata')

lexma_hardtables = rr.read_lexma(LEXMA + 'hardtables/')
lexma_tfood = rr.read_lexma(LEXMA + 'tfood/')
lexma_toughtables_dbp = rr.read_lexma(LEXMA + 'toughtables_dbp/')
lexma_toughtables_wd = rr.read_lexma(LEXMA + 'toughtables_wd/')
lexma_wikitables_2013_dbp = rr.read_lexma(LEXMA + 'wikitables_2013_dbp/')
lexma_wikitables_2013_wd = rr.read_lexma(LEXMA + 'wikitables_2013_wd/')
lexma_wikitables_2019_dbp = rr.read_lexma(LEXMA + 'wikitables_2019_dbp/')
lexma_wikitables_2019_wd = rr.read_lexma(LEXMA + 'wikitables_2019_wd/')

magic_hardtables = rr.read_magic(MAGIC + 'HardTables/')
magic_tfood = rr.read_magic(MAGIC + 'tfood/')
magic_toughtables_dbp = rr.read_magic(MAGIC + 'tough_tables_dbp/')
magic_toughtables_dbp_candidates = rr.read_magic_candidates(MAGIC + 'tough_tables_dbp_candidates/')
magic_toughtables_wd = rr.read_magic(MAGIC + 'tough_tables_wd/')
magic_wikitables_2013_dbp = rr.read_magic(MAGIC + 'wikitables-2013_dbp/')
magic_wikitables_2013_wd = rr.read_magic(MAGIC + 'wikitables-2013_wd/')
magic_wikitables_2019_dbp = rr.read_magic(MAGIC + 'wikitables-2019_dbp/')
magic_wikitables_2019_dbp_candidates = rr.read_magic_candidates(MAGIC + 'wikitables-2019_dbp_candidates/')
magic_wikitables_2019_wd = rr.read_magic(MAGIC + 'wikitables-2019_wd/')

print('Reading ground truth...')

hardtables_gt = ground_truth(SEMTAB_HARDTABLES_GT)
tfood_gt = ground_truth(SEMTAB_TFOOD_GT)
toughtables_dbp = ground_truth(TOUGH_TABLES_DBPEDIA_GT)
toughtables_wd = ground_truth(TOUGH_TABLES_WIKIDATA_GT)
wikitables_2013_dbp = ground_truth(WIKITABLES_2013_DBPEDIA_GT)
wikitables_2013_wd = ground_truth(WIKITABLES_2013_WIKIDATA_GT)
wikitables_2019_dbp = ground_truth(WIKITABLES_2019_DBPEDIA_GT)
wikitables_2019_wd = ground_truth(WIKITABLES_2019_WIKIDATA_GT)

print('Evaluating results...')

results_hardtables = {
    'bbw': bbw_hardtables,
    'EMBLOOKUP': emblookup_hardtables,
    'LexMa': lexma_hardtables,
    'MAGIC': magic_hardtables
}
evaluate_quality('/measure', 'hardtables', results_hardtables, None, hardtables_gt)

results_tfood = {
    'bbw': bbw_tfood,
    'EMBLOOKUP': emblookup_tfood,
    'LexMa': lexma_tfood,
    'MAGIC': magic_tfood
}
evaluate_quality('/measure', 'tfood', results_tfood, None, tfood_gt)

results_toughtables_wd = {
    'bbw': bbw_toughtables,
    'EMBLOOKUP': emblookup_toughtables_wd,
    'LexMa': lexma_toughtables_wd,
    'MAGIC': magic_toughtables_wd
}
evaluate_quality('/measure', 'toughtables_wd', results_toughtables_wd, None, toughtables_wd)

results_toughtables_dbp = {
    'EMBLOOKUP': emblookup_toughtables_dbp,
    'LexMa': lexma_toughtables_dbp,
    'MAGIC': magic_toughtables_dbp
}
candidates_toughtables_dbp = {
    'bbw':
    'EMBLOOKUP':
    'LexMa':
    'MAGIC': magic_toughtables_dbp_candidates
}
evaluate_quality('/measure', 'toughtables_dbp', results_toughtables_dbp, candidates_toughtables_dbp, toughtables_dbp)

results_wikitables_2013_dbp = {
    'EMBLOOKUP': emblookup_wikitables_2013_dbp,
    'LexMa': lexma_wikitables_2013_dbp,
    'MAGIC': magic_wikitables_2013_dbp
}
evaluate_quality('/measure', 'wikitables_2013_dbp', results_wikitables_2013_dbp, None, wikitables_2013_dbp)

results_wikitables_2013_wd = {
    'bbw': bbw_wikitables_2013,
    'EMBLOOKUP': emblookup_wikitables_2013_wd,
    'LexMa': lexma_wikitables_2013_wd,
    'MAGIC': magic_wikitables_2013_wd
}
evaluate_quality('/measure', 'wikitables_2013_wd', results_wikitables_2013_wd, None, wikitables_2013_wd)

results_wikitables_2019_dbp = {
    'EMBLOOKUP': emblookup_wikitables_2019_dbp,
    'LexMa': lexma_wikitables_2019_dbp,
    'MAGIC': magic_wikitables_2019_dbp
}
candidates_wikitables_2019_dbp = {
    'bbw':
    'EMBLOOKUP':
    'LexMa':
    'MAGIC': magic_wikitables_2019_dbp_candidates
}
evaluate_quality('/measure', 'wikitables_2019_dbp', results_wikitables_2019_dbp, candidates_wikitables_2019_dbp, wikitables_2019_dbp)

results_wikitables_2019_wd = {
    'bbw': bbw_wikitables_2019,
    'EMBLOOKUP': emblookup_wikitables_2019_wd,
    'LexMa': lexma_wikitables_2019_wd,
    'MAGIC': magic_wikitables_2019_wd
}
evaluate_quality('/measure', 'wikitables_2019_wd', results_wikitables_2019_wd, None, wikitables_2019_wd)

print('\nEvaluating scalability')

linked_tables(BBW + 'toughtables_wd_scalability/', 'BBW', 'Tough Tables - Wikidata')
linked_tables(BBW + 'wikitables_scalability/', 'BBW', 'Wikitables 2013')
linked_tables(LEXMA + 'toughtables_wd_scalability/', 'LexMa', 'Tough Tables - Wikidata')
linked_tables(LEXMA + 'wikitables_dbp_2013_scalability/', 'LexMa', 'Wikitables 2013')
linked_tables(MAGIC + 'toughtables_wd_scalability/', 'MAGIC', 'Tough Tables - Wikidata')
linked_tables(MAGIC + 'wikitables_dbp_2013_scalability/', 'MAGIC', 'Wikitables 2013')
linked_tables_emblookup(EMBLOOKUP + 'toughtables_wd_scalability/results.csv', 'EMBLOOKUP', 'Tough Tables - Wikidata')
linked_tables_emblookup(EMBLOOKUP + 'wikitables_dbp_2013_scalability/results.csv', 'EMBLOOKUP', 'Wikitables 2013')

print('Done')
