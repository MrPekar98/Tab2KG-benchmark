#!/bin/bash

set -e

echo
echo "Evaluating LexMa"

echo
echo "Linking quality experiment"
./quality.sh

echo
echo "Linking scalability experiment"
./scalability.sh

echo
echo "Candidate generation experiment"
./candidates.sh

echo
echo "No entity recognition experiment"
./non_rec_quality.sh
