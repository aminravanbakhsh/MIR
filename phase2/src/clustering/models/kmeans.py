import typing as th
from sklearn.base import TransformerMixin, ClusterMixin, BaseEstimator


class KMeans(TransformerMixin, ClusterMixin, BaseEstimator):
    def __init__(
            self,
            cluster_count: int,
            max_iteration: int,
            # add required hyper-parameters (if any)
    ):
        # todo: initialize parameters
        pass
        self.centroids = None

    def fit(self, x):
        # todo: for you to implement
        return self

    def predict(self, x):
        # todo: for you to implement
        pass
