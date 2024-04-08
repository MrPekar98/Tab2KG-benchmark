import sys
import shutil
import os

subset_size = int(sys.argv[1])
benchmark_dir = sys.argv[2]
table_dir = benchmark_dir + '/tables/'
output_table_dir = benchmark_dir + 'tables_subset/'
tables = list(os.listdir(table_dir))

if not os.path.exists(output_table_dir):
    os.mkdir(output_table_dir)

for i in range(subset_size):
    print(i, ':', table_dir + tables[i], '->', output_table_dir + tables[i])
    shutil.copyfile(table_dir + tables[i], output_table_dir + tables[i])
