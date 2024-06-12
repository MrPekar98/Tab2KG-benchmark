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
