#!/bin/bash

set -e

# TODO: Create multiple experiment files, one for each KG.
# So, the quality experiment should have 3 scripts so it can run all experiments for those using the same KG.

KG=$1

echo
echo "Evaluating Magic"

echo
echo "Linking quality experiment"
./quality.sh ${KG}
