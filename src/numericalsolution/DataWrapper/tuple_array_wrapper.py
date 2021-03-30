from abc import ABC

from src.numericalsolution.Common.binary_search import BinarySearch
from src.numericalsolution.DataWrapper.data_wrapper import DataWrapper


class TupleArrayWrapper(DataWrapper, ABC):
    def __init__(self, tuple_list):
        self.__callsNumber = 0
        self.__tuple_list = tuple_list
        # self.__xList = []
        # self.__yList = []
        # for t in tuple_list:
        #     self.__xList.append(t[0])
        #     self.__yList.append(t[1])

    def get_value_at(self, x, lo=0, hi=None):
        self.__callsNumber += 1

        k = BinarySearch.binary_search(self.__tuple_list, x)
        if k > -1:
            return self.__tuple_list[k][1]
        else:
            k = abs(k) - 2
            if k > -1 and (k < len(self.__tuple_list) - 1):
                return self.__tuple_list[k][1] + (self.__tuple_list[k + 1][1] - self.__tuple_list[k][1]) * (
                            x - self.__tuple_list[k][0]) / (
                               self.__tuple_list[k + 1][0] - self.__tuple_list[k][0])

        raise ValueError(f"Cant find x={x}")

    def get_statistics(self):
        return self.__callsNumber

    def get_max_x(self):
        return self.__tuple_list[len(self.__tuple_list) - 1][0]

    def get_min_x(self):
        return self.__tuple_list[0][0]

    def clear_statistics(self):
        self.__callsNumber = 0
