import pandas as pd
from index_engine.universe import Universe

class WeightingStrategy:
    def __init__(self):
        return
    
    def compute_weights(self, universe: Universe, mask: pd.Series, date: pd.Timestamp)->pd.Series:
        del universe, mask, date
        raise NotImplementedError(f"La classe {self.__class__.__name__} doit implémenter get_rebalance_dates()")



