from index_engine.universe import Universe
import pandas as pd

class Constraints:
    def __init__(self):
        return
    
    def apply(self, universe: Universe, weights: pd.Series, date: pd.Timestamp)->pd.Series:
        raise NotImplementedError(f"La classe {self.__class__.__name__} doit implémenter apply()")
