from utils.file import read_from_file
from compiler_levels.lexer.build import tokenize
from compiler_levels.parser.build import parse
from utils.AST import tree


def compile(file_address):
    data = read_from_file(file_address)
    tokenize(data)
    parse(data)
    tree.show()

