#!/bin/bash

set -e

if [[ ${WIKITABLES_2013} == "true" ]]
then
    echo "WikiTables 2013"
    mkdir -p /benchmarks/wikitables_2013/tables/
    mkdir -p /benchmarks/wikitables_2013/gt/dbpedia/
    mkdir -p /benchmarks/wikitables_2013/gt/wikidata/

    ./kg/neo4j-dbpedia-12-2022/bin/neo4j start
    ./kg_wait.sh /home/setup/kg/neo4j-dbpedia-12-2022/
    python3 wikitables/wikitables_dbpedia.py 13
    python3 wikitables/wikitables_wikidata.py 13
    python3 extend_gt.py /benchmarks/wikitables_2013/gt/dbpedia/gt.csv dbpedia
    ./kg/neo4j-dbpedia-12-2022/bin/neo4j stop
    sleep 1m

    ./kg/neo4j-wikidata/bin/neo4j start
    ./kg_wait.sh /home/setup/kg/neo4j-wikidata/
    python3 extend_gt.py /benchmarks/wikitables_2013/gt/wikidata/gt.csv wikidata
    python3 dataset_subset.py 0.2 /benchmarks/wikitables_2013/
    ./kg/neo4j-wikidata/bin/neo4j stop
    sleep 1m
fi

if [[ ${WIKITABLES_2019} == "true" ]]
then
    echo "WikiTables 2019"
    mkdir -p /benchmarks/wikitables_2019/tables/
    mkdir -p /benchmarks/wikitables_2019/gt/dbpedia/
    mkdir -p /benchmarks/wikitables_2019/gt/wikidata/

    ./kg/neo4j-dbpedia-12-2022/bin/neo4j start
    ./kg_wait.sh /home/setup/kg/neo4j-dbpedia-12-2022/
    python3 wikitables/wikitables_dbpedia.py 19
    python3 wikitables/wikitables_wikidata.py 19
    python3 extend_gt.py /benchmarks/wikitables_2019/gt/dbpedia/gt.csv dbpedia
    ./kg/neo4j-dbpedia-12-2022/bin/neo4j stop
    sleep 1m

    ./kg/neo4j-wikidata/bin/neo4j start
    ./kg_wait.sh /home/setup/kg/neo4j-wikidata/
    python3 extend_gt.py /benchmarks/wikitables_2019/gt/wikidata/gt.csv wikidata
    python3 dataset_subset.py 0.2 /benchmarks/wikitables_2019/
    ./kg/neo4j-wikidata/bin/neo4j stop
    sleep 1m
fi

if [[ ${HARDTABLES} == "true" ]]
then
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
    python3 dataset_subset.py 0.2 /benchmarks/semtab/HardTables/
    python3 extend_gt.py /benchmarks/HardTables/gt/cea_gt.csv wikidata
fi

if [[ ${WEB_DATA_COMMONS} == "true" ]]
then
    echo "WebDataCommons"
    mkdir -p /benchmarks/webdatacommons/gt/
    mv webcommons/tables/ /benchmarks/webdatacommons/
    mv webcommons/instance/* /benchmarks/webdatacommons/gt/
    rm -rf webcommon/instance/
fi

if [[ ${TOUGHTABLES_DBPEDIA} == "true" ]]
then
    echo "Tough Tables - DBpedia"
    mkdir -p /benchmarks/toughtables/dbpedia/gt/
    mv tough_tables/ToughTablesR2-DBP/Test/tables/ /benchmarks/toughtables/dbpedia/
    mv tough_tables/ToughTablesR2-DBP/Test/gt/cea_gt.csv /benchmarks/toughtables/dbpedia/gt/
    rm -rf tough_tables/ToughTablesR2-DBP/ tough_tables/ToughTablesR2-WD/
    python3 dataset_subset.py 0.2 /benchmarks/toughtables/dbpedia/
fi

if [[ ${TOUGHTABLES_WIKIDATA} == "true" ]]
then
    echo "Tough Tables - Wikidata"
    mkdir -p /benchmarks/toughtables/wikidata/gt/
    mv tough_tables/ToughTablesR2-WD/Test/tables/ /benchmarks/toughtables/wikidata/
    mv tough_tables/ToughTablesR2-WD/Test/gt/cea_gt.csv /benchmarks/toughtables/wikidata/gt/
    python3 dataset_subset.py 0.2 /benchmarks/toughtables/wikidata/
fi

if [[ ${TFOOD} == "true" ]]
then
    echo "tFood"
    rm -rf tfoof/entity/ tfood/horizontal/val/ tfood/horizontal/test/targets/
    mv tfood/horizontal/test/* tfood/horizontal/
    rmdir tfood/horizontal/test/
    mv tfood/ /benchmarks/semtab/
    python3 dataset_subset.py 0.2 /benchmarks/semtab/tfood/horizontal/
    python3 extend_gt.py /benchmarks/semtab/tfood/horizontal/gt/cea_gt.csv wikidata
    ./kg/neo4j-wikidata/bin/neo4j stop
    sleep 1m
fi
