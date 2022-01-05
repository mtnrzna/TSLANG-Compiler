from compiler_levels.lexer.tokens import Tokens
from utils.file import read_from_file
from compiler_levels.lexer.lexer import Lexer
from compiler_levels.lexer.tokens import Tokens
from compiler_levels.parser.parser import Parser
from compiler_levels.parser.grammer import Grammar
from utils.show_tree import show_tree
from compiler_levels.semantic.type_checker import TypeChecker
import config

class Compiler(object):
    tokens = Tokens()
    lexer = Lexer(tokens)
    Grammar.lexer = lexer.lexer # lexer attribute in lexer object of Lexer class!
    parser = Parser(Grammar)
    compiled_failed = False
    def compile(self, file_address):
        data = read_from_file(file_address)
        #self.lexer.build(data)
        self.parser.build(data)
        try:
            show_tree(config.syntax_tree)


            #lexer errors
            if Tokens.errors != 0 and not Compiler.compiled_failed:
                print(f"***{Tokens.errors} lexer errors detected***")
                Tokens.print_error_messages()
            elif Tokens.errors == 0 and not Compiler.compiled_failed:
                print(f"***Congrats! No lexer errors!***")
            
            #parser errors
            if Grammar.errors != 0 and not Compiler.compiled_failed:
                print(f"***{Grammar.errors} parser errors detected***")
                Grammar.print_error_messages()
            elif Grammar.errors == 0 and not Compiler.compiled_failed:
                print(f"***Congrats! No parser errors!***")

            #semantic errors
            type_checker = TypeChecker()
            type_checker.visit(config.ast, None)
            if TypeChecker.errors != 0 and not Compiler.compiled_failed:
                print(f"***{TypeChecker.errors} semantic errors detected***")
                TypeChecker.print_error_messages()
            elif TypeChecker.errors == 0 and not Compiler.compiled_failed:
                print(f"***Congrats! No semantic errors!***")
    
        except:
            Compiler.compiled_failed = True

        if Compiler.compiled_failed:
            print("Compiled failed with unrecoverable error/errors")

