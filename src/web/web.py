from dash import Dash, html

class website:
    def __init__(self, bal):
        self.app = Dash()
        self.__make_layout__(bal)

    def __make_layout__(self, bal):
        self.app.layout = [html.Div(children=f"Current Balance is {bal}")]

    def run(self, debug=False):
        self.app.run(debug=debug)