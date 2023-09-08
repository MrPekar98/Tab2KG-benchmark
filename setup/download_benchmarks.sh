#!/bin/bash

set -e

# WebDataCommons
wget http://webdatacommons.org/webtables/extended_instance_goldstandard.tar.gz
tar -xf extended_instance_goldstandard.tar.gz
mv classes_GS.csv webcommons/
mv tables/ webcommons/
mv instance/ webcommons/
mv property/ webcommons/
rm extended_instance_goldstandard.tar.gz
./kg/download-files.sh webcommons/dbpedia-files.txt

# Tough Tables (DBpedia)
wget https://zenodo.org/record/7419275/files/ToughTables-DBP_v3.zip?download=1
mv 'ToughTables-DBP_v3.zip?download=1' ToughTables-DBP_v3.zip
unzip ToughTables-DBP_v3.zip
mv DataSets/ToughTablesR2-DBP/ tough_tables/
rm CEA_DBP_Evaluator.py
rm CTA_DBP_Evaluator.py
rm ToughTables-DBP_v3.zip
rmdir DataSets/
git clone https://github.com/vcutrona/tough-tables.git
mv tough-tables/ tough_tables/repo/
./kg/download-files.sh tough_tables/dbpedia-2016.txt
mv files tough_tables/dbpedia/

# Tough Tables (Wikidata)
wget https://zenodo.org/record/7419275/files/ToughTables-WD_v3.zip?download=1
mv 'ToughTables-WD_v3.zip?download=1' ToughTables-WD_v3.zip
unzip ToughTables-WD_v3.zip
mv DataSets/ToughTablesR2-WD/ tough_tables/
rm ToughTables-WD_v3.zip
rm CEA_WD_Evaluator.py
rm CTA_WD_Evaluator.py
rmdir DataSets/
wget https://zenodo.org/record/6643443/files/wikidata-20220521-truthy.nt.bz2?download=1
mv 'wikidata-20220521-truthy.nt.bz2?download=1' wikidata.nt.bz2
bzip2 -dk wikidata.nt.bz2
rm wikidata.nt.bz2
mkdir -p tough_tables/wikidata/
mv wikidata.nt tough_tables/wikidata/
python3 tough_tables/split.py
rm /home/tough_tables/wikidata/wikidata.nt
ln -s /home/tough_tables/wikidata /home/kg/wikidata

# SemTab 2023
wget https://github.com/sem-tab-challenge/2023/raw/main/datasets/WikidataTables2023R1.tar.gz
tar -xf WikidataTables2023R1.tar.gz
mv DataSets/ semtab/
rm WikidataTables2023R1.tar.gz
rm CEA_WD_Evaluator.py
rm CPA_WD_Evaluator.py
rm CTA_WD_Evaluator.py
ln -s /home/tough_tables/wikidata /home/semtab/wikidata

# WikiTables (2019)
git clone https://github.com/EDAO-Project/SemanticTableSearchDataset.git
mv SemanticTableSearchDataset/table_corpus/tables_2019/ .
rm -r SemanticTableSearchDataset
mkdir -p wikitables/wikitables/

for F in tables_2019/* ;\
do
    tar -xf ${F}
    mv ${F:0:-7}/* wikitables/wikitables/
done

rm -r tables_2019/

echo
echo "Importing DBpedia"
./kg/neo4j-dbpedia/bin/neo4j start
sleep 30s
./kg/import.sh kg/dbpedia kg/neo4j-dbpedia
./kg/neo4j-dbpedia/bin/neo4j stop
sleep 30s

echo
echo "Importing Wikidata"
./kg/neo4j-wikidata/bin/neo4j start
sleep 1m
./kg/import.sh kg/wikidata kg/neo4j-wikidata
./kg/neo4j-wikidata/bin/neo4j stop
sleep 30s
