import pandas as pd

class DataProvider:
    """Classe abstraite pour la récupération des données"""

    def fetch_price_historic(self, ticker: str, start_date: str = None, end_date: str = None)->pd.DataFrame:
        """
        Renvoie un dataframe contenant l'historique des prix d'un actif, 
        entre les dates spécifiées en paramètre. Par défaut, renvoie le prix 
        sur les 5 dernières années, avec un pas de temps de 1 jour.
        """
        raise NotImplementedError("DataProvider est une classe abstraite")
    
    def get_market_cap(self, filename: str)->pd.Series:
        """
        Renvoie une Series contenant la market cap de l'asset
        donc le ticker ou le nom de fichier est passé en paramètre.
        """
        df = pd.read_csv(f"data/{filename}.csv", index_col=0, parse_dates=True)
        return df["MarketCap"]
    
    def get_price(self, filename: str)->pd.Series:
        """
        Renvoie une Series contenant le prix de l'asset
        donc le ticker ou le nom de fichier est passé en paramètre.
        """
        df = pd.read_csv(f"data/{filename}.csv", index_col=0, parse_dates=True)
        return df["Close"]
