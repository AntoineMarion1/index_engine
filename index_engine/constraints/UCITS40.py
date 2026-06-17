from .Constraints import Constraints
from index_engine.universe import Universe
import pandas as pd
import numpy as np
import cvxpy as cp

class UCITS40(Constraints):
    def apply(self, universe: Universe, weights: pd.Series, date: pd.Timestamp)->pd.Series:
        del date
        print("====CONSTRAINTS====")

        selected = weights > 0

        w0 = weights[selected].values
        n = len(w0)

        max_weight = max(1 / n, 0.10) # permet de traiter le cas ou n < 10

        x = cp.Variable(n)

        objective = cp.Minimize(cp.sum_squares(x - w0))

        constraints = [
            cp.sum(x) == 1,
            x >= 0,
            x <= max_weight,
        ]

        # approximation UCITS 5/40 (version propre)
        if n >= 8:
            y = cp.Variable(n)
            constraints += [
                y >= x - 0.05,
                y >= 0,
                cp.sum(y) <= 0.40
            ]

        problem = cp.Problem(objective, constraints)

        # Essai avec plusieurs solveurs en cascade
        for solver in [cp.CLARABEL, cp.OSQP, cp.SCS]:
            problem.solve(solver=solver)
            if problem.status in ["optimal", "optimal_inaccurate"]:
                break

        if problem.status not in ["optimal", "optimal_inaccurate"]:
            print(f"OSQP n'a pas convergé : {problem.status}. Impossible d'appliquer UCITS40")
            print(weights)
            return weights
        
        optimized_weights = pd.Series(x.value, index=weights[selected].index)
        result = weights.copy()
        result[selected] = optimized_weights
        print(result)
        print(f"check sum: {result.sum()}")
        return result
    
    def is_satisfied(self, weights: pd.Series)->bool:
        """Vérifie que la rule est satisfaite"""
        rule_10 = (weights <= 0.10).all()
        rule_5_40 = (weights[weights>0.05].sum())<=0.40
        return rule_10 and rule_5_40