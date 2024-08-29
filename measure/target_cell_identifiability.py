import filter_ground_truth as fgt

def identifiability(predictions, gt):
    method_gt_cells = dict()
    results = dict()

    for method in predictions.keys():
        method_gt = fgt.filter_gt(gt, predictions[method])
        method_gt_cells[method] = 0
        cells = dict()

        for table_id in method_gt.keys():
            cells[table_id] = set()

            for cell in method_gt[table_id]:
                method_gt_cells[method] += 1
                row = cell[0]
                column = cell[1]
                cells[table_id].add((row, column))

        total = 0
        correct = 0

        for prediction in predictions[method]:
            table = prediction[0]
            row = prediction[1]
            column = prediction[2]
            total += 1

            if table in cells.keys() and (row, column) in cells[table]:
                correct += 1

        precision = correct / total if total > 0 else 0.0
        recall = correct / method_gt_cells[method]
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        results[method] = {'precision': precision, 'recall': recall, 'f1': f1}

    return results
