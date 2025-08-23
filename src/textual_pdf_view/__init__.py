from pathlib import Path

import click
from textual.app import App, ComposeResult
from textual.widgets import Static

from .viewer import PDFViewer


class PDFTestApp(App):
    """A simple app to test the PDFViewer."""

    def __init__(self, pdf_path: str, render_with: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.pdf_path = pdf_path
        self.render_with = render_with

    def compose(self) -> ComposeResult:
        pdf_path = Path(self.pdf_path)
        if pdf_path.exists():
            yield PDFViewer(pdf_path, renderable=self.render_with)
        else:
            yield Static(
                f"PDF file not found. Please create a file named {self.pdf_path} or provide a valid path."
            )


@click.command(help="test appplication for textual-pdf-view")
@click.argument("filename")
def main(filename: str) -> None:
    """Run the PDF test app."""
    app = PDFTestApp(filename, render_with="Auto")
    app.run()


__all__ = ["PDFViewer"]
