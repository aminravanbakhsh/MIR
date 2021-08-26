import typing as th
from sklearn.base import BaseEstimator, ClassifierMixin


class KNN(BaseEstimator, ClassifierMixin):
    def __init__(
            self,
            k: int,
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
