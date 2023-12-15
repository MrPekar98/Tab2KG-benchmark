import precision
import recall
import f1

def evaluate_quality(base_dir, result_name, predictions, gt):
    precision_results = precision.write(base_dir + '/precision_' + result_name + '.csv', predictions, gt)
    recall_results = recall.write(base_dir + '/recall_' + result_name + '.csv', predictions, gt)
    f1.write(base_dir + '/f1_' + result_name + '.csv', precision_results, recall_results)
