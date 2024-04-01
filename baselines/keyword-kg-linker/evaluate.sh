#!/bin/bash

set -e

echo
echo "Evaluating keyword-kg-linker"

echo
echo "Linking quality experiment"
./experiments/quality.sh

echo
echo "Linking scalability experiment"
./experiments/scalability.sh
