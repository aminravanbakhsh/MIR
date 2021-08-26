import typing as th


def accuracy(y, y_hat) -> float:
    # todo: for you to implement
    pass


def f1(y, y_hat, alpha: float = 0.5, beta: float = 1.):
    # todo: for you to implement
    pass


def precision(y, y_hat) -> float:
    # todo: for you to implement
    pass


def recall(y, y_hat) -> float:
    # todo: for you to implement
    pass


evaluation_functions = dict(accuracy=accuracy, f1=f1, precision=precision, recall=recall)


def evaluate(y, y_hat) -> th.Dict[str, float]:
    """
    :param y: ground truth
    :param y_hat: model predictions
    :return: a dictionary containing evaluated scores for provided values
    """
    return {name: func(y, y_hat) for name, func in evaluation_functions.items()}
