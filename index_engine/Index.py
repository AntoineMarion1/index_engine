from index_engine.scoring import ScoringFactor
from index_engine.selection import Selector
from index_engine.weighting import WeightingStrategy
from index_engine.rebalance import RebalanceRule
from index_engine.universe import Universe
from index_engine.IndexComposition import IndexComposition
from index_engine.backtest import BacktestResult
import pandas as pd 

class Index:
    def __init__(
            self, 
            universe: Universe,
            filters: list, 
            scorer: ScoringFactor, 
            selector: Selector, 
            weighter: WeightingStrategy, 
            constraints: list, 
            rule: RebalanceRule
        ):
        self.universe = universe
        self.filters = filters
        self.scorer = scorer
        self.selector = selector
        self.weighter = weighter
        self.constraints = constraints
        self.rule = rule
        self.index_composition = None
        self.basis = 100 # valeur initiale de l'indice

    def compute(self, date: pd.Timestamp | str)->IndexComposition:
        date = pd.Timestamp(date) # gérer le cas ou on passse une date en paramètre de la fonction

        #le masque ne contient pour le moment que des 1, car on garde tous les assets
        n = self.universe.get_number_assets()
        mask = pd.Series([1] * n) 
        # les scores sont tous égaux à 0 pour le moment
        scores = pd.Series([0.0] * n) 
        # le classement se fait pour le moment dans un ordre déterministe
        ranking = pd.Series([i for i in range(n)])
        # la stratégie de base pour le weighting est EqualWeights
        weights = pd.Series([1/n] * n)

        # FILTERING
        for filter in self.filters:
            new_mask = filter.apply(self.universe, date)
            mask  = mask & new_mask

        # RANKING
        scores = self.scorer.compute_scores(self.universe, mask, date)
        ranking = scores.rank(ascending=False, method = "first").convert_dtypes(True)

        # SELECTION
        mask = mask & self.selector.select(ranking)

        # WEIGHTING
        weights = self.weighter.compute_weights(self.universe, mask, date)

        # CONSTRAINING
        for constraint in self.constraints:
            weights = constraint.apply(self.universe, weights, date)

        index_comp = IndexComposition(date, self.universe.assets, scores, weights)
        self.index_composition = index_comp
        return index_comp
    
    def constituents(self):
        """
        renvoie un Dataframe avec en indice les noms d'assets et en valeurs
        le poids de chaque asset dont le poids n'est pas égal à 0.
        """
        n = self.universe.get_number_assets()
        res_dict = {}
        weights = self.index_composition.get_weights()
        for i in range(n):
            asset = self.universe.get_asset(i)
            weight = weights.iloc[i]
            if weight != 0:
                res_dict[asset.get_name()] = weight
        
        return pd.Series(res_dict)
    
    def backtest(
            self, 
            start: str | pd.Timestamp, 
            end: str | pd.Timestamp
            )->BacktestResult:
        """
        Renvoie un objet backtest result contenant les 
        compositions d'indice à chaque date de rebalancement.
        """
        start = self.universe.get_next_market_day(pd.Timestamp(start))
        end = pd.Timestamp(end)

        # Il faut calculer la composition de l'indice le jour de son lancement
        # on l'ajoute donc à la liste des dates de rebalancement.
        rebalance_dates = (
            pd.DatetimeIndex([start])
            .append(self.rule.get_rebalance_dates(start, end))
            .unique()
            .sort_values()
        )

        print("====REBALANCE DATES====")
        print(rebalance_dates)

        # Créer un objet BacktestResult pour tout sauvegarder.
        result = BacktestResult(self.universe, rebalance_dates, start, end)

        # Ajouter la composition de l'indice à chaque rebalancement
        for date in rebalance_dates:
            result.add_rebalance(date, self.compute(date))

        # Calculer la valeur de l'indice à chaque date de cotation.
        result._compute_index_values(self.basis)
        return result
    