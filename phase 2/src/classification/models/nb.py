import typing as th  # Literals are available for python>=3.8
from sklearn.base import BaseEstimator, ClassifierMixin


class NaiveBayes(BaseEstimator, ClassifierMixin):
    def __init__(
            self,
            kind,  #: th.Literal['gaussian', 'bernoulli', ],
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
