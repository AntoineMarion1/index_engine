from .WeightingStrategy import WeightingStrategy
from index_engine.universe import Universe
from index_engine.error import EmptyUniverseError
import pandas as pd

class EqualWeightsStrategy(WeightingStrategy):
    
    def compute_weights(self, universe: Universe, mask: pd.Series, date: pd.Timestamp) -> pd.Series:
        """
        Renvoyer les poids: 1/ nombre de titres dont le masque est 1
        """
        del date
        n = mask.sum()
        if n <= 0:
            raise EmptyUniverseError("Univers vide")

        w = 1 / n

        # tickers pour TOUS les actifs de l'univers (pas seulement ceux sélectionnés)
        tickers = [universe.get_asset(i).get_ticker() for i in range(len(mask))]

        weights = pd.Series(mask.astype(float).values * w, index=tickers)

        print("====WEIGHTING====")
        print(weights)
        print(f"check sum: {weights.sum()}")

        return weights