import ply.yacc as yacc

class Parser(object):
    def __init__(self, Grammer):
        self.parser = yacc.yacc(debug=True, module= Grammer)

    def build(self, data):
        self.parser.parse(data)

