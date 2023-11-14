#!/bin/bash

set -e

pip3 install -e /home/setup/analysis

command="new"
kg_running="false"

# WikiTables

if [[ -f "/plots/.Wikitables2013_DBpedia.stats" ]]
then
    command="load"
else
    /home/setup/kg/neo4j-dbpedia-12-2022/bin/neo4j start
    kg_running="true"
    sleep 1h
fi

python3 /home/setup/analysis/analyze_wikitables_dbpedia.py ${command}

if [[ ${kg_running} == "true" ]]
then
    /home/setup/kg/neo4j-dbpedia-12-2022/bin/neo4j stop
    kg_running="false"
    sleep 1m
fi

if [[ -f "/plots/.Wikitables2013_Wikidata.stats" ]]
then
    command="load"
else
    command="new"
    /home/setup/kg/neo4j-wikidata/bin/neo4j start
    kg_running="true"
    sleep 24h
fi

python3 /home/setup/analysis/analyze_wikitables_wikidata.py ${command}

# Semtab

if [[ -f "/plots/.SemTab.stats" ]]
then
    command="load"
else
    command="new"

    if [[ ${kg_running} == "false" ]]
    then
        /home/setup/kg/neo4j-wikidata/bin/neo4j start
        kg_running="true"
        sleep 24h
    fi
fi

python3 /home/setup/analysis/analyze_semtab.py ${command}

if [[ -f "/plots/.SemTab_BioDivTab-WD.stats" ]]
then
    command="load"
else
    command="new"

    if [[ ${kg_running} == "false" ]]
    then
        /home/setup/kg/neo4j-wikidata/bin/neo4j start
        kg_running="true"
        sleep 24h
    fi
fi

python3 /home/setup/analysis/analyze_semtab_biodivtab_wikidata.py ${command}

# Tough Tables

if [[ -f "/plots/.ToughTables_Wikidata.stats" ]]
then
    command="load"
else
    command="new"

    if [[ ${kg_running} == "false" ]]
    then
        /home/setup/kg/neo4j-wikidata/bin/neo4j start
        kg_running="true"
        sleep 24h
    fi
fi

python3 /home/setup/analysis/analyze_tough_tables_wikidata.py ${command}

if [[ ${kg_running} == "true" ]]
then
    /home/setup/kg/neo4j-wikidata/bin/neo4j stop
    kg_running="false"
    sleep 1m
fi

if [[ -f "/plots/.ToughTables_DBpedia.stats" ]]
then
    command="load"
else
    command="new"
    /home/setup/kg/neo4j-dbpedia-10-2016/bin/neo4j start
    kg_running="true"
    sleep 1h
fi

python3 /home/setup/analysis/analyze_tough_tables_dbpedia.py ${command}

if [[ ${kg_running} == "true" ]]
then
    /home/setup/kg/neo4j-dbpedia-10-2016/bin/neo4j stop
    kg_running="false"
    sleep 1m
fi

# Semtab

if [[ -f "/plots/.SemTab_BioDivTab-DBP.stats" ]]
then
    command="load"
else
    command="new"
    /home/setup/kg/neo4j-dbpedia-03-2022/bin/neo4j start
    kg_running="true"
    sleep 6h
fi

python3 /home/setup/analysis/analyze_semtab_biodivtab_dbpedia.py ${command}

if [[ ${kg_running} == "true" ]]
then
    /home/setup/kg/neo4j-dbpedia-03-2022/bin/neo4j stop
    kg_running="false"
    sleep 1m
fi

# WebDataCommons

if [[ -f "/plots/.WebDataCommons.stats" ]]
then
    command="load"
else
    command="new"
    /home/setup/kg/neo4j-dbpedia-2014/bin/neo4j start
    kg_running="true"
    sleep 6h
fi

python3 /home/setup/analysis/analyze_web_data_commons.py ${command}

if [[ ${kg_runnning} == "true" ]]
then
    /home/setup/kg/neo4j-dbpedia-2014/bin/neo4j stop
    kg_running = "false"
    sleep 1m
fi
