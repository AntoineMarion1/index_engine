from index_engine import IndexComposition
from index_engine.universe import Universe
from datetime import timedelta
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class BacktestResult:
    def __init__(self, universe: Universe, dates: pd.DatetimeIndex, start: pd.Timestamp, end: pd.Timestamp):
        self.universe : Universe = universe
        self.index_comp : dict = {}
        self.start : pd.Timestamp = start
        self.end : pd.Timestamp = end
        self.rebalance_dates : pd.DatetimeIndex = dates 

        # calculer les jours de cotation entre start
        # et end, sachant qu'il ne faut prendre que les jours
        # de cotation en compte
        all_market_days = self.universe.get_market_days()
        self.days : pd.DatetimeIndex = all_market_days[
            (all_market_days >= self.start) &
            (all_market_days <= self.end)
        ]

        self.returns : pd.Series | None = None
        self.values : pd.Series | None = None
        
    def add_rebalance(self, date: pd.Timestamp, index_composition: IndexComposition):
        self.index_comp[date]=index_composition

    def _compute_index_values(self, basis: float = 100.0)->pd.Series:
        """
        Calcule la valeur de l'indice à chaque date entre 
        start et end. Renvoie une pd.Series contenant les
        valeurs de l'indice.
        """
        returns = self.universe.get_all_returns() # pd.DataFrame contenant les returns entre chaque jour

        j = 0 # indices dans les dates de rebalancement

        # Initialiser les dates utiles
        last_rebalance : pd.Timestamp = self.rebalance_dates[j]
        next_rebalance : pd.Timestamp = self.rebalance_dates[j+1]
        current_composition: IndexComposition = self.index_comp[last_rebalance]

        # Au premier jour, qui est aussi le premier jour de rebalancement,
        # la performance est de 0
        index_returns = {last_rebalance: 0.0}

        for current_date in self.days[1:]:
            # commencer à itérer au jour suivant le premier. On itère
            # sur chaque jour de marché entre start et end. current_date
            # est un pd.Timestamp
            
            # On commence par calculer le rendement
            weights = current_composition.get_weights() # poids à la date courante
            returns_at_date = returns.loc[current_date] # returns à la date courante

            # Aligner sur les actifs communs
            common = weights.index.intersection(returns_at_date.index)
            if common.empty:
                raise ValueError(
                    f"Aucun actif en commun à {current_date}.\n"
                    f"  weights.index    = {weights.index.tolist()}\n"
                    f"  returns.index    = {returns_at_date.index.tolist()}"
                )
            # print(weights)
            # print(returns_at_date)
            
            index_return = (weights * returns_at_date).sum() # somme pondérée des returns
            index_returns[current_date] = index_return # sauvegarder le return de l'indice

            # Dans un second temps seulement, on met à jour la composition
            # de l'indice -> rebalancement à la clôture (car on regarde toujours
            # les prix de clôture).
            if current_date >= next_rebalance:
                    # on est à la date de rebalancement, il faut
                    # donc modifier la date du dernier rebalance
                    # ainsi que la composition actuelle de l'indice
                    # ATTENTION: iL FAUT GÉRER LE CAS DU DERNIER REBALANCE
                    # en attribuant la date end + 1 jour si on est après le dernier 
                    # rebalancement
                    j += 1 # passer à la date de rebalancement suivante
                    
                    last_rebalance = self.rebalance_dates[j]

                    if j + 1 < len(self.rebalance_dates):
                        next_rebalance = self.rebalance_dates[j + 1]
                    else:
                        next_rebalance = self.end + timedelta(days=1)

                    current_composition: IndexComposition = self.index_comp[last_rebalance]
        # créer la series des returns
        self.returns = pd.Series(index_returns)
        # calculer les I(t+1) = I(t)*R(t, t+1)
        self.values = basis * (1 + self.returns).cumprod()

        return self.values
        
    def get_dates(self)->pd.Series:
        return self.rebalance_dates
    
    def plot_returns(self)->None: 
        fig, ax1 = plt.subplots(figsize=(12, 6))

        # Série 1 : valeur de l'indice
        ax1.plot(self.values.index, self.values, color="blue", label="Indice")
        ax1.set_ylabel("Valeur de l'indice", color="blue")
        ax1.tick_params(axis="y", labelcolor="blue")

        # Axe secondaire
        ax2 = ax1.twinx()

        # Série 2 : performance
        ax2.plot(self.returns.index, self.returns * 100, color="green", label="Perf (%)")
        ax2.set_ylabel("Performance (%)", color="green")
        ax2.tick_params(axis="y", labelcolor="green")

        plt.title(f"Indice : valeur vs performance")
        plt.grid(True)
        plt.show()

    def plot_weights(self) -> None:
        # Construire un DataFrame : lignes = dates de rebalancement, colonnes = tickers
        weights_dict = {}
        for date, comp in self.index_comp.items():
            weights_dict[date] = comp.get_weights()
        
        df = pd.DataFrame(weights_dict).T  # shape : (n_dates, n_tickers)
        df = df.fillna(0.0)

        # Bar chart empilé
        fig, ax = plt.subplots(figsize=(12, 6))
        df.plot(kind="bar", stacked=True, ax=ax, colormap="tab20")

        ax.set_title("Composition de l'indice à chaque rebalancement")
        ax.set_xlabel("Date de rebalancement")
        ax.set_ylabel("Poids")
        ax.legend(loc="upper right", bbox_to_anchor=(1.15, 1), fontsize=8)
        ax.set_xticklabels([str(d.date()) for d in df.index], rotation=45, ha="right")
        plt.tight_layout()
        plt.show()

    def metrics(self):
        """
        Affiche les métriques principales
        """
        total_return = self.values.iloc[-1] / self.values.iloc[0] - 1
        nb_years = (self.values.index[-1] - self.values.index[0]).days / 365.25

        cagr = (self.values.iloc[-1] / self.values.iloc[0])**(1/nb_years) - 1
        vol = self.returns.std() * np.sqrt(252)

        print(f"Total return = {100*total_return:.2f}%")
        print(f"Compound Annual Growth Rate = {100*cagr:.2f}%")
        print(f"Volatility = {100*vol:.2f}%")