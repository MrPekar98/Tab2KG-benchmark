#!/bin/bash

set -e

command="new"

# WikiTables

if [[ -f "/plots/.Wikitables2013_DBpedia.stats" ]]
then
    command="load"
fi

/home/setup/kg/neo4j-dbpedia/bin/neo4j start
sleep 10m
python3 /home/setup/analysis/analyze_wikitables_dbpedia.py ${command}
/home/setup/kg/neo4j-dbpedia/bin/neo4j stop
sleep 1m

if [[ -f "/plots/.Wikitables2013_Wikidata.stats" ]]
then
    command="load"
else
    command="new"
fi

/home/setup/kg/neo4j-wikidata/bin/neo4j start
#sleep 24h
sleep 15m
python3 /home/setup/analysis/analyze_wikitables_wikidata.py ${command}
/home/setup/kg/neo4j-wikidata/bin/neo4j stop
sleep 1m

# Tough Tables

if [[ -f "/plots/.ToughTables_DBpedia.stats" ]]
then
    command="load"
else
    command="new"
fi

/home/setup/kg/neo4j-dbpedia/bin/neo4j start
sleep 10m
python3 /home/setup/analysis/analyze_tough_tables_dbpedia.py ${command}
/home/setup/kg/neo4j-dbpedia/bin/neo4j stop
sleep 1m

if [[ -f "/plots/.ToughTables_Wikidata.stats" ]]
then
    command="load"
else
    command="new"
fi

/home/setup/kg/neo4j-wikidata/bin/neo4j start
#sleep 24h
sleep 15m
python3 /home/setup/analysis/analyze_tough_tables_wikidata.py ${command}

# SemTab

if [[ -f "/plots/.SemTab.stats" ]]
then
    command="load"
else
    command="new"
fi

python3 /home/setup/analysis/analyze_semtab.py ${command}
/home/setup/kg/neo4j-wikidata/bin/neo4j stop
sleep 1m

# WebDataCommons

if [[ -f ".SemTab.stats" ]]
then
    command="load"
else
    command="new"
fi

/home/setup/kg/neo4j-dbpedia/bin/neo4j start
sleep 10m
python3 /home/setup/analysis/analyze_web_data_commons.py ${command}
/home/setup/kg/neo4j-dbpedia/bin/neo4j stop
sleep 1m
