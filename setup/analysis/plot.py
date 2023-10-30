import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter

def plot(type_distribution, top_k, x_size, y_size, filename):
    counter = Counter(type_distribution)
    type_distribution = {k:v for k, v in counter.most_common()[:top_k]}
    fig, ax = plt.subplots(figsize = (x_size, y_size))
    data = pd.DataFrame()
    data['Entity types'] = list(type_distribution.keys())
    data['Type frequency'] = list(type_distribution.values())
    plot = sns.barplot(data, x = 'Entity types', y = 'Type frequency', ax = ax)
    plot.set_xticklabels(plot.get_xticklabels(), rotation = 30, horizontalalignment = 'right')
    plt.savefig(filename)
