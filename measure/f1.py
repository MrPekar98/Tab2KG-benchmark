import csv
from data import *
import read_results as rr

# It assumes both precision_results and recall_results contains the exact same methods and number of results, and that each result corresponds to the same table across the two variables
def write(output_file, precision_results, recall_results):
    with open(output_file, 'w') as output_file:
        writer = csv.writer(output_file, delimiter = ',')
        result_count = len(precision_results[list(precision_results.keys())[0]])
        writer.writerow([method for method in precision_results.keys()])

        for i in range(result_count):
            row = list()

            for method in precision_results.keys():
                pre = precision_results[method][i]
                rec = recall_results[method][i]

                if pre + rec == 0:
                    row.append(0.0)

                else:
                    row.append((2 * pre * rec) / (pre + rec))

            writer.writerow(row)
