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
            Asset("Procter & Gamble", "PG", "Consumer Staples"),

             # — ajouts —
            Asset("Tesla",               "TSLA",  "Consumer Discretionary"),  # incontournable 2020-2026
            Asset("Broadcom",            "AVGO",  "Tech"),                    # top 5 market cap en 2024-2026
            Asset("Eli Lilly",           "LLY",   "Healthcare"),              # explosion avec GLP-1 (Ozempic)
            Asset("UnitedHealth Group",  "UNH",   "Healthcare"),              # géant santé, top 10 US
            Asset("Mastercard",          "MA",    "Financials"),              # binôme naturel de Visa
            Asset("Chevron",             "CVX",   "Energy"),                  # diversifier l'énergie vs XOM seul
            Asset("Home Depot",          "HD",    "Consumer Discretionary"),  # top 15 US régulier
            Asset("Costco",              "COST",  "Consumer Staples"),        # surperformance constante
            Asset("Netflix",             "NFLX",  "Communication Services"),  # ×6 sur la période
            Asset("Bank of America",     "BAC",   "Financials"),              # 2e banque US par actifs
        ]

        self.fetch_data()  # récupère les données des titres de l'univers
        