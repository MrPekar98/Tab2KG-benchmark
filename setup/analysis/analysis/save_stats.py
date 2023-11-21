import pickle

def load_stats(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)

def write_stats(filename, stat):
    with open(filename, 'wb') as file:
        pickle.dump(stat, file, pickle.HIGHEST_PROTOCOL)
