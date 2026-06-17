from .ScoringFactor import ScoringFactor
from index_engine.universe import Universe
from index_engine.error import HistoryError
import pandas as pd

class MomentumFactor(ScoringFactor):
    """Facteur de momentum"""

    def __init__(self, lookback: int):
        self.lookback = lookback # Nombre de jours de cotation sur lequel de calculer le momentum.

    def compute_scores(self, universe: Universe, mask: pd.Series, date: pd.Timestamp)->pd.Series:
        """
        Renvoie une Series contenant les scores des asset de l'univers. 
        Le score est calculé comme le return sur les self.lookback derniers 
        jours. Dans le cas ou il n'y a pas suffisamment d'historique pour calculer
        le momentum, on exclut le titre de l'indice.
        """
        print("====SCORING====")
        n = universe.get_number_assets()
        scores = pd.Series([0.0]*n)
        for i in range(n):
            if mask[i]==1:
                asset = universe.get_asset(i)
                price_serie = universe.get_price(asset)
                pos = price_serie.index.get_loc(date)

                # vérifier que l'on a suffisamment d'historique pour calculer
                # le momentum de l'asset
                if pos < self.lookback:
                    error_message = f"Il n'y a pas {self.lookback} jours d'historique avant le {date} pour {asset.get_name()}."
                    print(error_message)
                    scores[i] = pd.NA
                else: 
                    price_252d_ago = price_serie.iloc[pos - self.lookback]
                    price_at_date = price_serie.loc[date]
                    scores[i] = price_at_date / price_252d_ago - 1
            else:
                scores[i] = pd.NA
            print(scores[i])
        return scores
        