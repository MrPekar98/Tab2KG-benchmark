#!/bin/bash

set -e

# Keyword-kg-linker

# bbw
docker run --rm -d -v ${PWD}/searx:/etc/searx --network evaluation --name searx -e BASE_URL=http://localhost:3030/ searx/searx
docker run --rm --network evaluation -v ${PWD}/benchmarks:/benchmarks -v ${PWD}/results:/results bbw
docker stop searx

# EmbLookup
#docker run --rm -v ${PWD}/benchmarks:/benchmarks -v ${PWD}/results:/results emblookup

# T2K Match

# LexMa
