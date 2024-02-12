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
