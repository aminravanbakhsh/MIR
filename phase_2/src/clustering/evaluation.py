import typing as th


def purity(y, y_hat) -> float:
    # todo: for you to implement
    pass


def adjusted_rand_index(y, y_hat) -> float:
    # todo: for you to implement
    pass


evaluation_functions = dict(purity=purity, adjusted_rand_index=adjusted_rand_index)


def evaluate(y, y_hat) -> th.Dict[str, float]:
    """
    :param y: ground truth
    :param y_hat: model predictions
    :return: a dictionary containing evaluated scores for provided values
    """
    return {name: func(y, y_hat) for name, func in evaluation_functions.items()}
