import numpy as np
from sklearn import tree
from scipy.stats import mode


class RandomForest:
    def __init__(self, max_depth, forest_size, X_train, Y_train, max_features):
        self.max_depth = max_depth
        self.forest_size = forest_size
        self.trees = []

        for _ in range(forest_size):
            clf = tree.DecisionTreeClassifier(criterion='gini', splitter='random', max_depth=self.max_depth,
                                              max_features=max_features)
            clf.fit(X=X_train, y=Y_train)
            self.trees.append(clf)

    def predict(self, X):
        predictions = []
        for the_tree in self.trees:
            predictions.append(the_tree.predict(X))
        predictions = np.stack(predictions)
        result = np.array(mode(predictions, axis=0)[0])
        return result
