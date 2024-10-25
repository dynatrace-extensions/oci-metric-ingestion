class SummaryStat:
    def __init__(
        self,
        value_min: float,
        value_max: float,
        value_sum: float,
        value_count: float,
    ):
        self.value_min = value_min
        self.value_max = value_max
        self.value_sum = value_sum
        self.value_count = value_count

    def __str__(self):
        return f"min={self.value_min},max={self.value_max},sum={self.value_sum},count={self.value_count}"
