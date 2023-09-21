#!/bin/bash

set -e

command="new"

if [[ -f ".Wikitables2013_DBpedia.stats" ]]
then
    command="load"
fi

# WikiTables
#/home/setup/kg/neo4j-dbpedia/bin/neo4j start
#sleep 5m
#python3 /home/setup/analysis/analyze_wikitables_dbpedia.py ${command}
#/home/setup/kg/neo4j-dbpedia/bin/neo4j stop
#sleep 1m

/home/setup/kg/neo4j-wikidata/bin/neo4j start
sleep 20m
python3 /home/setup/analysis/analyze_wikitables_wikidata.py ${command}
/home/setup/kg/neo4j-wikidata/bin/neo4j stop
sleep 1m

# Tough Tables
python3 /home/setup/analysis/analyze_tough_tables.py ${command}

# SemTab
python3 /home/setup/analysis/analyze_semtab.py ${command}

# WebDataCommons
python3 /home/setup/analysis/analyze_web_data_commons.py ${command}
