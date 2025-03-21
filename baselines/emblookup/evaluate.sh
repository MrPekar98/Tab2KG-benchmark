#!/bin/bash

set -e

echo
echo "Evaluating EmbLookup"

echo
echo "Linking quality experiment"
./quality.sh

echo
echo "Linking scalability experiment"
./scalability.sh

echo
echo "Candidate generation experiment"
./candidates.sh
