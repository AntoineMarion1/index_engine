"""Module pour créer une métrique de backtest"""

class Metric:
    """
    Un nom et une valeur
    """
    def __init__(self, name: str, value: float):
        self.name = name
        self.value = value