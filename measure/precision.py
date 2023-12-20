import csv
from data import *
import read_results as rr

def _precision(predictions, gt):
    scores = dict()

    for method in predictions.keys():
        results = predictions[method]
        table_group = dict()
        scores[method] = list()

        for result in results:
            table_id = result[0]

            if table_id not in gt.keys():
                continue

            if table_id not in table_group.keys():
                table_group[table_id] = dict()
                table_group[table_id]['predictions'] = 0
                table_group[table_id]['correct'] = 0
                table_group[table_id]['wrong'] = 0

            row = result[1]
            column = result[2]
            prediction = result[3]
            table_group[table_id]['predictions'] += 1

            for truth in gt[table_id]:
                if row == truth[0] and column == truth[1]:
                    gt_entities = truth[2:]

                    if prediction in gt_entities:
                        table_group[table_id]['correct'] += 1

                    else:
                        table_group[table_id]['wrong'] += 1

        for table in table_group.keys():
            precision = table_group[table]['correct'] / table_group[table]['predictions']
            scores[method].append(precision)

    return scores

def write(output_file, results, ground_truth):
    with open(output_file, 'w') as output:
        writer = csv.writer(output, delimiter = ',')
        header = list()
        rows = list()
        precision_results = _precision(results, ground_truth)
        methods = list(precision_results.keys())
        max_results = max([len(precision_results[method]) for method in methods])

        for i in range(max_results):
            row = list()

            for method in methods:
                if i >= len(precision_results[method]):
                    row.append(None)

                else:
                    row.append(precision_results[method][i])

            rows.append(row)

        for method in methods:
            header.append(method)

        writer.writerow(header)

        for row in rows:
            writer.writerow(row)

    return precision_results
