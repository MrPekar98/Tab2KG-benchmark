def identifiability(predictions, gt):
    results = dict()
    cells = dict()
    target_cell_count = 0

    for table in gt.keys():
        cells[table] = set()

        for cell in gt[table]:
            row = cell[0]
            column = cell[1]
            cells[table].add((row, column))
            target_cell_count += 1

    for method in predictions.keys():
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
        recall = correct / target_cell_count
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        results[method] = {'precision': precision, 'recall': recall, 'f1': f1}

    return results
