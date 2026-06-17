# index structuring engine

idée générale: ne load les données dans la RAM que lorsqu'on en a besoin


Universe
→ Filters (market cap, price)
→ Factor Scoring
→ Ranking (par le score)
→ Selection (top N ou déciles)
→ Weights (stratégies equal wieght, market cap, etc ...)
→ Constraints Engine (recalcul des poids après application des contraintes)
→ Rebalancing Rules (recalculer les poids de facon régulière)

à partir de là, l'indice est construit
-> backtest 
-> génération d'un rapport sur l'indice

Filtres: permettent de restreindre un univers d'investissement qui peut etre énorme (milliers d'actions sur le marché)


## TO DO

réussir à récupérer une liste des actions d'un marché et transformer automatiquement cette liste en un univers
(ce qui est pour le moment fait à la main)


### attributs pour créer l'indice en lui même
self.filters = filters
self.scorer = scorer
self.selector = selector
self.weighter = weighter
self.constraints = constraints
self.rule = rule


### attributs à utiliser
self.weights
self.scores
self.ranking
self.mask

valeurs possibles pour les rebalance rules: celles des offset aliases de la freq de date range
https://pandas.pydata.org/docs/user_guide/timeseries.html#timeseries-offset-aliases