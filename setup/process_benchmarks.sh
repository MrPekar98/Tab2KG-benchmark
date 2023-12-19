#!/bin/bash

set -e

echo "WikiTables"
mkdir -p /benchmarks/wikitables_2013/tables/
mkdir -p /benchmarks/wikitables_2013/gt/dbpedia/
mkdir -p /benchmarks/wikitables_2013/gt/wikidata/
mkdir -p /benchmarks/wikitables_2019/tables/
mkdir -p /benchmarks/wikitables_2019/gt/dbpedia/
mkdir -p /benchmarks/wikitables_2019/gt/wikidata/

./kg/neo4j-dbpedia-12-2022/bin/neo4j start
sleep 10m
python3 wikitables/wikitables_dbpedia.py 13
python3 wikitables/wikitables_dbpedia.py 19
python3 wikitables/wikitables_wikidata.py 13
python3 wikitables/wikitables_wikidata.py 19
./kg/neo4j-dbpedia-12-2022/bin/neo4j stop
sleep 1m

python3 wikitables_subset.py 10000 2013
python3 wikitables_subset.py 10000 2019

echo "Semtab"
mkdir -p /benchmarks/semtab/HardTables/gt/
mkdir -p /benchmarks/semtab/biodivtab/dbpedia/gt/
mkdir -p /benchmarks/semtab/biodivtab/wikidata/gt/
mv semtab/HardTablesR2/DataSets/HardTablesR2/Test/tables/ /benchmarks/semtab/HardTables/
mv semtab/HardTablesR2/DataSets/HardTablesR2/Test/gt/cea_gt.csv /benchmarks/semtab/HardTables/gt/
mv semtab/BiodivTab_DBpedia/test/tables/ /benchmarks/semtab/biodivtab/dbpedia/
mv semtab/BiodivTab_DBpedia/test/gt/CEA_biodivtab_gt.csv /benchmarks/semtab/biodivtab/dbpedia/gt/
mv semtab/biodivtab_benchmark/tables/ /benchmarks/semtab/biodivtab/wikidata/
mv semtab/biodivtab_benchmark/gt/CEA_biodivtab_2021_gt.csv /benchmarks/semtab/biodivtab/wikidata/gt/
rm -rf semtab/HardTablesR2/
rm -rf semtab/BiodivTab_DBpedia/
rm -rf semtab/biodivtab_benchmark/

echo "WebDataCommons"
mkdir -p /benchmarks/webdatacommons/gt/
mv webcommons/tables/ /benchmarks/webdatacommons/
mv webcommons/instance/* /benchmarks/webdatacommons/gt/
rm -rf webcommon/instance/

echo "Tough Tables"
mkdir -p /benchmarks/toughtables/dbpedia/gt/
mkdir -p /benchmarks/toughtables/wikidata/gt/
mv tough_tables/ToughTablesR2-DBP/Test/tables/ /benchmarks/toughtables/dbpedia/
mv tough_tables/ToughTablesR2-DBP/Test/gt/cea_gt.csv /benchmarks/toughtables/dbpedia/gt/
mv tough_tables/ToughTablesR2-WD/Test/tables/ /benchmarks/toughtables/wikidata/
mv tough_tables/ToughTablesR2-WD/Test/gt/cea_gt.csv /benchmarks/toughtables/wikidata/gt/
rm -rf tough_tables/ToughTablesR2-DBP/ tough_tables/ToughTablesR2-WD/

echo "tFood"
rm -rf tfoof/entity/ tfood/horizontal/val/ tfood/horizontal/test/targets/
mv tfood/horizontal/test/* tfood/horizontal/
rmdir tfood/horizontal/test/
mv tfood/ /benchmarks/semtab/
