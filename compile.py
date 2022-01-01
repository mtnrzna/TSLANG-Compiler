from utils.file import read_from_file
from compiler_levels.lexer.build import *
from compiler_levels.parser.build import *
from utils.show_tree import show_tree




def compile(file_address):
    data = read_from_file(file_address)
    tokenize(data)
    parse(data)
    show_tree(config.syntax_tree)



