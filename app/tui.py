from textual.app import App
from textual.widgets import Footer, Header


class PyDCBApp(App):
    BINDINGS = [
        ("t", "toggle_dark", "Dark Mode"),
    ]

    def compose(self):
        yield Header()
        yield Footer()

    def on_mount(self):
        self.title = "PyDCB"
        self.sub_title = "A Python-based Development Container Builder App"

    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )
