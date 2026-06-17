import pandas as pd
from index_engine.universe import Universe

class ScoringFactor:
    def __init__(self):
        return
    
    def compute_scores(self, universe: Universe, mask: pd.Series, date: pd.Timestamp)->pd.Series:
        del universe, mask
        raise NotImplementedError(f"La classe {self.__class__.__name__} doit implémenter get_rebalance compute_scores()")
