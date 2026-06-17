import yfinance as yf
import pandas as pd
from datetime import datetime
from .DataProvider import DataProvider

class YahooFinanceProvider(DataProvider):
    
    def fetch_price_historic(
        self,
        ticker,
        filename: str = None,
        start: str = "2000-01-01",
        end: str = None
        )->pd.DataFrame:  

        if end is None:
            end = datetime.today().strftime("%Y-%m-%d")

        # Récupération des prix
        prices = yf.download(ticker, start=start, end=end)
        df = pd.DataFrame(prices)

        # correction:  yfinance renvoie des dataframe avec des
        # MultiIndex à chaque colonne. Il ne faut garder qu'une 
        # seule serie de données par colonnes.
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Récupération du nombre d'actions
        yf_ticker = yf.Ticker(ticker)
        shares = yf_ticker.get_shares_full()
        shares = shares[~shares.index.duplicated(keep="last")] # supprimer les indices en double
        # print(shares.head())
        if shares is not None and not shares.empty:

            # harmonise timezone éventuelle
            shares.index = shares.index.tz_localize(None)

            # réaligne sur les dates des prix
            shares = shares.reindex(
                df.index,
            ).ffill().bfill() # un ffill pour remplir avec les données de la dernière date, 
                              # un bfill pour le début quand on n'a pas encore eu de données sur le nombre de shares

            # ajouter la colonne au data frame
            df["SharesOutstanding"] = shares

            # market cap historique
            df["MarketCap"] = (
                df["Close"]
                * df["SharesOutstanding"]
            )
        # print(df.head())
        output_filename = filename or ticker    
        df.to_csv(f"data/{output_filename}.csv")
        return df

