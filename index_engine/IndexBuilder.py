from index_engine import Index
from index_engine.universe import Universe, SP500Universe
from index_engine.data import YahooFinanceProvider
from index_engine.filters import MarketCapFilter, PriceFilter
from index_engine.scoring import MomentumFactor
from index_engine.selection import TopNSelector, TopPercentileSelector
from index_engine.weighting import MarketCapStrategy, EqualWeightsStrategy
from index_engine.rebalance import RebalanceRule
from index_engine.constraints import Constraints, NoConstraints

UNIVERSE_REGISTRY = {
    "S&P500": SP500Universe("S&P500", YahooFinanceProvider())
}

class IndexBuilder:
    def __init__(self, name: str, universe_name: str = None):
        self.name = name

        if universe_name in UNIVERSE_REGISTRY.keys():
            self.universe = UNIVERSE_REGISTRY[universe_name]
        else:
            raise KeyError(f"l'univers {universe_name} n'existe pas")
        
        self.filters = [] # par défaut pas de filtres
        self.scorer = MomentumFactor(30) # par défaut un momentum 1 mois
        self.selector = TopNSelector(10) # par défaut, on choisit les 10 meilleurs titres.
        self.weighter = MarketCapStrategy() # par défaut, on calcule les poids par la market cap
        self.rule = RebalanceRule("MS", self.universe.get_market_days()) # par défaut, on rebalance chaque mois
        self.constraints = [NoConstraints()] # par défaut, on n'a pas de contraintes

    def filter_market_cap(self, max_cap: float, min_cap: float = 0)->IndexBuilder:
        """
        Modifie le masque de l'indice, de sorte à être filtré
        par la capitalisation.
        """
        self.filters.append(MarketCapFilter(max_cap, min_cap))
        return self

    def filter_price(self, max_price: float, min_price: float = 0)->IndexBuilder:
        """
        Modifie le masque de l'indice, de sorte à être filtré
        par le prix.
        """
        self.filters.append(PriceFilter(max_price, min_price))
        return self
    
    def rank_by(self, factor: str, asc: bool = False)->IndexBuilder:
        """
        Ajoute un critère de ranking. Critères disponibles:
        - momentum_12m
        - momentum_6m
        """
        if factor == "momentum_12m":
            self.scorer = MomentumFactor(252)
        elif factor == "momentum_6m":
            self.scorer = MomentumFactor(126)
        else:
            raise KeyError("Le facteur de scoring n'existe pas.")
        return self
    
    def select_topN(self, N: int)->IndexBuilder:
        """
        Ajouter le sélecteur topN.
        """
        self.selector = TopNSelector(N)
        return self
    
    def select_top_percentile(self, percentile: float)->IndexBuilder:
        """
        Ajoute le sélecteur top percentile.
        """
        self.selector = TopPercentileSelector(percentile)
        return self
    
    def weight(self, method: str)->IndexBuilder:
        """
        Ajoute la stratégie de weighting.
        """
        if method == "equal_weights":
            self.weighter = EqualWeightsStrategy()
        elif method == "market_cap":
            self.weighter = MarketCapStrategy()
        else:
            raise KeyError("La stratégie de poids n'existe pas.")
        return self

    def rebalance(self, frequency: str)->IndexBuilder:
        """
        Ajoute la règle de rebalancement de l'indice.
        """
        market_days = self.universe.get_market_days() # datetimeindex
        self.rule = RebalanceRule(frequency, market_days)
        
        return self
    
    def add_constraints(self, constraints: Constraints)->IndexBuilder:
        """
        Ajoute des contraintes.
        """
        self.constraints.append(constraints)
        return self

    def build(self)->Index:
        """
        Construis l'indice. Renvoie un objet de type Index.
        """
        index = Index(
            self.universe,
            self.filters,
            self.scorer,
            self.selector,
            self.weighter,
            self.constraints,
            self.rule
        )
        return index
