from compiler_levels.lexer.tokens import Tokens
from utils.file import read_from_file
from compiler_levels.lexer.lexer import Lexer
from compiler_levels.lexer.tokens import Tokens
from compiler_levels.parser.parser import Parser
from compiler_levels.parser.grammer import Grammar
from utils.show_tree import show_tree
import config

class Compiler(object):
    tokens = Tokens()
    lexer = Lexer(tokens)
    parser = Parser(Grammar)

    def compile(self, file_address):
        data = read_from_file(file_address)
        self.lexer.build(data)
        self.parser.build(data)
        show_tree(config.syntax_tree)



