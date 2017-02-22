import random
import csv
import math
import os


def get_split(data_set, n_features):
    class_values = list(set(row[-1] for row in data_set))
    b_index, b_value, b_score, b_groups = 999, 999, 999, None
    features = list()
    while len(features) < n_features:
        index = random.randrange(len(data_set[0]) - 1)
        if index not in features:
            features.append(index)
    for index in features:
        for row in data_set:
            groups = test_split(index, row[index], data_set)
            gini = gini_index(groups, class_values)
            if gini < b_score:
                b_index, b_value, b_score, b_groups = index, row[index], gini, groups
    return {'index': b_index, 'value': b_value, 'groups': b_groups}


def load_csv(data_path, file_name):
    data_set = list()
    with open(os.path.join(data_path, file_name), 'r') as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            if not row:
                continue
            data_set.append(row)
    return data_set


def str_column_to_float(data_set, column):
    for row in data_set:
        row[column] = float(row[column].strip())


def str_column_to_int(data_set, column):
    class_values = [row[column] for row in data_set]
    unique = set(class_values)
    look_up = dict()
    for i, value in enumerate(unique):
        look_up[value] = i

    for row in data_set:
        row[column] = look_up[row[column]]

    return look_up


def cross_validation_split(data_set, n_folds):
    data_set_split = list()
    data_copy = list(data_set)
    fold_size = len(data_set) / n_folds
    for i in range(n_folds):
        fold = list()
        while len(fold) < fold_size:
            index = random.randrange(len(data_copy))
            fold.append(data_copy.pop(index))
        data_set_split.append(fold)

    return data_set_split


def accuracy_metric(actual, predicted):
    correct = 0
    for i in range(len(actual)):
        if actual[i] == predicted[i]:
            correct += 1

    return correct / float(len(actual)) * 100.0


def evaluate_algorithm(data_set, algorithm, n_folds, *args):
    folds = cross_validation_split(data_set, n_folds)
    scores = list()
    for fold in folds:
        train_set = list(folds)
        train_set.remove(fold)
        train_set = sum(train_set, [])
        test_set = list()
        for row in fold:
            row_copy = list(row)
            test_set.append(row_copy)
            row_copy[-1] = None
        predicted = algorithm(train_set, test_set, *args)
        actual = [row[-1] for row in fold]
        accuracy = accuracy_metric(actual, predicted)
        scores.append(accuracy)
    return scores


def test_split(index, value, data_set):
    left, right = list(), list()
    for row in data_set:
        if row[index] < value:
            left.append(row)
        else:
            right.append(row)
    return left, right


def gini_index(groups, class_values):
    gini = 0.0
    for class_value in class_values:
        for group in groups:
            size = len(group)
            if size == 0:
                continue
            proportion = [row[-1] for row in group].count(class_value) / float(size)
            gini += proportion * (1.0 - proportion)
    return gini


def to_terminal(group):
    outcomes = [row[-1] for row in group]
    return max(set(outcomes), key=outcomes.count)


def split(node, max_depth, min_size, n_features, depth):
    # create child splits for a node or make terminal
    left, right = node['groups']
    del(node['groups'])
    # check for a no split
    if not left or not right:
        node['left'] = node['right'] = to_terminal(left + right)
        return
    # check for max depth
    if depth >= max_depth:
        node['left'], node['right'] = to_terminal(left), to_terminal(right)
        return
    # process left child
    if len(left) <= min_size:
        node['left'] = to_terminal(left)
    else:
        node['left'] = get_split(left, n_features)
        split(node['left'], max_depth, min_size, n_features, depth+1)
    # process right child
    if len(right) <= min_size:
        node['right'] = to_terminal(right)
    else:
        node['right'] = get_split(right, n_features)
        split(node['right'], max_depth, min_size, n_features, depth=+1)


def build_tree(train, max_depth, min_size, n_features):
    root = get_split(train, n_features)
    split(root, max_depth, min_size, n_features, 1)
    return root


def predict(node, row):
    # make a prediction with a decision tree
    if row[node['index']] < node['value']:
        if isinstance(node['left'], dict):
            return predict(node['left'], row)
        else:
            return node['left']
    else:
        if isinstance(node['right'], dict):
            return predict(node['right'], row)
        else:
            return node['right']


def sub_sample(data_set, ratio):
    # create a random subsample form the dataset with replacement
    sample = list()
    n_sample = round(len(data_set) * ratio)
    while len(sample) < n_sample:
        index = random.randrange(len(data_set))
        sample.append(data_set[index])
    return sample


def bagging_predict(trees, row):
    # make a prediction with a list of bagged trees
    predictions = [predict(tree, row) for tree in trees]
    return max(set(predictions), key=predictions.count)


def random_forest(train, test, max_depth, min_size, sample_size, n_trees, n_features):
    trees = list()
    for i in range(n_trees):
        sample = sub_sample(train, sample_size)
        tree = build_tree(sample, max_depth, min_size, n_features)
        trees.append(tree)

    predictions = [bagging_predict(trees, row) for row in test]
    return predictions


# test the random forest algorithm