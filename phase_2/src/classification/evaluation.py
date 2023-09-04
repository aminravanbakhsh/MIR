import typing as th
import numpy as np


def accuracy(y, y_hat) -> float:

    print('ho')

    t = np.array(y)
    p = np.array(y_hat)
    correct = np.logical_not(np.logical_xor(t, p))
    N = len(t)
    
    TP = list(np.logical_and(correct, t)).count(True)
    TN = list(np.logical_and(correct, np.logical_not(t))).count(True)
    return (TP + TN)/N


def f1(y, y_hat, alpha: float = 0.5, beta: float = 1.):

    return 1 / ((alpha/precision(y, y_hat)) + ((1-alpha)/ recall(y, y_hat)))


def precision(y, y_hat) -> float:

    t = np.array(y)
    p = np.array(y_hat)
    correct = np.logical_not(np.logical_xor(t, p))

    TP = list(np.logical_and(correct, t)).count(True)
    FP = list(np.logical_and(np.logical_not(correct), t)).count(True)
    
    return TP/(TP + FP)


def recall(y, y_hat) -> float:

    t = np.array(y)
    p = np.array(y_hat)
    correct = np.logical_not(np.logical_xor(t, p))

    TP = list(np.logical_and(correct, t)).count(True)
    FN = list(np.logical_and(np.logical_not(correct), np.logical_not(t))).count(True)

    return TP/(TP + FN)


evaluation_functions = dict(accuracy=accuracy, f1=f1, precision=precision, recall=recall)


def evaluate(y, y_hat) -> th.Dict[str, float]:
    """
    :param y: ground truth
    :param y_hat: model predictions
    :return: a dictionary containing evaluated scores for provided values
    """
    return {name: func(y, y_hat) for name, func in evaluation_functions.items()}
