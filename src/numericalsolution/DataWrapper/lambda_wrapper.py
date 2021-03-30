from abc import ABC

from src.numericalsolution.DataWrapper.data_wrapper import DataWrapper


class LambdaWrapper(DataWrapper, ABC):
    def __init__(self, f):
        self.__f = f
        self.__callsNumber = 0

    def get_value_at(self, x, lo=None, hi=None):
        self.__callsNumber += 1
        return self.__f(x)

    def get_statistics(self):
        return self.__callsNumber

    def clear_statistics(self):
        self.__callsNumber = 0
