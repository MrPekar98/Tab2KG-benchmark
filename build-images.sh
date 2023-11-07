#!/bin/bash

set -e

BBW="baselines/bbw/"
T2KMATCH="baselines/t2kmatch/"
KEYWORD_KG_LINKER="baselines/keyword-kg-linker/"
LEXMA="baselines/lexma/"
EMBLOOKUP="baselines/emblookup/"

docker build -t tab2kg_benchmark -f evaluate.dockerfile .

docker build -t bbw -f ${BBW}bbw.dockerfile ${BBW}
docker build -t t2kmatch -f ${T2KMATCH}t2kmatch.dockerfile ${T2KMATCH}
docker build -t keyword-kg-linker -f ${KEYWORD_KG_LINKER}keyword-kg-linker.dockerfile ${KEYWORD_KG_LINKER}
docker build -t lexma -f ${LEXMA}lexma.dockerfile ${LEXMA}
docker build -t emblookup -f ${EMBLOOKUP}emblookup.dockerfile ${EMBLOOKUP}
