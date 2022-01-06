from utils.symbol_table import *
import utils.AST as AST
from compiler_levels.semantic.node_visitor import NodeVisitor
import config
from compiler_levels.semantic.semantic_errors import SemanticErrors
class PreProcess(NodeVisitor):


    def __init__(self):
        self.create_and_push_builtin_funcs(config.global_symbol_table)
    
    def visit_Prog1(self, node, table):
        #print(f"visiting: prog1")
        self.visit(node.func, config.global_symbol_table)

    def visit_Prog2(self, node, table):
        #print(f"visiting: prog2")
        self.visit(node.func, config.global_symbol_table)
        self.visit(node.prog, config.global_symbol_table)


    def visit_Func(self, node, table):
        #print(f"visiting: func")
        parameters = []
        flist = node.flist
        function_name= node.iden.iden_value["name"]
        if not isinstance(flist, AST.Empty):
            if flist.iden:
                parameters.append({"iden": flist.iden, "type": flist.type})
            while hasattr(flist, "flist"):
                flist = flist.flist
                if (not isinstance(flist, AST.Empty)):
                    parameters.append({"iden": flist.iden, "type": flist.type})
        parameters.reverse()
        name = node.iden.iden_value["name"]

        function_symbol = FunctionSymbol(name, node.type, parameters)
        if not table.put(function_symbol):
            # if there is a function or var with the same identifier
            SemanticErrors.add_error({"message":f"{node.flist.lineno}: identifier '{name}' already exists", "lineno":node.flist.lineno})
            return
        function_body_table = SymbolTable(table, function_name+"_function_body_block_table")
        for par in parameters:
            name = par["iden"].iden_value["name"]
            type = par["type"].type_value["name"]
            #print(f"funcion {function_name}'s arg: name: '{name}', type: {type}'" )
            if not function_body_table.put(VariableSymbol(name, type)):
                SemanticErrors.add_error({"message": f'{node.flist.lineno}: \'{name}\' already defined', "lineno": node.flist.lineno})
        self.visit(node.body, function_body_table)
        

    def visit_Body1(self, node, table):
        #print(f"visiting: body1")
        self.visit(node.stmt, table)
            


    def visit_Body2(self, node, table):
        #print(f"visiting: body2")
        self.visit(node.stmt, table)
        self.visit(node.body, table)


    def visit_Stmt1(self, node, table):
        #print(f"visiting: stmt1")
        pass            

    def visit_Stmt2(self, node, table):
        #print(f"visiting: stmt2")
        self.visit(node.defvar, table)


    def visit_Stmt3(self, node, table):
        #print(f"visiting: stmt3")
        if_block_symbol_table = SymbolTable(table, "if_block") # symbol table for "if" block
        self.visit(node.stmt, if_block_symbol_table)


    def visit_Stmt4(self, node, table):
        #print(f"visiting: stmt4")
        if_block_symbol_table = SymbolTable(table, "if_block") # symbol table for "if" block
        self.visit(node.stmt, if_block_symbol_table)
        else_block_symbol_table = SymbolTable(table, "else_block") # symbol table for "else" block
        self.visit(node.stmt2, else_block_symbol_table)


    def visit_Stmt5(self, node, table):
        #print(f"visiting: stmt5")
        do_block_symbol_table = SymbolTable(table, "do_block") # symbol table for "do" block of a while
        self.visit(node.stmt, do_block_symbol_table)


    def visit_Stmt6(self, node, table):
        #print(f"visiting: stmt6")
        foreach_block_symbol_table = SymbolTable(table, "foreach_block") # symbol table for "foreach" block
        name = node.iden.iden_value["name"]
        type = "Int"
        iden = VariableSymbol(name, type)
        foreach_block_symbol_table.put(iden)
        self.visit(node.stmt, foreach_block_symbol_table)


    def visit_Stmt7(self, node, table):
        #print(f"visiting: stmt7")
        pass

    def visit_Stmt8(self, node, table):
        #print(f"visiting: stmt8")
        body_block_symbol_table = SymbolTable(table, "body_block") # symbol table for "body" block
        self.visit(node.body, body_block_symbol_table)

    
    def visit_Defvar(self, node, table):
        #print(f"visiting: defvar")
        name = node.iden.iden_value["name"]
        type = node.type.type_value["name"]
        if not table.put(VariableSymbol(name, type)):
                SemanticErrors.add_error({"message": f'{node.iden.lineno}: \'{name}\' already defined', "lineno":node.iden.lineno})
        self.visit(node.iden, table)
        self.visit(node.type, table)

            

 

    def visit_Type(self, node, table):
        #print(f"visiting: type")
        pass


    def visit_Iden(self, node, table):
        #print(f"visiting: iden")
        pass

    def visit_Empty(self, node, table):
        #print(f"visiting: empty")
        pass



    def create_and_push_builtin_funcs(self, table):
        getInt_function_symbol = FunctionSymbol("getInt", "Int", [] )
        table.put(getInt_function_symbol)

        printInt_funcition_symbol = FunctionSymbol("printInt", "Int", [{"iden": "n", "type": "Int"}] )
        table.put(printInt_funcition_symbol)

        createArray_funcition_symbol = FunctionSymbol("createArray", "Array", [{"iden": "n", "type": "Int"}] )
        table.put(createArray_funcition_symbol)

        arrayLength_funcition_symbol = FunctionSymbol("arrayLength", "Int", [{"iden": "v", "type": "Int"}] )
        table.put(arrayLength_funcition_symbol)

        exit_funcition_symbol = FunctionSymbol("exit", "Int", [{"iden": "n", "type": "Int"}] )
        table.put(exit_funcition_symbol)
