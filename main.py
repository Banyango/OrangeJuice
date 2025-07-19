from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static


class OrangeJuiceApp(App):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Welcome to OrangeJuice CLI!")
        yield Footer()


if __name__ == "__main__":
    OrangeJuiceApp().run()
