class Asset:    
    _ticker: str
    _name: str
    _sector: str
    
    def __init__(self, name: str, ticker: str, sector: str):
        self._ticker = ticker
        self._name = name
        self._sector = sector
    
    def get_ticker(self):
        return self._ticker
    
    def get_name(self):
        return self._name