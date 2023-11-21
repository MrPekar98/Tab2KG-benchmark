#!/bin/bash

set -e

NEO4J_HOME=$1

if [ ! -d ${NEO4J_HOME} ] ;\
then
    echo "Neo4J directory '${NEO4J_HOME}' does not exist"
    exit 1
fi

sleep 30s

while [ "$(tail -n 1 ${NEO4J_HOME}/logs/neo4j.log | cut -c 36-42)" != "Started" ] ;\
do
    sleep 10s
done
