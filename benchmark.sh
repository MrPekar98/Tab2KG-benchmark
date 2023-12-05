#!/bin/bash

set -e

# Keyword-kg-linker

# bbw
#docker run --rm -d -v ${PWD}/searx:/etc/searx --network evaluation --name searx -e BASE_URL=http://localhost:3030/ searx/searx
#docker run --rm --network evaluation -v ${PWD}/benchmarks:/benchmarks -v ${PWD}/results:/results bbw
#docker stop searx

# EmbLookup
#docker run --rm -v ${PWD}/benchmarks:/benchmarks -v ${PWD}/results:/results emblookup

# Magic
docker run --rm --network evaluation -d --name dbpedia-spotlight spotlight_dbp-10-2016
docker run --rm --network evaluation -v ${PWD}/benchmarks:/benchmarks -v ${PWD}/results:/results magic_dbp-10-2016
docker stop dbpedia-spotlight

docker run --rm --network evaluation -d --name dbpedia-spotlight spotlight_dbp-03-2022
docker run --rm --network evaluation -v ${PWD}/benchmarks:/benchmarks -v ${PWD}/results:/results magic_dbp-03-2022
docker stop dbpedia-spotlight

docker run --rm --network evaluation -v ${PWD}/benchmarks:/benchmarks -v ${PWD}/results:/results magic_wd

# T2K Match

# LexMa
