from index_engine.backtest import BacktestResult

class ReportGenerator:
    def __init__(self, result: BacktestResult):
        self.result = result
    
    def to_html(self, name: str = "report.hmtl"):
        ...

    def to_pdf(self, name: str = "report.pdf"):
        ...