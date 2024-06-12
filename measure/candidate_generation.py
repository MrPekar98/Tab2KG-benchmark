import filter_ground_truth as fgt

# Measures the hit rate of candidate generation results
def evaluate_candidate_generation(candidates, gt):
    hit_rate = dict()

    for method in candidates.keys():
        filtered_gt = fgt.filter_gt(gt, candidates[method])
        gt_cells = dict()

        for table_id in filtered_gt.keys():
            for gt_cell in filtered_gt[table_id]:
                cell = '%s %s %s' % (table_id, gt_cell[0], gt_cell[1])
                gt_cells[cell] = gt_cell[2:]

        hits, misses = 0, 0
        results = candidates[method]

        for result in results:
            result_table_id = result[0]
            result_row = result[1]
            result_column = result[2]
            candidate_set = result[3]
            result_cell = '%s %s %s' % (result_table_id, result_row, result_column)

            if result_cell in gt_cells:
                found_hit = False

                for candidate in candidate_set:
                    if candidate in gt_cells[result_cell]:
                        hits += 1
                        found_hit = True
                        break

                if not found_hit:
                    misses += 1

        hit_rate[method] = hits / (hits + misses)

    return hit_rate
