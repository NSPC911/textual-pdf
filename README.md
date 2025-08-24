# Textual PDF View

A Textual widget for viewing PDF files.

## Installation

Install the package using your package manager:

```sh
pip install textual-pdf
uv add textual-pdf
poetry add textual-pdf
```

## Usage

Here is a simple example of how to use the `PDFViewer` widget in your Textual application:

```python
from textual.app import App, ComposeResult
from textual_pdf_view.pdf_viewer import PDFViewer

class PDFApp(App):
    def compose(self) -> ComposeResult:
        yield PDFViewer("path/to/your/document.pdf")

app = PDFApp()
app.run()
```

The `PDFViewer` class also comes with an option to switch protocols

`PDFViewer` supports whatever image protocols `textual-image` supports, which are `TGP`, `Sixel`, and `Halfcell` and `Unicode`

`TGP` and `Sixel` are the most recommended to use as they allow the clearest image to be produced. `Halfcell` and `Unicode` are not readable at all, and simply exists for the fun of it.

```py
# use tgp
PDFViewer("path/to/your/document.pdf", protocol="TGP")
# autodetect (default)
PDFViewer("path/to/your/document.pdf", protocol="Auto")
```

## CLI

This package also provides a command-line interface to view PDF files directly from your terminal.

```sh
textual-pdf-view /path/to/your/document.pdf
```

## Key Bindings

| Key                                   | Action              |
| ------------------------------------- | ------------------- |
| `Down`, `Right`, `j`, `l`, `PageDown` | Go to next page     |
| `Up`, `Left`, `k`, `h`, `PageUp`      | Go to previous page |
| `PageDown`                            | Go to next page     |
| `PageUp`                              | Go to previous page |
| `Home`                                | Go to first page    |
| `End`                                 | Go to last page     |

## License

This project is licensed under the MIT License.
