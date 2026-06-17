from index_engine.universe import Universe
import pandas as pd 

class Filter:
    """
    Un filtre est un objet qui contient une méthode apply et un nom.
    """
    def __init__(self, name: str):
        self.name = name

    def apply(self, universe: Universe, date: pd.Timestamp)->pd.Series:
        """Applique le filtre."""
        del universe, date
        raise NotImplementedError(f"La classe {self.__class__.__name__} doit implémenter apply()")
