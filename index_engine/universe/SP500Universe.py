from .Universe import Universe, Asset
from index_engine.data.DataProvider import DataProvider

class SP500Universe(Universe):
    def __init__(self, name: str, data_provider: DataProvider = None):
        super().__init__(name, data_provider)

        self.assets = [
            Asset("Apple", "AAPL", "Tech"),
            Asset("Microsoft", "MSFT", "Tech"),
            Asset("Alphabet Inc.", "GOOG", "Tech"),
            Asset("Amazon", "AMZN", "Consumer Discretionary"),
            Asset("NVIDIA", "NVDA", "Tech"),
            Asset("Meta Platforms", "META", "Tech"),
            Asset("Berkshire Hathaway", "BRK-B", "Financials"),
            Asset("JPMorgan Chase", "JPM", "Financials"),
            Asset("Exxon Mobil", "XOM", "Energy"),
            Asset("Johnson & Johnson", "JNJ", "Healthcare"),
            Asset("Visa", "V", "Financials"),
            Asset("Walmart", "WMT", "Consumer Staples"),
            Asset("Procter & Gamble", "PG", "Consumer Staples")
        ]

        self.fetch_data()  # récupère les données des titres de l'univers