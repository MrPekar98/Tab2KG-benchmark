import os
import csv

def linked_tables(dir, method, name, avg_table_size):
    print(method)
    print(name)
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
