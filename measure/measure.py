import csv
from data import *
import read_results as rr
from quality import evaluate_quality
from runtime import *

print('Reading experiment results...')

bbw_hardtables = rr.read_bbw(BBW + 'semtab_hardtables')
bbw_tfood = rr.read_bbw(BBW + 'tfood')
bbw_toughtables = rr.read_bbw(BBW + 'toughtables_wd')
bbw_toughtables_candidates = rr.read_bbw_candidates(BBW + 'toughtables_candidates/')
bbw_wikitables_2013 = rr.read_bbw(BBW + 'wikitables_2013')
bbw_wikitables_2019 = rr.read_bbw(BBW + 'wikitables_2019')
bbw_wikitables_2019_candidates = rr.read_bbw_candidates(BBW + 'wikitables_2019_candidates/')

emblookup_hardtables = rr.read_emblookup(EMBLOOKUP + 'semtab_hardtables/results.csv', 'wikidata')
emblookup_tfood = rr.read_emblookup(EMBLOOKUP + 'tfood/results.csv', 'wikidata')
emblookup_toughtables_dbp = rr.read_emblookup(EMBLOOKUP + 'toughtables_dbp/results.csv', 'dbpedia')
emblookup_toughtables_dbp_candidates = rr.read_emblookup_candidates(EMBLOOKUP + 'toughtables_dbp_candidates/results.csv', 'dbpedia')
emblookup_toughtables_wd = rr.read_emblookup(EMBLOOKUP + 'toughtables_wd/results.csv', 'wikidata')
emblookup_toughtables_wd_more = rr.read_emblookup(EMBLOOKUP + 'toughtables_wd_more_training/results.csv', 'wikidata')
emblookup_toughtables_wd_less = rr.read_emblookup(EMBLOOKUP + 'toughtables_wd_less_training/results.csv', 'wikidata')
emblookup_wikitables_2013_dbp = rr.read_emblookup(EMBLOOKUP + 'wikitables_2013_dbp/results.csv', 'dbpedia')
emblookup_wikitables_2013_wd = rr.read_emblookup(EMBLOOKUP + 'wikitables_2013_wd/results.csv', 'wikidata')
emblookup_wikitables_2019_dbp = rr.read_emblookup(EMBLOOKUP + 'wikitables_2019_dbp/results.csv', 'dbpedia')
emblookup_wikitables_2019_dbp_candidates = rr.read_emblookup_candidates(EMBLOOKUP + 'wikitables_2019_dbp_candidates/results.csv', 'dbpedia')
emblookup_wikitables_2019_wd = rr.read_emblookup(EMBLOOKUP + 'wikitables_2019_wd/results.csv', 'wikidata')
emblookup_wikitables_2019_wd_mroe = rr.read_emblookup(EMBLOOKUP + 'wikitables_2019_wd_more_training/results.csv', 'wikidata')
emblookup_wikitables_2019_wd_less = rr.read_emblookup(EMBLOOKUP + 'wikitables_2019_wd_less_training/results.csv', 'wikidata')

lexma_hardtables = rr.read_lexma(LEXMA + 'hardtables/')
lexma_tfood = rr.read_lexma(LEXMA + 'tfood/')
lexma_toughtables_dbp = rr.read_lexma(LEXMA + 'toughtables_dbp/')
lexma_toughtables_dbp_candidates = rr.read_lexma_candidates(LEXMA + 'toughtables_dbp_candidates/')
lexma_toughtables_wd = rr.read_lexma(LEXMA + 'toughtables_wd/')
lexma_wikitables_2013_dbp = rr.read_lexma(LEXMA + 'wikitables_2013_dbp/')
lexma_wikitables_2013_wd = rr.read_lexma(LEXMA + 'wikitables_2013_wd/')
lexma_wikitables_2019_dbp = rr.read_lexma(LEXMA + 'wikitables_2019_dbp/')
lexma_wikitables_2019_dbp_candidates = rr.read_lexma_candidates(LEXMA + 'wikitables_2019_dbp_candidates/')
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

naive_keyword_hardtables = rr.read_keyword_kg_linker(NAIVE + 'hardtables/keyword/')
naive_embeddings_hardtables = rr.read_keyword_kg_linker(NAIVE + 'hardtables/embeddings/')
naive_keyword_toughtables_dbp = rr.read_keyword_kg_linker(NAIVE + 'toughtables_dbp/keyword/')
naive_keyword_toughtables_dbp_candidates = rr.read_keyword_kg_linker_candidates(NAIVE + 'toughtables_dbp_candidates/keyword/')
naive_embeddings_toughtables_dbp = rr.read_keyword_kg_linker(NAIVE + 'toughtables_dbp/embeddings/')
naive_keyword_toughtables_wd = rr.read_keyword_kg_linker(NAIVE + 'toughtables_wd/keyword/')
naive_embeddings_toughtables_wd = rr.read_keyword_kg_linker(NAIVE + 'toughtables_wd/embeddings/')
naive_keyword_tfood = rr.read_keyword_kg_linker(NAIVE + 'tfood/keyword/')
naive_embeddings_tfood = rr.read_keyword_kg_linker(NAIVE + 'tfood/embeddings/')
naive_keyword_wikitables_2013_dbp = rr.read_keyword_kg_linker(NAIVE + 'wikitables_2013_dbp/keyword/')
naive_embeddings_wikitables_2013_dbp = rr.read_keyword_kg_linker(NAIVE + 'wikitables_2013_dbp/embeddings/')
naive_keyword_wikitables_2013_wd = rr.read_keyword_kg_linker(NAIVE + 'wikitables_2013_wd/keyword/')
naive_embeddings_wikitables_2013_wd = rr.read_keyword_kg_linker(NAIVE + 'wikitables_2013_wd/embeddings/')
naive_keyword_wikitables_2019_dbp = rr.read_keyword_kg_linker(NAIVE + 'wikitables_2019_dbp/keyword/')
naive_keyword_wikitables_2019_dbp_candidates = rr.read_keyword_kg_linker_candidates(NAIVE + 'wikitables_2019_dbp_candidates/keyword/')
naive_embeddings_wikitables_2019_dbp = rr.read_keyword_kg_linker(NAIVE + 'wikitables_2019_dbp/embeddings/')
naive_keyword_wikitables_2019_wd = rr.read_keyword_kg_linker(NAIVE + 'wikitables_2019_wd/keyword/')
naive_embeddings_wikitables_2019_wd = rr.read_keyword_kg_linker(NAIVE + 'wikitables_2019_wd/embeddings/')

print('Reading ground truth...')

hardtables_gt = ground_truth(SEMTAB_HARDTABLES_GT)
tfood_gt = ground_truth(SEMTAB_TFOOD_GT)
toughtables_dbp = ground_truth(TOUGH_TABLES_DBPEDIA_GT)
toughtables_wd = ground_truth(TOUGH_TABLES_WIKIDATA_GT)
toughtables_wd_entity_cells = entity_cells(TOUGH_TABLES_WIKIDATA_ENTITY_CELLS)
wikitables_2013_dbp = ground_truth(WIKITABLES_2013_DBPEDIA_GT)
wikitables_2013_wd = ground_truth(WIKITABLES_2013_WIKIDATA_GT)
wikitables_2019_dbp = ground_truth(WIKITABLES_2019_DBPEDIA_GT)
wikitables_2019_wd = ground_truth(WIKITABLES_2019_WIKIDATA_GT)
wikitables_2019_wd_entity_cells = entity_cells(WIKITABLES_2019_WIKIDATA_ENTITY_CELLS)

print('Evaluating results...')

results_hardtables = {
    'bbw': bbw_hardtables,
    'EMBLOOKUP': emblookup_hardtables,
    'LexMa': lexma_hardtables,
    'MAGIC': magic_hardtables,
    'Naive_k': naive_keyword_hardtables
}
evaluate_quality('/measure', 'hardtables', results_hardtables, None, None, hardtables_gt, None)

results_tfood = {
    'bbw': bbw_tfood,
    'EMBLOOKUP': emblookup_tfood,
    'LexMa': lexma_tfood,
    'MAGIC': magic_tfood,
    'Naive_k': naive_keyword_tfood
}
evaluate_quality('/measure', 'tfood', results_tfood, None, None, tfood_gt, None)

results_toughtables_wd = {
    'bbw': bbw_toughtables,
    'EMBLOOKUP': emblookup_toughtables_wd,
    'EMBLOOKUP - more training': emblookup_toughtables_wd_more,
    'EMBLOOKUP - less training': emblookup_toughtables_wd_less,
    'LexMa': lexma_toughtables_wd,
    'MAGIC': magic_toughtables_wd,
    'Naive_k': naive_keyword_toughtables_wd
}
candidates_toughtables_wd = {
    'bbw': bbw_toughtables_candidates
}
non_rec_toughtables_wd = {
    'bbw': bbw_toughtables,
    'EMBLOOKUP': emblookup_toughtables_wd,
    'LexMa': lexma_toughtables_wd,
    'MAGIC': magic_toughtables_wd,
}
evaluate_quality('/measure', 'toughtables_wd', results_toughtables_wd, candidates_toughtables_wd, non_rec_toughtables_wd, toughtables_wd, toughtables_wd_entity_cells)

results_toughtables_dbp = {
    'EMBLOOKUP': emblookup_toughtables_dbp,
    'LexMa': lexma_toughtables_dbp,
    'MAGIC': magic_toughtables_dbp,
    'Naive_k': naive_keyword_toughtables_dbp
}
candidates_toughtables_dbp = {
    'EMBLOOKUP': emblookup_toughtables_dbp_candidates,
    'LexMa': lexma_toughtables_dbp_candidates,
    'MAGIC': magic_toughtables_dbp_candidates,
    'Naive_k': naive_keyword_toughtables_dbp_candidates
}
evaluate_quality('/measure', 'toughtables_dbp', results_toughtables_dbp, candidates_toughtables_dbp, None, toughtables_dbp, None)

results_wikitables_2013_dbp = {
    'EMBLOOKUP': emblookup_wikitables_2013_dbp,
    'LexMa': lexma_wikitables_2013_dbp,
    'MAGIC': magic_wikitables_2013_dbp,
    'Naive_k': naive_keyword_wikitables_2013_dbp
}
evaluate_quality('/measure', 'wikitables_2013_dbp', results_wikitables_2013_dbp, None, None, wikitables_2013_dbp, None)

results_wikitables_2013_wd = {
    'bbw': bbw_wikitables_2013,
    'EMBLOOKUP': emblookup_wikitables_2013_wd,
    'LexMa': lexma_wikitables_2013_wd,
    'MAGIC': magic_wikitables_2013_wd,
    'Naive_k': naive_keyword_wikitables_2013_wd
}
candidates_wikitables_2013_wd = {
    'bbw': bbw_wikitables_2013_candidates
}
evaluate_quality('/measure', 'wikitables_2013_wd', results_wikitables_2013_wd, candidates_wikitables_2013_wd, None, wikitables_2013_wd, None)

results_wikitables_2019_dbp = {
    'EMBLOOKUP': emblookup_wikitables_2019_dbp,
    'LexMa': lexma_wikitables_2019_dbp,
    'MAGIC': magic_wikitables_2019_dbp,
    'Naive_k': naive_keyword_wikitables_2019_dbp
}
candidates_wikitables_2019_dbp = {
    'EMBLOOKUP': emblookup_wikitables_2019_dbp_candidates,
    'LexMa': lexma_wikitables_2019_dbp_candidates,
    'MAGIC': magic_wikitables_2019_dbp_candidates,
    'Naive_k': naive_keyword_wikitables_2019_dbp_candidates
}
evaluate_quality('/measure', 'wikitables_2019_dbp', results_wikitables_2019_dbp, candidates_wikitables_2019_dbp, None, wikitables_2019_dbp, None)

results_wikitables_2019_wd = {
    'bbw': bbw_wikitables_2019,
    'EMBLOOKUP': emblookup_wikitables_2019_wd,
    'LexMa': lexma_wikitables_2019_wd,
    'MAGIC': magic_wikitables_2019_wd,
    'Naive_k': naive_keyword_wikitables_2019_wd,
    'EMBLOOKUP - less training': emblookup_wikitables_2019_wd_less
}
candidates_wikitables_2019_wd = {
    'bbw': bbw_wikitables_2019_candidates
}
non_rec_wikitables_2019_wd = {
    'bbw': bbw_wikitables_2019,
    'EMBLOOKUP': emblookup_wikitables_2019_wd,
    'LexMa': lexma_wikitables_2019_wd,
    'MAGIC': magic_wikitables_2019_wd,
}
evaluate_quality('/measure', 'wikitables_2019_wd', results_wikitables_2019_wd, candidates_wikitables_2019_wd, non_rec_wikitables_2019_wd, wikitables_2019_wd, wikitables_2019_wd_entity_cells)

print('\nEvaluating scalability')

magic_tough_tables_wd_linked_cells = magic_linked_cells(MAGIC + 'toughtables_wd_scalability/')
magic_wikitables_2019_dbp_linked_cells = magic_linked_cells(MAGIC + 'wikitables_wd_2019_scalability/')
lexma_tough_tables_wd_linked_cells = lexma_linked_cells(LEXMA + 'toughtables_wd_scalability/')
lexma_wikitables_2019_dbp_linked_cells = lexma_linked_cells(LEXMA + 'wikitables_dbp_2019_scalability/')
bbw_tough_tables_wd_linked_cells = bbw_linked_cells(BBW + 'toughtables_wd_scalability/')
bbw_wikitables_2019_linked_cells = bbw_linked_cells(BBW + 'wikitables_2019_scalability/')
emblookup_tough_tables_wd_linked_cells = emblookup_linked_cells(EMBLOOKUP + 'toughtables_wd_scalability/results.csv')
emblookup_wikitables_2019_linked_cells = emblookup_linked_cells(EMBLOOKUP + 'wikitables_dbp_2019_scalability/results.csv')

print('Linked cells')
print('MAGIC - Tough Tables (Wikidata):', magic_tough_tables_wd_linked_cells)
print('MAGIC - Wikitables 2019 (DBpedia):', magic_wikitables_2019_dbp_linked_cells)
print('\nLexMa - Tough Tables (Wikidata):', lexma_tough_tables_wd_linked_cells)
print('LexMa - Wikitables 2019 (DBpedia):', lexma_wikitables_2019_dbp_linked_cells)
print('\nbbw - Tough Tables (Wikidata):', bbw_tough_tables_wd_linked_cells)
print('bbw - Wikitables 2019 (Wikidata):', bbw_wikitables_2019_linked_cells)
print('\nEMBLOOKUP - Tough Tables (Wikidata):', emblookup_tough_tables_wd_linked_cells)
print('EMBLOOKUP - Wikitabkes 2019 (DBpedia):', emblookup_wikitables_2019_linked_cells)

print('\nDone')
