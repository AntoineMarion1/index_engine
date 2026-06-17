import pandas as pd

class Selector:
    def __init__(self):
        return
    
    def select(self, ranking: pd.Series)->pd.Series:
        raise NotImplementedError(f"La classe {self.__class__.__name__} doit implémenter get_rebalance_dates()")
