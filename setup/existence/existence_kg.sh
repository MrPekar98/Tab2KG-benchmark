#!/bin/bash

set -e

# TODO: Remove ground truth entities that do not exist in the KG

# Generate files of ground truth entities
echo "Processing ground truth and KG files..."

TT_DBP_ENTS_DUP=".toughtables_dbp_entities_duplicates.tmp"

if [[ ! -f ${TT_DBP_ENTS_UNI} ]]
then
    while read -r line;
    do
        ENTITIES=$(echo ${line} | cut -d "," -f 4)
        ENTITY=$(echo ${ENTITIES} | cut -d " " -f 1)

        if [[ ${ENTITY:0:1} == '"' ]]
        then
            ENTITY=${ENTITY:1}
        fi

        if [[ ${ENTITY: -1} == '"' ]]
        then
            ENTITY=${ENTITY:0:-1}
        fi

        TOKENS=${ENTITY//// }
        echo ${TOKENS[-1]} >> ${TT_DBP_ENTS_DUP}
    done < ${TOUGHTABLES_GT_DBP}

    sort ${TT_DBP_ENTS_DUP} | uniq > ${TT_DBP_ENTS_UNI}
    rm ${TT_DBP_ENTS_DUP}
fi

TT_WD_ENTS_DUP=".toughtables_wd_entities_duplicates.tmp"

if [[ ! -f ${TT_WD_ENTS_UNI} ]]
then
    while read -r line;
    do
        ENTITIES=$(echo ${line} | awk -F ',' '{print $4}')
        ENTITY=$(echo ${ENTITIES} | awk -F ' ' '{print $1}')

        if [[ ${ENTITY: -1} == '"' ]]
        then
            ENTITY=${ENTITY:1:-1}
        else
            ENTITY=${ENTITY:1}
        fi

        TOKENS=${ENTITY//// }
        echo ${TOKENS[-1]} >> ${TT_WD_ENTS_DUP}
    done < ${TOUGHTABLES_GT_WD}

    sort ${TT_WD_ENTS_DUP} | uniq > ${TT_WD_ENTS_UNI}
    rm ${TT_WD_ENTS_DUP}
fi

HT_ENTS_DUP=".hardtables_entities_duplicates.tmp"

if [[ ! -f ${HT_ENTS_UNI} ]]
then
    while read -r line;
    do
        ENTITY=$(echo ${line} | awk -F ',' '{print $4}')
        TOKENS=${ENTITY//// }
        echo ${TOKENS[-1]} >> ${HT_ENTS_DUP}
    done < ${HARDTABLES_GT}

    sort ${HT_ENTS_DUP} | uniq > ${HT_ENTS_UNI}
    rm ${HT_ENTS_DUP}
fi

TF_ENTS_DUP=".tfood_entities_duplicates.tmp"

if [[ ! -f ${TF_ENTS_UNI} ]]
then
    while read -r line;
    do
        ENTITY=$(echo ${line} | cut -d "," -f 4)

        if [[ ${ENTITY:0:1} == '"' ]]
        then
            ENTITY=${ENTITY:1}
        fi

        TOKENS=${ENTITY//// }
        echo ${TOKENS[-1]} >> ${TF_ENTS_DUP}
    done < ${TFOOD_GT}

    sort ${TF_ENTS_DUP} | uniq > ${TF_ENTS_UNI}
    rm ${TF_ENTS_DUP}
fi

WT_2013_DBP_ENTS_DUP=".wikitables_2013_dbp_entities_duplicates.tmp"

if [[ ! -f ${WT_2013_DBP_ENTS_UNI} ]]
then
    while read -r line;
    do
        ENTITY=$(echo ${line} | cut -d "," -f 4)

        if [[ ${ENTITY:0:1} == '"' ]]
        then
            ENTITY=${ENTITY:1}
        fi

        TOKENS=${ENTITY//// }
        echo ${TOKENS[-1]} >> ${WT_2013_DBP_ENTS_DUP}
    done < ${WIKITABLES_2013_DBP}

    sort ${WT_2013_DBP_ENTS_DUP} | uniq > ${WT_2013_DBP_ENTS_UNI}
    rm ${WT_2013_DBP_ENTS_DUP}
fi

WT_2013_WD_ENTS_DUP=".wikitables_2013_wd_entities_duplicates.tmp"

if [[ ! -f ${WT_2013_WD_ENTS_UNI} ]]
then
    while read -r line;
    do
        ENTITY=$(echo ${line} | cut -d "," -f 4)
        TOKENS=${ENTITY//// }
        echo ${TOKENS[-1]} >> ${WT_2013_WD_ENTS_DUP}
    done < ${WIKITABLES_2013_WD}

    sort ${WT_2013_WD_ENTS_DUP} | uniq > ${WT_2013_WD_ENTS_UNI}
    rm ${WT_2013_WD_ENTS_DUP}
fi

WT_2019_DBP_ENTS_DUP=".wikitables_2019_dbp_entities_duplicates.tmp"

if [[ ! -f ${WT_2019_DBP_ENTS_UNI} ]]
then
    while read -r line;
    do
        ENTITY=$(echo ${line} | cut -d "," -f 4)

        if [[ ${ENTITY:0:1} == '"' ]]
        then
            ENTITY=${ENTITY:1}
        fi

        TOKENS=${ENTITY//// }
        echo ${TOKENS[-1]} >> ${WT_2019_DBP_ENTS_DUP}
    done < ${WIKITABLES_2019_DBP}

    sort ${WT_2019_DBP_ENTS_DUP} | uniq > ${WT_2019_DBP_ENTS_UNI}
    rm ${WT_2019_DBP_ENTS_DUP}
fi

WT_2019_WD_ENTS_DUP=".wikitables_2019_wd_entities_duplicates.tmp"

if [[ ! -f ${WT_2019_WD_ENTS_UNI} ]]
then
    while read -r line;
    do
        ENTITY=$(echo ${line} | cut -d "," -f 4)
        TOKENS=${ENTITY//// }
        echo ${TOKENS[-1]} >> ${WT_2019_WD_ENTS_DUP}
    done < ${WIKITABLES_2019_WD}

    sort ${WT_2019_WD_ENTS_DUP} | uniq > ${WT_2019_WD_ENTS_UNI}
    rm ${WT_2019_WD_ENTS_DUP}
fi

DBP_2016_ENTS_DUP=".dbpedia_2016_entities_duplicates.tmp"

if [[ ! -f ${DBP_2016_ENTS_UNI} ]]
then
    for FILE in ${DBP_2016}*;
    do
        while read -r line;
        do
            if [[ ! ${line} =~ "#" ]]
            then
                SUBJECT=$(echo ${line} | cut -d " " -f 1)
                ENTITY=${SUBJECT:1:-1}
                TOKENS=${ENTITY//// }
                echo ${TOKENS[-1]} >> ${DBP_2016_ENTS_DUP}
            fi
        done < ${FILE}
    done

    sort ${DBP_2016_ENTS_DUP} | uniq > ${DBP_2016_ENTS_UNI}
    rm ${DBP_2016_ENTS_DUP}
fi

DBP_2022_ENTS_DUP=".dbpedia_2022_entities_duplicates.tmp"

if [[ ! -f ${DBP_2022_ENTS_UNI} ]]
then
    for FILE in ${DBP_2022}*;
    do
        while read -r line;
        do
            if [[ ! ${line} =~ "#" ]]
            then
                SUBJECT=$(echo ${line} | cut -d " " -f 1)
                ENTITY=${SUBJECT:1:-1}
                TOKENS=${ENTITY//// }
                echo ${TOKENS[-1]} >> ${DBP_2022_ENTS_DUP}
            fi
        done < ${FILE}
    done

    sort ${DBP_2022_ENTS_DUP} | uniq > ${DBP_2022_ENTS_UNI}
    rm ${DBP_2022_ENTS_DUP}
fi

WD_ENTS_DUP=".wikidata_entities_duplicates.tmp"

if [[ ! -f ${WD_ENTS_UNI} ]]
then
    for FILE in ${WD}*;
    do
        while read -r line;
        do
            if [[ ! ${line:0:2} =~ "#" ]]
            then
                SUBJECT=$(echo ${line} | cut -d " " -f 1)
                ENTITY=${SUBJECT:1:-1}
                TOKENS=${ENTITY//// }
                echo ${TOKENS[-1]} >> ${WD_ENTS_DUP}
            fi
        done < ${FILE}
    done

    sort ${WD_ENTS_DUP} | uniq > ${WD_ENTS_UNI}
    rm ${WD_ENTS_DUP}
fi

echo "Done"
echo

# ToughTables - DBpedia 10-2016
ENTITIES=$(cat ${TT_DBP_ENTS_UNI} | wc -l)
EXISTS=$((${ENTITIES} - $(python3 non_exists.py ${TT_DBP_ENTS_UNI} ${DBP_2016_ENTS_UNI} | wc -l)))
echo "ToughTables - DBpedia: ${EXISTS}/${ENTITIES}"

# ToughTables - Wikidata
ENTITIES=$(cat ${TT_WD_ENTS_UNI} | wc -l)
EXISTS=$((${ENTITIES} - $(python3 non_exists.py ${TT_WD_ENTS_UNI} ${WD_ENTS_UNI} | wc -l)))
echo "ToughTables - Wikidata: ${EXISTS}/${ENTITIES}"

# HardTables - Wikidata
ENTITIES=$(cat ${HT_ENTS_UNI} | wc -l)
EXISTS=$((${ENTITIES} - $(python3 non_exists.py ${HT_ENTS_UNI} ${WD_ENTS_UNI} | wc -l)))
echo "HardTables: ${EXISTS}/${ENTITIES}"

# tFood - Wikidata
ENTITIES=$(cat ${TF_ENTS_UNI} | wc -l)
EXISTS=$((${ENTITIES} - $(python3 non_exists.py ${TF_ENTS_UNI} ${WD_ENTS_UNI} | wc -l)))
echo "tFood: ${EXISTS}/${ENTITIES}"

# WikiTables 2013 - DBpedia 12-2022
ENTITIES=$(cat ${WT_2013_DBP_ENTS_UNI} | wc -l)
EXISTS=$((${ENTITIES} - $(python3 non_exists.py ${WT_2013_DBP_ENTS_UNI} ${DBP_2022_ENTS_UNI} | wc -l)))
echo "WikiTables 2013 - DBpedia: ${EXISTS}/${ENTITIES}"

# WikiTables 2013 - Wikidata
ENTITIES=$(cat ${WT_2013_WD_ENTS_UNI} | wc -l)
EXISTS=$((${ENTITIES} - $(python3 non_exists.py ${WT_2013_WD_ENTS_UNI} ${WD_ENTS_UNI} | wc -l)))
echo "WikiTables 2013 - Wikidata: ${EXISTS}/${ENTITIES}"

# WikiTables 2019 - DBpedia 12-2022
ENTITIES=$(cat ${WT_2019_DBP_ENTS_UNI} | wc -l)
EXISTS=$((${ENTITIES} - $(python3 non_exists.py ${WT_2019_DBP_ENTS_UNI} ${DBP_2022_ENTS_UNI} | wc -l)))
echo "WikiTables 2019 - DBpedia: ${EXISTS}/${ENTITIES}"

# WikiTables 2019 - Wikidata
ENTITIES=$(cat ${WT_2019_WD_ENTS_UNI} | wc -l)
EXISTS=$((${ENTITIES} - $(python3 non_exists.py ${WT_2019_WD_ENTS_UNI} ${WD_ENTS_UNI} | wc -l)))
echo "WikiTables 2019 - Wikidata: ${EXISTS}/${ENTITIES}"
echo
