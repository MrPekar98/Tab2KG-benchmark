import csv

# Only consider ground truth for tables that have been processed by the entity linker
def _filter_gt(gt, predictions):
    filtered_gt = dict()
    processed_tables = set()

    for result in predictions:
        processed_tables.add(result[0])

    for table_id in gt.keys():
        if table_id in processed_tables:
            filtered_gt[table_id] = gt[table_id]

    return filtered_gt

# Measures all metrics as a single value across all tables
def _measure_quality(predictions, gt):
    gt_per_method = dict()
    method_gt_cell_ent = dict()

    for method in predictions.keys():
        gt_per_method[method] = _filter_gt(gt, predictions[method])
        method_gt_cell_ent[method] = dict()

        for table_id in gt_per_method[method].keys():
            for gt_cell in gt_per_method[method][table_id]:
                cell = '%s %s %s' % (table_id, gt_cell[0], gt_cell[1])
                method_gt_cell_ent[method][cell] = gt_cell[2:]

    scores = dict()

    for method in predictions.keys():
        correct_cells, annotated_cells = set(), set()
        results = predictions[method]

        for result in results:
            result_table_id = result[0]
            result_row = result[1]
            result_column = result[2]
            annotation = result[3].lower()
            result_cell = '%s %s %s' % (result_table_id, result_row, result_column)

            if result_cell in method_gt_cell_ent[method]:
                """if result_cell in annotated_cells:
                    raise Exception("Duplicate cells in the submission file")

                else:
                    annotated_cells.add(result_cell)"""

                annotated_cells.add(result_cell)

                if not annotation:
                    if method_gt_cell_ent[method][result_cell] == 'nil':
                        correct_cells.add(result_cell)

                else:
                    if annotation in method_gt_cell_ent[method][result_cell]:
                        correct_cells.add(result_cell)

        precision = len(correct_cells) / len(annotated_cells) if len(annotated_cells) > 0 else 0.0
        recall = len(correct_cells) / len(method_gt_cell_ent[method].keys())
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        scores[method] = {'precision': precision, 'recall': recall, 'f1': f1}

    return scores

def evaluate_quality(base_dir, result_name, predictions, gt):
    scores = _measure_quality(predictions, gt)
    print(result_name)

    for method in scores.keys():
        print(method)
        print('Precision:', scores[method]['precision'])
        print('Recall:', scores[method]['recall'])
        print('F1-score:', scores[method]['f1'], '\n')
