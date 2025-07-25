#!/bin/bash

set -e

echo
echo "Evaluating CitySTI"

echo
echo "Linking quality experiment"
./quality.sh

echo
echo "Candidate generation experiment"
./candidates.sh
