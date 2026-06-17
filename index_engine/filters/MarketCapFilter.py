from .Filter import Filter
from index_engine.universe.Universe import Universe
from index_engine.error import EmptyUniverseError
import pandas as pd

class MarketCapFilter(Filter):
    """
    Filtre par la capitalisation de marché totale du titre, à une date donnée.
    """
    def __init__(self, max_cap: float,  min_cap: float = 0):
        self._max_cap = max_cap
        self._min_cap = min_cap

    def apply(self, universe: Universe, date: pd.Timestamp)->pd.Series:
        """
        Appliquer le filtre à l'univers et à la date donnés en paramètres.
        Renvoie le masque adapté à l'univers. Ne prend en compte que les titres 
        présents sur le marché à cette date.
        """
        print("====MARKET CAP FILTER====")
        n = universe.get_number_assets()
        mask = pd.Series([1]*n)
        for i in range(n):
            asset = universe.get_asset(i)
            # vérifier si le premier jour de cotation de l'asset est antérieur
            # à la date à laquelle on applique le filtre
            first_market_day = universe.get_first_market_day(asset)
            if first_market_day > date:
                mask[i] = 0
            else:
                market_cap_serie = universe.get_market_cap(asset)
                if market_cap_serie[date] < self._min_cap or market_cap_serie[date] > self._max_cap:
                    # tester si la market cap est bien dans le range
                    mask[i] = 0
                print(market_cap_serie[date])
        print(mask)
        if mask.sum() == 0:
            chaine = f"Aucune action n'a passé le filtre de la market cap le {date}."
            raise EmptyUniverseError(chaine)
        return mask
