#!/bin/bash

set -e

write_existence()
{
    FILE=$1
    KG=$2
    PREFIX=$3
    echo "" > .exists
    echo "" > .not_exists

    while read -r line;
    do
        ENTITY=${line}
        ASK=$(python3 entity_exists.py "${PREFIX}${ENTITY}" "http://localhost:8890/${KG}" "${VIRTUOSO_URL}")

        if [[ "${ASK}" == "True" ]]
        then
            echo "${ENTITY}" >> .exists
        else
            echo "${ENTITY}" >> .not_exists
        fi
    done < ${FILE}
}

# Tough Tables - DBpedia
write_existence ${TT_DBP_ENTS_UNI} dbp_2016 "http://dbpedia.org/resource/"

TT_DBP_EXISTS=$(cat .exists | wc -l)
TT_DBP_NOT_EXISTS=$(cat .not_exists | wc -l)

# Tough Tables - Wikidata
write_existence ${TT_WD_ENTS_UNI} wd "http://www.wikidata.org/entity/"

TT_WD_EXISTS=$(cat .exists | wc -l)
TT_WD_NOT_EXISTS=$(cat .not_exists | wc -l)

# HardTables
write_existence ${HT_ENTS_UNI} wd "http://www.wikidata.org/entity/"

HT_EXISTS=$(cat .exists | wc -l)
HT_NOT_EXISTS=$(cat .not_exists | wc -l)

# tFood
write_existence ${TF_ENTS_UNI} wd "http://www.wikidata.org/entity/"

TF_EXISTS=$(cat .exists | wc -l)
TF_NOT_EXISTS=$(cat .not_exists | wc -l)

# Wikitables 2013 - DBpedia
write_existence ${WT_2013_DBP_ENTS_UNI} dbp_2022 "http://dbpedia.org/resource/"

WT_2013_DBP_EXISTS=$(cat .exists | wc -l)
WT_2013_DBP_NOT_EXISTS=$(cat .not_exists | wc -l)

# Wikitables 2013 - Wikidata
write_existence ${WT_2013_WD_ENTS_UNI} wd "http://www.wikidata.org/entity/"

WT_2O13_WD_EXISTS=$(cat .exists | wc -l)
WT_2013_WD_NOT_EXISTS=$(cat .not_exists | wc -l)

# Wikitables 2019 - DBpedia
write_existence ${WT_2019_DBP_ENTS_UNI} dbp_2022 "http://dbpedia.org/resource/"

WT_2019_DBP_EXISTS=$(cat .exists | wc -l)
WT_2019_DBP_NOT_EXISTS=$(cat .not_exists | wc -l)

# Wikitables 2019 - Wikidata
write_existence ${WT_2019_WD_ENTS_UNI} wd "http://www.wikidata.org/entity/"

WT_2019_WD_EXISTS=$(cat .exists | wc -l)
WT_2019_WD_NOT_EXISTS=$(cat .not_exists | wc -l)

rm .exists .not_exists

# Print the existence stats
echo "Tough Tables - DBpedia: ${TT_DBP_EXISTS}/$(cat ${TT_DBP_ENTS_UNI} | wc -l)"
echo "Tough Tables - Wikidata: ${TT_WD_EXISTS}/$(cat ${TT_WD_ENTS_UNI} | wc -l)"
echo "HardTables: ${HT_EXISTS}/$(cat ${HT_ENTS_UNI} | wc -l)"
echo "tFood: ${TF_EXISTS}/$(cat ${TF_ENTS_UNI} | wc -l)"
echo "Wikitables 2013 - DBpedia: ${WT_2013_DBP_EXISTS}/$(cat ${WT_2013_WD_ENTS_UNI} | wc -l)"
echo "Wikitables 2013 - Wikidata: ${WT_2O13_WD_EXISTS}/$(cat ${WT_2013_WD_ENTS_UNI} | wc -l)"
echo "Wikitables 2019 - DBpedia: ${WT_2019_DBP_EXISTS}/$(cat ${WT_2019_DBP_ENTS_UNI} | wc -l)"
echo "Wikitables 2019 - Wikidata: ${WT_2019_WD_EXISTS}/$(cat ${WT_2019_WD_ENTS_UNI} | wc -l)"
