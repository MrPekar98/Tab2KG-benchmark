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
mv files webcommons/dbpedia

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
mkdir -p semtab
wget https://zenodo.org/record/7416036/files/HardTablesR2.zip?download=1 -O HardTablesR2.zip
unzip HardTablesR2.zip
mv HardTablesR2 semtab/
rm HardTablesR2.zip
ln -s /home/tough_tables/wikidata /home/semtab/wikidata
wget https://zenodo.org/record/7319654/files/biodivtab_benchmark.zip?download=1 -O BioDivTab_WD.zip
unzip BioDivTab_WD.zip
rm BioDivTab_WD.zip
mv biodivtab_benchmark semtab/
wget wget https://zenodo.org/record/7319654/files/BiodivTab_DBpedia.zip?download=1 -O BioDivTab_DBP.zip
unzip BioDivTab_DBP.zip
rm BioDivTab_DBP.zip
mv BiodivTab_DBpedia semtab/

query=$(curl -H "Accept:text/sparql" https://databus.dbpedia.org/dbpedia/collections/dbpedia-snapshot-2022-03)
files=$(curl -X POST -H "Accept: text/csv" --data-urlencode "query=${query}" https://databus.dbpedia.org/sparql | tail -n +2 | sed 's/\r$//' | sed 's/"//g')
while IFS= read -r file ; do wget $file; done <<< "$files"
mkdir semtab/dbpedia_2022-03/

for FILE in *.bzip2 ;\
do
    bzip2 -dk ${FILE} -k -c > semtab/dbpedia_2022-03/${FILE:0:-6}
    rm ${FILE}
done

rm "*=*"

# WikiTables (2013)
git clone https://github.com/EDAO-Project/SemanticTableSearchDataset.git
mv SemanticTableSearchDataset/table_corpus/tables_2013/ .
mkdir -p wikitables/wikitables_2013/

for F in tables_2013/* ;\
do
    tar -xf ${F}
    mv ${F:12:-7}/* wikitables/wikitables_2013/
    rm -r ${F:12:-7}
done

rm -r tables_2013/

# WikiTables (2019)
mv SemanticTableSearchDataset/table_corpus/tables_2019/ .
rm -r SemanticTableSearchDataset
mkdir -p wikitables/wikitables_2019/

for F in tables_2019/* ;\
do
    tar -xf ${F}
    mv ${F:0:-7}/* wikitables/wikitables_2019/
done

rm -r tables_2019/

echo
echo "Importing DBpedia 12/2022"
./kg/neo4j-dbpedia-12-2022/bin/neo4j start
sleep 30s
./kg/import.sh kg/dbpedia kg/neo4j-dbpedia-12-2022
./kg/neo4j-dbpedia-12-2022/bin/neo4j stop
sleep 30s

echo
echo "Importing DBpedia 03/2022"
./kg/neo4j-dbpedia-03-2022/bin/neo4j start
sleep 30s
./kg/import.sh semtab/dbpedia_2022-03 kg/neo4j-dbpedia-03-2022
./kg/neo4j-dbpedia-03-2022/bin/neo4j stop
sleep 30s

echo
echo "Importing DBpedia 10/2016"
./kg/neo4j-dbpedia-10-2016/bin/neo4j start
sleep 30s
./kg/import.sh tough_tables/dbpedia kg/neo4j-dbpedia-10-2016
./kg/neo4j-dbpedia-10-2016/bin/neo4j stop
sleep 30s

echo
echo "Importing DBpedia 2014"
./kg/neo4j-dbpedia-2014/bin/neo4j start
sleep 30s
./kg/import.sh webcommons/dbpedia kg/neo4j-dbpedia-2014
./kg/neo4j-dbpedia-2014/bin/neo4j stop
sleep 30s

#echo
echo "Importing Wikidata"
./kg/neo4j-wikidata/bin/neo4j start
sleep 1m
./kg/import.sh kg/wikidata kg/neo4j-wikidata
./kg/neo4j-wikidata/bin/neo4j stop
sleep 30s
