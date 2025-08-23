from pathlib import Path
from textual.app import App, ComposeResult
from textual.widgets import Static
from .viewer import PDFViewer


class PDFTestApp(App):
    """A simple app to test the PDFViewer."""

    def compose(self) -> ComposeResult:
        # NOTE TO USER:
        # Please replace "your_document.pdf" with the actual path to a PDF file.
        pdf_path = Path("your_document.pdf")
        if pdf_path.exists():
            yield PDFViewer(pdf_path)
        else:
            yield Static(
                "PDF file not found. Please create a file named your_document.pdf or edit src/textual_pdf_view/__init__.py and provide a valid path."
            )


def main() -> None:
    """Run the PDF test app."""
    app = PDFTestApp()
    app.run()


__all__ = ["PDFViewer"]
