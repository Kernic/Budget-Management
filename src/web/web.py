from dash import Dash, html

class website:
    def __init__(self):
        self.app = Dash()
        self.__make_layout__()

    def __make_layout__(self):
        self.app.layout = [html.Div(children="Hello World")]

    def run(self, debug=False):
        self.app.run(debug=debug)