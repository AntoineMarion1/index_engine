from .Selector import Selector
from index_engine.universe import Universe
import pandas as pd

class TopNSelector(Selector):
    """
    Sélectionne les N meilleurs titres.
    """
    def __init__(self, n: int):
        self.n = n

    def select(self, ranking: pd.Series)->pd.Series:
        """
        Renvoie un mask sous forme de pd.Series sélectionnant les N 
        meilleurs titres, conformément à leur rang.
        """
        print("====TOP N SELECTOR====")

        selection = (ranking.astype(float).fillna(float('inf')) <= self.n).astype(int)
        print(selection)
        return selection