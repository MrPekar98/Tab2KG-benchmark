import os
import csv

def linked_tables(dir, method, name, avg_table_size):
    print(method)
    print(name)

    if method == 'MAGIC':
        print((len(os.listdir(dir)) / 3) / avg_table_size)

    else:
        print(len(os.listdir(dir)) / avg_table_size)

def linked_tables_emblookup(file, method, name, avg_table_size):
    tables = set()
    print(method)
    print(name)

    with open(file, 'r') as handle:
        reader = csv.reader(handle)

        for row in reader:
            tables.add(row[0])

    print(len(tables) / avg_table_size)

def magic_linked_cells(dir):
    files = os.listdir(dir)
    lines = 0

    for file in files:
        if not 'cea' in file:
            continue

        with open(dir + file, 'r') as handle:
            for row in handle:
                lines += 1

    return lines

def lexma_linked_cells(dir):
    files = os.listdir(dir)
    lines = 0

    for file in files:
        with open(dir + file, 'r') as handle:
            for row in handle:
                lines += 1

    return lines

def bbw_linked_cells(dir):
    return lexma_linked_cells(dir)

def emblookup_linked_cells(links_file):
    lines = 0

    with open(links_file, 'r') as handle:
        for line in handle:
            lines += 1

    return lines
