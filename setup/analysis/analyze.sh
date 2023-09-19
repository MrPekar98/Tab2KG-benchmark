#!/bin/bash

set -e

# WikiTables
python3 analyze_wikitables.py

# Tough Tables
python3 analyze_tough_tables.py

# SemTab
analyze_semtab.py

# WebDataCommons
python3 analyze_web_data_commons.py
