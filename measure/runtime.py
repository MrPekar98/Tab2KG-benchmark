import os
import csv

def linked_tables(dir, method, name):
    print(method)
    print(name)
    print(len(os.listdir(dir)))

def linked_tables_emblookup(file, method, name):
    tables = set()
    print(method)
    print(name)

    with open(file, 'r') as handle:
        reader = csv.reader(handle)

        for row in reader:
            tables.add(row[0])

    print(len(tables))
