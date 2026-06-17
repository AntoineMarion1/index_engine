import pandas as pd

class RebalanceRule():
    def __init__(self, freq: str, market_days: pd.DatetimeIndex):
        self.freq = freq
        self.market_days = market_days
    
    def get_rebalance_dates(self, start: pd.Timestamp, end: pd.Timestamp)->pd.DatetimeIndex:
        """
        Renvoie un DatetimeIndex contenant les dates de rebalancement de l'indice.
        """
        period_starts = pd.date_range(start=start, end=end, freq=self.freq)

        idx = self.market_days.searchsorted(period_starts)

        valid = idx < len(self.market_days)

        return pd.DatetimeIndex(self.market_days[idx[valid]])
