from src.numericalsolution.DataWrapper.statistics import Statistics


class Response:
    def __init__(self, is_ok: bool, root: float, method: str, message: str, statistics: Statistics):
        self.is_ok = is_ok
        self.root = root
        self.message = message
        self.method = method
        self.statistics = statistics

    def print(self):
        return f"IsOk: {self.is_ok} | Root: {self.root} | Method: {self.method} | Message: {self.message} | Stat: {self.statistics} "

    def __repr__(self):
        return self.print()

    def __str__(self):
        return self.print()
