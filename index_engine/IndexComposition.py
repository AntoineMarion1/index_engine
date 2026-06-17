import pandas as pd

class IndexComposition:
    def __init__(
        self,
        date: pd.Timestamp,
        constituents: list,
        scores,
        weights
    ):
        self.date = date
        self.constituents = constituents # list de tous les assets de l'univers
        self.scores = scores
        self.weights = weights # poids de tous les assets de l'univers

    def get_weights(self)->pd.Series:
        return self.weights
    
    def get_asset(self, i: int):
        return self.constituents[i]