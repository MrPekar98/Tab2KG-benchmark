import csv

def _measure_quality(predictions, gt):
    scores = dict()

    for method in predictions.keys():
        results = predictions[method]
        table_group = dict()
        scores[method] = {'precision': list(), 'recall': list(), 'f1': list()}

        for result in results:
            table_id = result[0]

            if table_id not in gt.keys():
                continue

            elif table_id not in table_group.keys():
                table_group[table_id] = dict()
                table_group[table_id]['predictions'] = 0
                table_group[table_id]['correct'] = 0
                table_group[table_id]['wrong'] = 0
                table_group[table_id]['gt size'] = len(gt[table_id])

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
            recall = table_group[table]['correct'] / table_group[table]['gt size']
            scores[method]['precision'].append(precision)
            scores[method]['recall'].append(recall)

            if precision + recall == 0:
                scores[method]['f1'].append(0.0)

            else:
                f1 = (2 * precision * recall) / (precision + recall)
                scores[method]['f1'].append(f1)

    return scores

def _write(output_file, scores):
    methods = list(scores.keys())
    max_results = max([len(scores[method]['precision']) for method in methods])
    rows_precision = list()
    rows_recall = list()
    rows_f1 = list()

    for i in range(max_results):
        row_precision = list()
        row_recall = list()
        row_f1 = list()

        for method in methods:
            if i >= len(scores[method]['precision']):
                row_precision.append(None)

            else:
                row_precision.append(scores[method]['precision'][i])

            if i >= len(scores[method]['recall']):
                row_recall.append(None)

            else:
                row_recall.append(scores[method]['recall'][i])

            if i >= len(scores[method]['f1']):
                row_f1.append(None)

            else:
                row_f1.append(scores[method]['f1'][i])

        rows_precision.append(row_precision)
        rows_recall.append(row_recall)
        rows_f1.append(row_f1)

    with open(output_file + '_precision.csv', 'w') as output:
        writer = csv.writer(output)
        writer.writerow(methods)

        for row in rows_precision:
            writer.writerow(row)

    with open(output_file + '_recall.csv', 'w') as output:
        writer = csv.writer(output)
        writer.writerow(methods)

        for row in rows_recall:
            writer.writerow(row)

    with open(output_file + '_f1.csv', 'w') as output:
        writer = csv.writer(output)
        writer.writerow(methods)

        for row in rows_f1:
            writer.writerow(row)

def evaluate_quality(base_dir, result_name, predictions, gt):
    results = _measure_quality(predictions, gt)
    _write(base_dir + result_name, results)
