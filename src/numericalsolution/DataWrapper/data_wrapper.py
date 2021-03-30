from abc import ABC, abstractmethod


class DataWrapper(ABC):
    @abstractmethod
    def get_value_at(self, x, lo=None, hi=None):
        pass

    def get_statistics(self):
        pass

    def clear_statistics(self):
        pass

    def __call__(self, *args, **kwargs):
        return self.get_value_at(args[0])
