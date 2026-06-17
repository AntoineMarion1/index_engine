from .RebalanceRule import RebalanceRule
import pandas as pd

class MonthlyRebalance(RebalanceRule):
    def get_rebalance_dates(self, start: pd.Timestamp, end: pd.Timestamp) -> pd.DatetimeIndex:
        """
        Renvoie les dates de rebalancement mensuelles.
        """

        period_starts = pd.date_range(start=start, end=end, freq="MS")

        idx = self.market_days.searchsorted(period_starts)

        valid = idx < len(self.market_days)

        return pd.DatetimeIndex(self.market_days[idx[valid]])