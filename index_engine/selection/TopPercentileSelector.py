import pandas as pd

class TopPercentileSelector:
    def __init__(self, percentile: float):
        self.percentile = percentile

    def select(self, ranking: pd.Series)->pd.Series:
        print("====TOP PERCENTILE SELECTOR====")
        return