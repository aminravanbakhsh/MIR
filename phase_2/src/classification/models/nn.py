import typing as th
from sklearn.base import BaseEstimator, ClassifierMixin

# since you can use sklearn (or other libraries) implementations for this task,
#   you can either initialize those implementations in the provided format or use them as you wish
from sklearn.neural_network import MLPClassifier


class NeuralNetwork(BaseEstimator, ClassifierMixin):
    def __init__(
            self,
            # add required hyper-parameters (if any)
    ):
        # todo: initialize parameters
        pass

    def fit(self, x, y, **fit_params):
        # todo: for you to implement
        return self

    def predict(self, x):
        # todo: for you to implement
        pass
