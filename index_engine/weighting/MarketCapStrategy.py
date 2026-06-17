from .WeightingStrategy import WeightingStrategy
from index_engine.universe import Universe
import pandas as pd

class MarketCapStrategy(WeightingStrategy):
    
    def compute_weights(self, universe: Universe, mask: pd.Series, date: pd.Timestamp)->pd.Series:
        """
        Calcule les poids à la date considérée en fonction de la
        capitalisation boursière du titre.
        """
        n = universe.get_number_assets() # n = nombre de titres dans l'univers global
        tickers = [universe.get_asset(i).get_ticker() for i in range(n)]
        weights = pd.Series([0.0] * n, index=tickers)  # index par ticker
        total_market_cap = 0.0

        for i in range(n):
            if mask.iloc[i] == 1:
                asset = universe.get_asset(i)
                mc = universe.get_market_cap(asset)[date]
                weights.iloc[i] = mc
                total_market_cap += mc

        if total_market_cap == 0:
            raise Exception("Market cap totale est nulle")
        weights = weights / total_market_cap

        print("====WEIGHTING====")
        print(weights)
        print(f"check sum: {weights.sum()}")

        return weights