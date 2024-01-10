#!/bin/bash

set -e

echo
echo "Evaluating bbw"

echo
echo "Linking quality experiment"
./quality.sh

echo
echo "Linkin scalability experiment"
./scalability.sh
