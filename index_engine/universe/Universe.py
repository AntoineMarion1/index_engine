from index_engine.universe.Asset import Asset
from index_engine.data.DataProvider import DataProvider
from index_engine.data.YahooFinanceProvider import YahooFinanceProvider
from pathlib import Path
import pandas as pd

class Universe:

    assets : list[Asset] # liste contenant les titres de l'univers, sous la forme d'objets de type Asset

    def __init__(self, name : str, data_provider: DataProvider = None):
        self.name = name
        self.dp = data_provider if data_provider is not None else YahooFinanceProvider()

    def fetch_data(self):
        """
        Récupère les données des titres de l'univers depuis
        le dataprovider.
        """
        print("fetch data")
        Path("data").mkdir(exist_ok=True)
        for a in self.assets:
            ticker = a.get_ticker()
            self.dp.fetch_price_historic(ticker, self.name + "_" + ticker)

    def get_number_assets(self)->int:
        """renvoie le nombre d'assets dans l'univers"""
        return len(self.assets)

    def get_asset(self, i: int):
        return self.assets[i]
    
    def get_market_cap(self, asset: Asset)->pd.Series:
        """
        Renvoie une series contenant la market cap de l'asset 
        passé en paramètre. Utilise le DataProvider. 
        """
        ticker = asset.get_ticker()
        return self.dp.get_market_cap(self.name + "_" + ticker)
    
    def get_price(self, asset: Asset)->pd.Series:
        """
        Renvoie une series contenant le prix de l'asset 
        passé en paramètre, en indice les dates.
        Utilise le DataProvider. 
        """
        ticker = asset.get_ticker()
        return self.dp.get_price(self.name + "_" + ticker)
    
    def get_all_prices(self)->pd.DataFrame:
        """
        Renvoie un DataFrame contenant le prix de tous les assets 
        à toutes les dates. 
        """
        dic = {}
        for asset in self.assets:
            price_series = self.dp.get_price(self.name + "_" + asset.get_ticker())
            dic[asset.get_ticker()]= price_series
        return pd.DataFrame(dic)
    
    def get_all_returns(self)->pd.DataFrame:
        """
        Renvoie un DataFrame contenant les return de tous les assets
        à toutes les dates.
        """
        return self.get_all_prices().pct_change()
    
    def get_market_days(self, asset: Asset = None)->pd.DatetimeIndex:
        """
        Renvoie un DatetimeIndex contenant toutes les dates de cotation.
        """
        if asset is None:
            prices: pd.DataFrame = self.get_all_prices()
        else:
            prices: pd.DataFrame = self.get_price(asset)
        return prices.index

    def get_next_market_day(self, date: pd.Timestamp) -> pd.Timestamp:
        """
        Renvoie le prochain jour de marché après la date donnée.
        """
        market_days = self.get_market_days().sort_values()

        # position d'insertion strictement après la date
        pos = market_days.searchsorted(date, side="right")

        # s'il existe un jour suivant
        if pos < len(market_days):
            return market_days[pos]

        # sinon pas de jour suivant disponible
        return pd.NaT
    
    def get_first_market_day(self, asset: Asset) -> pd.Timestamp:
        """
        Renvoie le premier jour de cotation du marché de l'asset.
        """
        market_days = self.get_market_days(asset).sort_values()
        return market_days[0]