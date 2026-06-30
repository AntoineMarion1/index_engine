from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

class ReportGenerator:

    def __init__(self, result):
        self.result = result

    def _render_html(self) -> str:
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("template.html")

        return template.render(
            index_name=self.result.name,
            cagr = self.result.metrics[0],
            metrics=self.result.metrics,
            chart_perf=self.result.plot_returns(display=False),
            chart_drawdown = self.result.plot_drawdown(display = False)
        )

    def to_html(self, name: str = "report.html") -> None:
        html = self._render_html()
        Path(name).write_text(html, encoding="utf-8")

    def to_pdf(self, name: str = "report.pdf") -> None:
        html = self._render_html()
        HTML(string=html).write_pdf(name)