# Only consider ground truth for tables that have been processed by the entity linker
def filter_gt(gt, predictions):
    filtered_gt = dict()
    processed_tables = set()

    for result in predictions:
        processed_tables.add(result[0])

    for table_id in gt.keys():
        if table_id in processed_tables:
            filtered_gt[table_id] = gt[table_id]

    return filtered_gt

def filter_gt_cells(gt, entity_cells):
    filtered_gt = dict()

    for table_id in entity_cells.keys():
        for annotation in gt[table_id]:
            if (annotation[0], annotation[1]) in entity_cells[table_id]:
                if not table_id in filtered_gt:
                    filtered_gt[table_id] = list()

                filtered_gt[table_id].append(annotation)

    return filtered_gt

def filter_prediction_cells(predictions, entity_cells):
    filtered = dict()

    for method in predictions.keys():
        method_filtered = list()

        for prediction in predictions[method]:
            cell = (prediction[1], prediction[2])
            table_id = prediction[0]

            if cell in entity_cells[table_id]:
                method_filtered.append(prediction)

        filtered[method] = method_filtered

    return filtered
