#!/bin/bash

set -e

echo "Setting up keyword-kg-linker"
cd /home/keyword-kg-linker

if [[ ! -d DBpedia-12-2022/ ]]
then
    LABEL_PREDICATE="rdfs__label"

    mkdir -p DBpedia-12-2022/
    mkdir -p DBpedia-03-2022/
    mkdir -p DBpedia-10-2016/
    mkdir -p DBpedia-2014/
    mkdir -p Wikidata/

    echo "Indexing keyword-kg-linker on DBpedia 12/2022"
    /setup/kg/neo4j-dbpedia-12-2022/bin/neo4j start
    sleep 15m
    ./linker.sh -dir DBpedia-12-2022/ -predicate ${LABEL_PREDICATE}
    /setup/kg/neo4j-dbpedia-12-2022/bin/neo4j stop
    sleep 1m

    echo "Indexing keyword-kg-linker on DBpedia 03/2022"
    /setup/kg/neo4j-dbpedia-03-2022/bin/neo4j start
    sleep 15m
    ./linker.sh -dir DBpedia-03-2022/ -predicate ${LABEL_PREDICATE}
    /setup/kg/neo4j-dbpedia-03-2022/bin/neo4j stop
    sleep 1m

    echo "Indexing keyword-kg-linker on DBpedia 10/2016"
    /setup/kg/neo4j-dbpedia-10-2016/bin/neo4j start
    sleep 15m
    ./linker.sh -dir DBpedia-10-2016/ -predicate ${LABEL_PREDICATE}
    /setup/kg/neo4j-dbpedia-10-2016/bin/neo4j stop
    sleep 1m

    echo "Indexing keyword-kg-linker on DBpedia 2014"
    /setup/kg/neo4j-dbpedia-2014/bin/neo4j start
    sleep√15m
    ./linker.sh -dir DBpedia-2014/ -predicate ${LABEL_PREDICATE}
    /setup/kg/neo4j-dbpedia-2014/bin/neo4j stop
    sleep 1m

    echo "Indexing keyword-kg-linker on Wikidata"
    /setup/kg/neo4j-wikidata/bin/neo4j start
    sleep 24h
    ./linker.sh -dir Wikidata/ -predicate ${LABEL_PREDICATE}
    /setup/kg/neo4j-wikidata/bin/neo4j stop
    sleep 1m

    echo "Done indexing keyword-kg-linker"
fi

cd /home

echo "Setting up EmbLookup"

echo "Setting up TK2Match"

echo "Setting up bbw"

echo "Setting up LexMa"

echo "Setting up REL"
