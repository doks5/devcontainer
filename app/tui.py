from textual.app import App
from textual.widgets import Footer, Header
from app.dialogs.question import QuestionDialog


class PyDCBApp(App):
    CSS_PATH = "app.tcss"
    BINDINGS = [
        ("t", "toggle_dark", "Dark Mode"),
        ("q", "request_quit", "Quit"),
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

    def action_request_quit(self):
        def check_answer(accepted):
            if accepted:
                self.exit()

        self.push_screen(QuestionDialog("Do you want to exit?"), check_answer)
