class Statistics:
    def __init__(self, calls_number: int = 0, iterations: int = 0):
        self.callsNumbers = calls_number
        self.iterations = iterations

    def print(self):
        return f"CallsNumbers: {self.callsNumbers} | Iterations: {self.iterations}"

    def __repr__(self):
        return self.print()

    def __str__(self):
        return self.print()
