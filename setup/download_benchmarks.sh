#!/bin/bash

set -e

# WebDataCommons
if [[ ${WEB_DATA_COMMONS} == "true" ]]
then
    wget http://webdatacommons.org/webtables/extended_instance_goldstandard.tar.gz
    tar -xf extended_instance_goldstandard.tar.gz
    mv classes_GS.csv webcommons/
    mv tables/ webcommons/
    mv instance/ webcommons/
    mv property/ webcommons/
    rm extended_instance_goldstandard.tar.gz
    ./kg/download-files.sh webcommons/dbpedia-files.txt
    mv files webcommons/dbpedia
fi

# Tough Tables (DBpedia)
if [[ ${TOUGHTABLES_DBPEDIA} == "true" ]]
then
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
fi

# Tough Tables (Wikidata)
if [[ ${TOUGHTABLES_WIKIDATA} == "true" ]]
then
    wget -O 2T_wd.zip https://zenodo.org/records/7419275/files/ToughTables-WD_v3.zip?download=1
    unzip 2T_wd.zip
    rm 2T_wd.zip
    rm CEA_WD_Evaluator.py CTA_WD_Evaluator.py
    mv DataSets/ToughTablesR2-WD/ tough_tables/
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
    mkdir -p /home/kg/sub_wikidata
    cp /home/tough_tables/wikidata/P31.nt /home/kg/sub_wikidata
    cp /home/tough_tables/wikidata/rdf-schema#label.nt /home/kg/sub_wikidata
    cp /home/tough_tables/wikidata/description.nt /home/kg/sub_wikidata
    cp /home/tough_tables/wikidata/P910.nt /home/kg/sub_wikidata
    cp /home/tough_tables/wikidata/name.nt /home/kg/sub_wikidata
    cp /home/tough_tables/wikidata/entities.nt /home/kg/sub_wikidata
fi

# SemTab 2023
if [[ ${HARDTABLES} == "true" ]]
then
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
then

# WikiTables (2013)
if [[ ${WIKITABLES_2013} == "true" ]]
then
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
fi

# WikiTables (2019)
if [[ ${WIKITABLES_2019} == "true" ]]
then
    if [ ! -d SemanticTableSearchDataset/ ]
    then
        git clone https://github.com/EDAO-Project/SemanticTableSearchDataset.git
    fi

    mv SemanticTableSearchDataset/table_corpus/tables_2019/ .
    mkdir -p wikitables/wikitables_2019/

    for F in tables_2019/* ;\
    do
        tar -xf ${F}
        mv ${F:0:-7}/* wikitables/wikitables_2019/
    done

    rm -r tables_2019/
fi

if [ -d SemanticTableSearchDataset/ ]
then
    rm -r SemanticTableSearchDataset/
fi

# tFood
if [[ ${TFOOD} == "true" ]]
then
    wget https://zenodo.org/records/10048187/files/tfood_wiith_test_gt.zip?download=1 -O tfood.zip
    unzip tfood.zip
    rm tfood.zip
fi

if [[ ${WIKITABLES_2013} == "true" || ${WIKITABLES_2019} == "true" ]]
then
    echo
    echo "Downloading DBpedia 12/2022"
    ./kg/download-files.sh kg/dbpedia_files.txt
    mv files/ kg/dbpedia/

    echo "Importing DBpedia 12/2022"
    ./kg/neo4j-dbpedia-12-2022/bin/neo4j start
    sleep 30s
    ./kg/import.sh kg/dbpedia kg/neo4j-dbpedia-12-2022
    ./kg/neo4j-dbpedia-12-2022/bin/neo4j stop
    sleep 30s
fi

if [[ ${TOUGHTABLES_DBPEDIA} == "true" ]]
then
    echo
    echo "Importing DBpedia 10/2016"
    ./kg/neo4j-dbpedia-10-2016/bin/neo4j start
    sleep 30s
    ./kg/import.sh tough_tables/dbpedia kg/neo4j-dbpedia-10-2016
    ./kg/neo4j-dbpedia-10-2016/bin/neo4j stop
    sleep 30s
fi

if [[ ${WIKITABLES_2013} == "true" || ${WIKITABLES_2019} == "true" || ${TOUGHTABLES_WIKIDATA} == "true" || ${HARDTABLES} == "true" || ${TFOOD} == "true" ]]
then
    echo
    echo "Importing Wikidata"
    ./kg/neo4j-wikidata/bin/neo4j start
    sleep 1m
    ./kg/import.sh kg/wikidata kg/neo4j-wikidata
    ./kg/neo4j-wikidata/bin/neo4j stop
    sleep 30s
fi
