#!/bin/bash

set -e

KG=$1

if [[ ! -d keyword-kg-linker ]]
then
    git clone https://github.com/MrPekar98/keyword-kg-linker.git
    rm keyword-kg-linker/config.json
    mv keyword-kg-linker/* .
fi

# TODO: Start indexing for each KG
