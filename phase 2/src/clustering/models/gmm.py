import typing as th
from abc import ABCMeta
from sklearn.base import DensityMixin, BaseEstimator

# since you can use sklearn (or other libraries) implementations for this task,
#   you can either initialize those implementations in the provided format or use them as you wish
from sklearn.mixture import GaussianMixture


class GMM(DensityMixin, BaseEstimator, metaclass=ABCMeta):
    def __init__(
            self,
            cluster_count: int,
            max_iteration: int,
            # add required hyper-parameters (if any)
    ):
        # todo: initialize parameters
        pass

    def fit(self, x):
        # todo: for you to implement
        return self

    def predict(self, x):
        # todo: for you to implement
        pass
