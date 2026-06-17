from .Constraints import Constraints
from index_engine.universe import Universe
import pandas as pd

class NoConstraints(Constraints):
    def apply(self, universe: Universe, weights: pd.Series, date: pd.Timestamp)->pd.Series:
        del universe, date
        return weights