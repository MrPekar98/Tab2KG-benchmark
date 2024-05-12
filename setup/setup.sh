#!/bin/bash

set -e

echo
echo "Installing Neo4J"
./kg/install.sh
mkdir tmp
mv neo4j-server tmp
cp -r tmp/neo4j-server .
mv neo4j-server kg/neo4j-dbpedia-12-2022
cp -r tmp/neo4j-server .
mv neo4j-server kg/neo4j-dbpedia-10-2016
cp -r tmp/neo4j-server .
mv neo4j-server kg/neo4j-wikidata
rm -rf tmp

echo "dbms.memory.heap.initial_size=50g" >> kg/neo4j-dbpedia-12-2022/conf/neo4j.conf
echo "dbms.memory.heap.max_size=150g" >> kg/neo4j-dbpedia-12-2022/conf/neo4j.conf
echo "dbms.memory.heap.initial_size=50g" >> kg/neo4j-dbpedia-10-2016/conf/neo4j.conf
echo "dbms.memory.heap.max_size=150g" >> kg/neo4j-dbpedia-10-2016/conf/neo4j.conf
echo "dbms.memory.heap.initial_size=50g" >> kg/neo4j-wikidata/conf/neo4j.conf
echo "dbms.memory.heap.max_size=150g" >> kg/neo4j-wikidata/conf/neo4j.conf

echo
echo "Setting up benchmark"
echo
echo "Downloading benchmarks"
./download_benchmarks.sh

echo
echo "Processing benchmarks"
./process_benchmarks.sh

echo
echo "Setting up baselines"
./setup_baselines.sh

echo
echo "Done"
