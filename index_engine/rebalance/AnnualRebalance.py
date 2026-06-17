from .RebalanceRule import RebalanceRule
import pandas as pd

class AnnualRebalance(RebalanceRule):
    def get_rebalance_dates(self, start: pd.Timestamp, end: pd.Timestamp) -> pd.DatetimeIndex:
        year_starts = pd.date_range(start=start, end=end, freq="YS")

        rebalance_dates = []
        for date in year_starts:
            idx = self.market_days.searchsorted(date)

            if idx < len(self.market_days):
                rebalance_dates.append(self.market_days[idx])
        
        return pd.DatetimeIndex(rebalance_dates)
         