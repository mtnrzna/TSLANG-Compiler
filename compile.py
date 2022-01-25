from compiler_levels.lexer.tokens import Tokens
from compiler_levels.lexer.lexer import Lexer
from compiler_levels.lexer.tokens import Tokens
from compiler_levels.parser.parser import Parser
from compiler_levels.parser.grammer import Grammar
from utils.show_tree import show_tree
from compiler_levels.semantic.type_checker import TypeChecker
from compiler_levels.semantic.preprocess import PreProcess
from compiler_levels.semantic.semantic_errors import SemanticErrors
from compiler_levels.IR_generation.IR_generator import IRGenerator
import config
from utils.symbol_table import SymbolTable
from compiler_levels.IR_generation.run_tsvm import RunTSVM
from utils.color_prints import Colorprints


class Compiler(object):
    def __init__(self):
        config.global_symbol_table = SymbolTable(None, "global")
        tokens = Tokens()
        lexer = Lexer(tokens)
        Grammar.lexer = lexer.lexer # lexer attribute in lexer object of Lexer class!

        self.parser = Parser(Grammar)
        self.type_checker = TypeChecker()
        self.preprocess = PreProcess()
        self.compiled_failed = False
        self.IR_generator = IRGenerator() 
        self.run_tsvm = RunTSVM()
    


    def compile(self, data):
        #self.lexer.build(data)
        self.parser.build(data)
        #try:
        try:
            show_tree(config.syntax_tree)
        except:
            Colorprints.print_in_black("***Couldn't build the syntax tree :(***")
        #lexer errors
        if Tokens.errors != 0 and not self.compiled_failed:
            Colorprints.print_in_yellow(f"***{Tokens.errors} lexer errors detected***")
            Tokens.print_error_messages()
        elif Tokens.errors == 0 and not self.compiled_failed:
            Colorprints.print_in_green(f"***Congrats! No lexer errors!***")
        
        #parser errors
        if Grammar.errors != 0 and not self.compiled_failed:
            Colorprints.print_in_yellow(f"***{Grammar.errors} parser errors detected***")
            Grammar.print_error_messages()
        elif Grammar.errors == 0 and not self.compiled_failed:
            Colorprints.print_in_green(f"***Congrats! No parser errors!***")

        #semantic errors
        self.preprocess.visit(config.ast, None)
        self.type_checker.visit(config.ast, None)
        if SemanticErrors.errors != 0 and not self.compiled_failed:
            Colorprints.print_in_yellow(f"***{SemanticErrors.errors} semantic errors detected***")
            SemanticErrors.print_error_messages()
        elif SemanticErrors.errors == 0 and not self.compiled_failed:
            Colorprints.print_in_green(f"***Congrats! No semantic errors!***")

        #IR generartion
        if Tokens.errors == 0 and Grammar.errors == 0 and SemanticErrors.errors == 0:
            self.IR_generator.visit(config.ast, None)

            f = open(".\compiler_levels\IR_generation\generated_IR.txt", "w")
            f.write(config.IR_code)
            f.close()


            Colorprints.print_in_lightPurple("***TSLANG Terminal***")

            self.run_tsvm.run()

        else:
            self.compiled_failed = True                
        #except:
        #    self.compiled_failed = True

        if self.compiled_failed:
            Colorprints.print_in_red("!!! Compiled failed :( !!!")
