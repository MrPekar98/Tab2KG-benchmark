#!/bin/bash

set -e

TABLES=$1

if [[ ! -d ${TABLES} ]]
then
    echo "Directory '${TABLES}' does not exist"
    exit 1
fi

JAR="target/t2kmatch-2.1-jar-with-dependencies.jar"
CP="de.uni_mannheim.informatik.dws.t2k.match.T2KMatch"
KB="data/dbpedia/"
ONTOLOGY="data/OntologyDBpedia"
INDEX="data/index/"
RESULTS="/results/TK2Match/"

mkdir -p ${RESULTS}
java -cp ${JAR} ${CP} -sf ${SF} -kb ${KB} -ontology ${ONTOLOGY} \
    -web ${TABLES} -index ${INDEX} -results ${RESULTS} -verbose
