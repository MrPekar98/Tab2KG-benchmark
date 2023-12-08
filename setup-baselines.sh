#!/bin/bash

set -e

HOME=${PWD}
NETWORK="evaluation"

BBW="baselines/bbw/"
T2KMATCH="baselines/t2kmatch/"
KEYWORD_KG_LINKER="baselines/keyword-kg-linker/"
LEXMA="baselines/lexma/"
EMBLOOKUP="baselines/emblookup/"
MAGIC="baselines/magic/"

mkdir -p results/
mkdir -p results/bbw/
mkdir -p results/emblookup/
mkdir -p results/keyword-kg-linker/
mkdir -p results/lexma/
mkdir -p results/t2kmatch/
mkdir -p results/magic/

docker pull searx/searx
docker network inspect ${NETWORK} >/dev/null 2>&1 || docker network create ${NETWORK}

docker build -t bbw -f ${BBW}bbw.dockerfile ${BBW}
docker build -t spotlight_dbp-10-2016 -f ${MAGIC}spotlight.dockerfile --build-arg KG="dbp-10-2016" ${MAGIC}
docker build -t spotlight_dbp-03-2022 -f ${MAGIC}spotlight.dockerfile --build-arg KG="dbp-03-2022" ${MAGIC}
docker build -t magic_dbp-10-2016 -f ${MAGIC}magic.dockerfile --build-arg KG="dbp-10-2016" ${MAGIC}
docker build -t magic_dbp-03-2022 -f ${MAGIC}magic.dockerfile --build-arg KG="dbp-03-2022" ${MAGIC}
docker build -t magic_wd -f ${MAGIC}magic.dockerfile --build-arg KG="wd" ${MAGIC}
docker build -t t2kmatch -f ${T2KMATCH}t2kmatch.dockerfile ${T2KMATCH}
docker build -t lexma -f ${LEXMA}lexma.dockerfile ${LEXMA}
docker build -t emblookup -f ${EMBLOOKUP}emblookup.dockerfile ${EMBLOOKUP}

# Setup
# Keyword-kg-linker
#cd ${KEYWORD_KG_LINKER}
#./setup.sh
#cd ${HOME}

# TODO: Setup the other baselines
