from .Filter import Filter
from index_engine.universe import Universe
from index_engine.error import EmptyUniverseError
import pandas as pd

class PriceFilter(Filter):
    """
    Filtre par le prix du titre, à une date donnée.
    """
    def __init__(self, max_price: float, min_price: float = 0):
        self._max_price = max_price
        self._min_price = min_price

    def apply(self, universe: Universe, date: pd.Timestamp)->pd.Series:
        """
        Applique le filtre à l'univers et à la date passés en paramètre.
        """
        print("====PRICE FILTER====")
        n = universe.get_number_assets()
        mask = pd.Series([1]*n)
        for i in range(n):
            asset = universe.get_asset(i)
            price_serie = universe.get_price(asset)
            # vérifier si la date existe bien
            first_market_day = universe.get_first_market_day(asset)
            if first_market_day > date:
                mask[i] = 0
            elif price_serie[date] < self._min_price or price_serie[date] > self._max_price :
                # tester que le prix est bien dans la fourchette
                mask[i] = 0
                print(price_serie[date])
        print(mask)
        if mask.sum() == 0:
            error_string= f"Aucune action n'a passé le filtre de prix le {date}."
            raise EmptyUniverseError(error_string)
        return mask
