import csv
from data import *
import read_results as rr
import precision

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


print('Reading ground truth...')

hardtables_gt = ground_truth(SEMTAB_HARDTABLES_GT)
tfood_gt = ground_truth(SEMTAB_TFOOD_GT)
toughtables_dbp = ground_truth(TOUGH_TABLES_DBPEDIA_GT)
toughtables_wd = ground_truth(TOUGH_TABLES_WIKIDATA_GT)
wikitables_2013_dbp = ground_truth(WIKITABLES_2013_DBPEDIA_GT)
wikitables_2013_wd = ground_truth(WIKITABLES_2013_WIKIDATA_GT)
wikitables_2019_dbp = ground_truth(WIKITABLES_2019_DBPEDIA_GT)
wikitables_2019_wd = ground_truth(WIKITABLES_2019_WIKIDATA_GT)

# TODO: Add the rest

print('Evaluating results...')

results_hardtables = {
    'bbw': bbw_hardtables,
    'EMBLOOKUP': emblookup_hardtables
}
precision.write('/measure/precision_hardtables.csv', results_hardtables, hardtables_gt)

results_tfood = {
    'bbw': bbw_tfood,
    'EMBLOOKUP': emblookup_tfood
}
precision.write('/measure/precision_tfood.csv', results_tfood, tfood_gt)

results_toughtables_wd = {
    'bbw': bbw_toughtables,
    'EMBLOOKUP': emblookup_toughtables_wd
}
precision.write('/measure/precision_toughtables_wd.csv', results_toughtables_wd, toughtables_wd)

results_toughtables_dbp = {
    'EMBLOOKUP': emblookup_toughtables_dbp
}
precision.write('/measure/precision_toughtables_dbp.csv', results_toughtables_dbp, toughtables_dbp)

results_wikitables_2013_dbp = {
    'EMBLOOKUP': emblookup_wikitables_2013_dbp
}
precision.write('/measure/precision_wikitables_2013_dbp.csv', results_wikitables_2013_dbp, wikitables_2013_dbp)

results_wikitables_2013_wd = {
    'EMBLOOKUP': emblookup_wikitables_2013_wd
}
precision.write('/measure/precision_wikitables_2013_wd.csv', results_wikitables_2013_wd, wikitables_2013_wd)

results_wikitables_2019_dbp = {
    'EMBLOOKUP': emblookup_wikitables_2019_dbp
}
precision.write('/measure/precision_wikitables_2019_dbp.csv', results_wikitables_2019_dbp, wikitables_2019_dbp)

results_wikitables_2019_wd = {
    'EMBLOOKUP': emblookup_wikitables_2019_wd
}
precision.write('/measure/precision_wikitables_2019_wd.csv', results_wikitables_2019_wd, wikitables_2019_wd)

print('Done')
