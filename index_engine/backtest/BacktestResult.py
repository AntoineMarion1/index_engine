"""
Module contenant la classe Basktestresult.
"""

from datetime import timedelta
from io import BytesIO

import base64
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from index_engine import IndexComposition
from index_engine.universe import Universe
from index_engine.error import DateError
from index_engine.metrics import Metric

class BacktestResult:
    """
    Classe permettant de stocker les résultats d'un backtest.
    """
    def __init__(
            self,
            name: str,
            universe: Universe,
            base_date: pd.Timestamp,
            base_value: float,
            dates: pd.DatetimeIndex,
            start: pd.Timestamp,
            end: pd.Timestamp
        ):
        self.name       : str = name
        self.universe   : Universe = universe
        self.base_date  : pd.Timestamp = base_date
        self.base_value : float = base_value
        self.index_comp : dict = {}
        self.start      : pd.Timestamp = start
        self.end        : pd.Timestamp = end
        self.rebalance_dates : pd.DatetimeIndex = dates

        if self.start < self.base_date:
            raise DateError("Le début du backtest est antérieur à la date d'initialisation de l'indice")

        # calculer les jours de cotation entre start
        # et end, sachant qu'il ne faut prendre que les jours
        # de cotation en compte
        all_market_days = self.universe.get_market_days()
        self.days : pd.DatetimeIndex = all_market_days[
            (all_market_days >= self.base_date) &
            (all_market_days <= self.end)
        ]

        self.returns : pd.Series | None = None
        self.values : pd.Series | None = None
        self.metrics: list | None = None

    def add_rebalance(self, date: pd.Timestamp, index_composition: IndexComposition):
        """
        Ajouter une composition de l'indice à une date donnée.
        """
        if date in self.index_comp:
            raise ValueError(f"Il y a déjà un rebalancement qui a été calculé le {date}.")
        self.index_comp[date]=index_composition

    def compute_index_values(self)->pd.Series:
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
        self.values = self.base_value * (1 + self.returns).cumprod()

        return self.values
        
    def get_dates(self)->pd.Series:
        """
        Renvoie les dates de rebalancement du backtest.
        """
        return self.rebalance_dates
    
    def _filter_to_period(self, series: pd.Series) -> pd.Series:
        """Filtre une Series sur la période [start, end] de façon robuste,
        même si start/end ne sont pas des market days."""
        mask = (series.index >= self.start) & (series.index <= self.end)
        return series[mask]

    def plot_returns(self, display = True) -> None:
        """
        Afficher la performance de l'indice entre start et end.
        """
        # Filtrer sur [start, end] uniquement
        values  = self._filter_to_period(self.values)
        returns = self._filter_to_period(self.returns)

        _, ax1 = plt.subplots(figsize=(12, 6))

        ax1.plot(values.index, values, color="blue", label="Indice")
        ax1.set_ylabel("Valeur de l'indice", color="blue")
        ax1.tick_params(axis="y", labelcolor="blue")

        ax2 = ax1.twinx()
        ax2.plot(returns.index, returns * 100, color="green", label="Perf (%)")
        ax2.set_ylabel("Performance (%)", color="green")
        ax2.tick_params(axis="y", labelcolor="green")

        plt.title("Indice : valeur vs performance")
        plt.grid(True)

        if display: 
            plt.show()
        else:
            # ← Remplace plt.show() par ça
            buf = BytesIO()
            plt.savefig(buf, format="png", bbox_inches="tight")
            plt.close()  # Libère la mémoire
            chart_b64 = base64.b64encode(buf.getvalue()).decode()
            return chart_b64
        
    def plot_drawdown(self, display = True):
        """
        Affiche le graphique du drawdown de la série des valeurs.
        """
        running_max = self.values.cummax()
        drawdown = 100*(self.values / running_max - 1)

        _, ax1 = plt.subplots(figsize=(12, 6))

        ax1.plot(self.values.index, drawdown, color="red", label="Drawdown")
        ax1.set_ylabel("Drawdown (%)", color="blue")
        ax1.tick_params(axis="y", labelcolor="blue")

        plt.title("Drawdown de l'indice")
        plt.grid(True)

        if display:
            plt.show()
        else:
            buf = BytesIO()
            plt.savefig(buf, format="png", bbox_inches="tight")
            plt.close()  # Libère la mémoire
            chart_b64 = base64.b64encode(buf.getvalue()).decode()
            return chart_b64

    def plot_weights(self) -> None:
        """
        Afficher la composition de l'indice en focntion du temps.
        """
        weights_dict = {}
        for date, comp in self.index_comp.items():
            if self.start <= date <= self.end:   # ← ignorer les rebalancements avant start
                weights_dict[date] = comp.get_weights()

        df = pd.DataFrame(weights_dict).T
        df = df.fillna(0.0)

        _, ax = plt.subplots(figsize=(12, 6))
        df.plot(kind="bar", stacked=True, ax=ax, colormap="tab20")

        ax.set_title("Composition de l'indice à chaque rebalancement")
        ax.set_xlabel("Date de rebalancement")
        ax.set_ylabel("Poids")
        ax.legend(loc="upper right", bbox_to_anchor=(1.15, 1), fontsize=8)
        ax.set_xticklabels([str(d.date()) for d in df.index], rotation=45, ha="right")
        plt.tight_layout()
        plt.show()

    def compute_metrics(self) -> None:
        """
        Affiche les métriques principales: performance totale, 
        yield annuel, volatilité annuelle.
        """
        # Filtrer sur [start, end] uniquement
        values  = self._filter_to_period(self.values)
        returns = self._filter_to_period(self.returns)

        total_return = values.iloc[-1] / values.iloc[0] - 1
        nb_years     = (values.index[-1] - values.index[0]).days / 365.25

        cagr = (values.iloc[-1] / values.iloc[0]) ** (1 / nb_years) - 1
        vol  = returns.std() * np.sqrt(252)
        max_drawdown = - (self.values / self.values.cummax() - 1).min()

        print(f"Total return                 = {100 * total_return:.2f}%")
        print(f"Compound Annual Growth Rate  = {100 * cagr:.2f}%")
        print(f"Annual Volatility            = {100 * vol:.2f}%")
        print(f"Maximum Drawdown             = {100 * max_drawdown:.2f}%")

        self.metrics = [
            Metric("Compound Annual Growth Rate", cagr),
            Metric("Total return", total_return),
            Metric("Annual Volatility", vol),
            Metric("Maximum Drawdown", max_drawdown)
        ]
