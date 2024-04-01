#!/bin/bash

set -e

count_existence()
{
    FILE=$1
    COUNT=0

    while read -r ENTITY;
    do
        RES=$(curl http://localhost:7000/exists&entity=${ENTITY})

        if [[ ${RES} == "True" ]]
        then
            COUNT=$((${COUNT} + 1))
        fi
    done < ${FILE}

    return ${COUNT}
}

# Tough Tables - DBpedia
docker run --rm -d --network kg-lookup-network \
           -v ${PWD}/../../baselines/magic/lucene_dbp_2016/:/lucene \
           -v ${PWD}/../tough_tables/dbpedia/:/kg \
           -p 7000:7000 \
           -e MEM=200g \
           -e GRAPH=dbp_2016 \
           -e VIRTUOSO='none' \
           --name kg-lookup-service kg-lookup
sleep 1m

count_existence ${TT_DBP_ENTS_UNI}
COUNT=$?
TOTAL=$(cat ${TT_DBP_ENTS_UNI} | wc -l)
echo "ToughTables - DBpedia: ${COUNT}/${TOTAL}"

docker stop kg-lookup-service

# Wikitables 2013 - DBpedia
docker run --rm -d --network kg-lookup-network \
           -v ${PWD}../../baselines/magic/lucene_dbp_2022/:/lucene \
           -v ${PWD}/../kg/dbpedia/:/kg \
           -p 7000:7000 \
           -e MEM=200g \
           -e GRAPH=dbp_2016 \
           -e VIRTUOSO='none' \
           --name kg-lookup-service kg-lookup
sleep 1m

count_existence ${WT_2013_DBP_ENTS_UNI}
COUNT=$?
TOTAL=$(cat ${WT_2013_DBP_ENTS_UNI} | wc -l)
echo "Wikitables 2013 - DBpedia: ${COUNT}/${TOTAL}"

# Wikitables 2019 - DBpedia
count_existence ${WT_2019_DBP_ENTS_UNI}
COUNT=$?
TOTAL=$(cat ${WT_2019_DBP_ENTS_UNI} | wc -l)
echo "Wikitables 2019 - DBpedia: ${COUNT}/${TOTAL}"

docker stop kg-lookup-service

# ToughTables - Wikidata
docker run --rm -d --network kg-lookup-network \
           -v ${PWD}/../../baselines/lexma/lucene_wd/:/lucene \
           -v ${PWD}/../tough_tables/wikidata/:/kg \
           -p 7000:7000 \
           -e MEM=200g \
           -e GRAPH=wd \
           -e VIRTUOSO='none' \
           --name kg-lookup-service kg-lookup
sleep 1m

count_existence ${TT_WD_ENTS_UNI}
COUNT$?
TOTAL=$(cat ${TT_WD_ENTS_UNI} | wc -l)
echo "ToughTables - Wikidata: ${COUNT}/${TOTAL}"

# HardTables
count_existence ${HT_ENTS_UNI}
COUNT=$?
TOTAL=$(cat ${HT_ENTS_UNI} | wc -l)
echo "HardTables: ${COUNT}/${TOTAL}"

# tFood
count_existence ${TF_ENTS_UNI}
COUNT=$?
TOTAL=$(cat ${TF_ENTS_UNI} | wc -l)
echo "tFood: ${COUNT}/${TOTAL}"

# Wikitables 2013 - Wikidata
count_existence ${WT_2013_WD_ENTS_UNI}
COUNT=$?
TOTAL=$(cat ${WT_2013_WD_ENTS_UNI} | wc -l)
echo "Wikitables 2013 - Wikidata: ${COUNT}/${TOTAL}"

# Wikitables 2019 - Wikidata
count_existence ${WT_2019_WD_ENTS_UNI}
COUNT=$?
TOTAL=$(cat ${WT_2019_WD_ENTS_UNI} | wc -l)
echo "Wikitables 2019 - Wikidata: ${COUNT}/${TOTAL}"

docker stop kg-lookup-service
