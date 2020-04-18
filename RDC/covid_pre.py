import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
import pickle


def data_split(data, ratio):
    np.random.seed(42)
    shuffled = np.random.permutation(len(data))
    test_set_size = int(len(data) * ratio)
    test_indices = shuffled[:test_set_size]
    train_indices = shuffled[test_set_size:]
    return data.iloc[train_indices], data.iloc[test_indices]


if __name__ == '__main__':
    # read the data
    df = pd.read_csv('data.csv')
    train, test = data_split(df, 0.2)
    x_train = train[['fever', 'body_pain', 'age', 'runny_nose', 'diff_breath']].to_numpy()
    x_test = test[['fever', 'body_pain', 'age', 'runny_nose', 'diff_breath']].to_numpy()

    y_train = train[['virus_prob']].to_numpy().reshape(2275, )
    y_test = test[['virus_prob']].to_numpy().reshape(568, )

    clf = LogisticRegression()  # initializing LR model
    clf.fit(x_train, y_train)

    # open a file, where you want to store the data
    file = open('model.pkl', 'wb')

    # dump information to that file
    pickle.dump(clf, file)
    file.close()


