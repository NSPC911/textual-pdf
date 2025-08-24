import click
from textual import events
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup
from textual.widgets import Button, Footer, Input, Label

from textual_pdf.pdf_viewer import PDFViewer


class PDFTestApp(App):
    """A simple app to test the PDFViewer."""

    CSS = """
    Footer {
        background: transparent !important;
        .footer-key--key, .footer-key--description {
            background: transparent !important;
            color: black !important;
        }
    }
    VerticalGroup {
        align: center middle;
        width: auto;
        & > * {
            align-horizontal: center;
        }
    }
    HorizontalGroup * {
        border: round $accent;
        background: transparent;
        &Input#current {
            max-width: 5;
            height: 3;
            border-right: none;
            padding-left: 1;
            &:focus { background-tint: transparent !important }
            &:ansi >.input--cursor {
                background: white !important;
                color: black !important;
                text-style: none;
            }
        }
        &Button {
            max-width: 7;
            max-height: 3;
            width: 3;
            opacity: 1 !important;
            background-tint: transparent !important;
            text-opacity: 1 !important;
            border: round $primary;
            tint: transparent !important;
            &:focus {
                border: round $accent;
            }
            &:disabled {
                border: round $error-darken-3;
            }
            &.-active {
                background: transparent;
                border: round $accent-lighten-3;
            }
        }
        &Label {
            border-left: none;
            border-right: none;
        }
        &Label#total {
            border-right: round $accent;
            padding-right: 1;
        }
        &Label#empty_focusable {
            border: none !important;
            padding: 0 !important;
        }
    }
    """

    BINDINGS = [
        ("left", "key_event('prev')", "Previous Page"),
        ("right", "key_event('next')", "Next Page"),
        ("ctrl+q", "quit", "Quit"),
    ]

    ENABLE_COMMAND_PALETTE = False

    def __init__(self, pdf_path: str, render_with: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.pdf_path = pdf_path
        self.render_with = render_with

    def compose(self) -> ComposeResult:
        with VerticalGroup():
            yield PDFViewer(self.pdf_path, protocol=self.render_with)
            with HorizontalGroup():
                yield Label(id="empty_focusable")
                yield Button("<", id="prev")
                yield Input("1", id="current", compact=True)
                yield Label("/ ")
                yield Label("0", id="total")
                yield Button(">", id="next")
        yield Footer()

    def on_mount(self) -> None:
        self.pdf_viewer: PDFViewer = self.query_one(PDFViewer)
        self.pdf_viewer.can_focus = False
        self.query_one("#empty_focusable").can_focus = True
        self.focus_nothing()
        self.query_one("#total").update(str(self.pdf_viewer.total_pages))
        self.fix_buttons()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "prev":
            self.pdf_viewer.previous_page()
        elif event.button.id == "next":
            self.pdf_viewer.next_page()
        self.fix_buttons()

    def focus_nothing(self) -> None:
        self.query_one("#empty_focusable").focus()

    def fix_buttons(self) -> None:
        self.query_one("#prev").disabled = self.pdf_viewer.current_page == 0
        self.query_one("#next").disabled = (
            self.pdf_viewer.total_pages - 1 == self.pdf_viewer.current_page
        )
        self.query_one("#current").value = str(self.pdf_viewer.current_page + 1)

    def on_input_changed(self, event: Input.Changed) -> None:
        event.input.styles.max_width = len(event.value) + 3
        if (
            event.value.isnumeric()
            and self.pdf_viewer.current_page != int(event.value)
            and int(event.value) < self.pdf_viewer.total_pages
        ):
            self.pdf_viewer.current_page = int(event.value) - 1

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.focus_nothing()

    def on_key(self, event: events.Key) -> None:
        """Handle key presses."""
        if self.focused.id == "current" and event.key not in ["up", "down"]:
            if event.key == "escape":
                self.focus_nothing()
            return
        match event.key:
            case "down" | "page_down" | "right" | "j" | "l":
                event.stop()
                self.pdf_viewer.next_page()
                self.fix_buttons()
            case "up" | "page_up" | "left" | "k" | "h":
                event.stop()
                self.pdf_viewer.previous_page()
                self.fix_buttons()
            case "home" | "g":
                event.stop()
                self.pdf_viewer.go_to_start()
                self.fix_buttons()
            case "end" | "G":
                event.stop()
                self.pdf_viewer.go_to_end()
                self.fix_buttons()
            case "i":
                event.stop()
                self.query_one(Input).focus()


@click.command(help="test appplication for textual-pdf-view")
@click.argument("filename")
def main(filename: str) -> None:
    """Run the PDF test app."""
    app = PDFTestApp(filename, render_with="Auto", ansi_color=True)
    app.run()


__all__ = ["PDFViewer"]
