from pathlib import Path

import fitz
import textual_image.widget as timg
from PIL import Image as PILImage
from textual import events
from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import var


class PDFViewer(Container):
    """A PDF viewer widget."""

    CSS = """
    Container {
        height: 1fr;
        width: auto;
        Image {
            width: auto;
            height: auto;
        }
    }
    """

    current_page: var[int] = var(0)

    def __init__(self, path: str | Path, renderable: str = "Auto", *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        assert renderable in ["Auto", "TGP", "Sixel", "Halfcell", "Unicode"]
        self.doc: fitz.Document | None = None
        self.renderable = renderable
        self.path = path
        self._cache: dict[int, PILImage.Image] = {}

    def on_mount(self) -> None:
        """Load the PDF when the widget is mounted."""
        self.doc = fitz.open(self.path)
        self.render_page()
        self.can_focus = True

    def compose(self) -> ComposeResult:
        yield timg.__dict__[self.renderable + "Image"](
            PILImage.new("RGB", (self.size.width, self.size.height)), id="pdf-image"
        )

    def _render_current_page_pil(self) -> PILImage.Image:
        """Renders the current page and returns a PIL image.
        Returns:
            PIL.Image: a valid PIL image

        Raises:
            RuntimeError: when a document isn't opened before this function was called, by any means
        """
        if not self.doc:
            raise RuntimeError("_render_current_page_pil was called before a document was opened.")

        if self.current_page in self._cache:
            return self._cache[self.current_page]

        page = self.doc.load_page(self.current_page)
        pix = page.get_pixmap()
        mode = "RGBA" if pix.alpha else "RGB"
        image = PILImage.frombytes(mode, (pix.width, pix.height), pix.samples)
        self._cache[self.current_page] = image
        return image

    def render_page(self) -> None:
        """Renders the current page and updates the image widget.
        Raises:
            RuntimeError: when a document isn't opened before this function was called, by any means
        """
        if not self.doc:
            raise RuntimeError("render_page was called before a document was opened.")

        image_widget: timg.Image = self.query_one("#pdf-image")
        image_widget.image = self._render_current_page_pil()

    def watch_current_page(self, new_page: int) -> None:
        """Renders the new page when the current_page variable changes."""
        self.render_page()

    def on_key(self, event: events.Key) -> None:
        """Handle key presses."""
        match event.key:
            case "down" | "page_down" | "right":
                self.next_page()
                event.stop()
            case "up" | "page_up" | "left":
                self.previous_page()
                event.stop()
            case "home":
                self.go_to_start()
                event.stop()
            case "end":
                self.go_to_end()
                event.stop()

    def on_mouse_scroll_down(self, event: events.MouseScrollDown) -> None:
        self.next_page()
        event.stop()

    def on_mouse_scroll_up(self, event: events.MouseScrollUp) -> None:
        self.previous_page()
        event.stop()

    def next_page(self) -> None:
        """Go to the next page."""
        if self.doc and self.current_page < self.doc.page_count - 1:
            self.current_page += 1

    def previous_page(self) -> None:
        """Go to the previous page."""
        if self.doc and self.current_page > 0:
            self.current_page -= 1

    def go_to_start(self) -> None:
        """Go to the first page."""
        if self.doc:
            self.current_page = 0

    def go_to_end(self) -> None:
        """Go to the last page."""
        if self.doc:
            self.current_page = self.doc.page_count - 1
