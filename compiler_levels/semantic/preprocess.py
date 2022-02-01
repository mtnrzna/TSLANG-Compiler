from utils.symbol_table import *
import utils.AST as AST
from utils.node_visitor import NodeVisitor
import config


class PreProcess(NodeVisitor):

    def __init__(self, semantic_errors):
        self.create_and_push_builtin_funcs(config.global_symbol_table)
        self.semantic_errors = semantic_errors
    
    def visit_Prog1(self, node, table):
        #print(f"visiting: prog1")
        self.visit(node.func, config.global_symbol_table)

    def visit_Prog2(self, node, table):
        #print(f"visiting: prog2")
        self.visit(node.func, config.global_symbol_table)
        self.visit(node.prog, config.global_symbol_table)


    def visit_Func(self, node, table):
        #print(f"visiting: func")

        parameters = self.get_parameters(node)
        function_name= node.iden.iden_value["name"]


        name = node.iden.iden_value["name"]

        function_symbol = FunctionSymbol(name, node.type.type_value["name"], parameters)
        if not table.put(function_symbol):
            # if there is a function or var with the same identifier
            self.semantic_errors.add_error({"message":f"{node.flist.lineno}: identifier '{name}' already exists", "lineno":node.flist.lineno})
            return
        function_body_table = SymbolTable(table, function_name+"_function_body_block_table")
        for par in parameters:
            name = par["iden"].iden_value["name"]
            type = par["type"].type_value["name"]
            #print(f"funcion {function_name}'s arg: name: '{name}', type: {type}'" )
            if not function_body_table.put(VariableSymbol(name, type)):
                self.semantic_errors.add_error({"message": f'{node.flist.lineno}: \'{name}\' already defined', "lineno": node.flist.lineno})
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
        if_block_symbol_table = SymbolTable(table, f"if_block_{node.lineno}") # symbol table for "if" block
        self.visit(node.stmt, if_block_symbol_table)
        self.visit(node.else_choice, table)


    def visit_Else_choice1(self, node, table):
        #print(f"visiting: stmt4")
        pass


    def visit_Else_choice2(self, node, table):
        #print(f"visiting: stmt4")
        else_block_symbol_table = SymbolTable(table, f"else_block_{node.lineno}") # symbol table for "else" block
        self.visit(node.stmt, else_block_symbol_table)


    def visit_Stmt4(self, node, table):
        #print(f"visiting: stmt4")
        do_block_symbol_table = SymbolTable(table, f"do_block_{node.lineno}") # symbol table for "do" block of a while
        self.visit(node.stmt, do_block_symbol_table)


    def visit_Stmt5(self, node, table):
        #print(f"visiting: stmt5")
        foreach_block_symbol_table = SymbolTable(table, f"foreach_block_{node.lineno}") # symbol table for "foreach" block
        name = node.iden.iden_value["name"]
        type = "Int"
        iden = VariableSymbol(name, type)
        foreach_block_symbol_table.put(iden)
        self.visit(node.stmt, foreach_block_symbol_table)


    def visit_Stmt6(self, node, table):
        #print(f"visiting: stmt6")
        pass

    def visit_Stmt7(self, node, table):
        #print(f"visiting: stmt7")
        body_block_symbol_table = SymbolTable(table, f"body_block_{node.lineno}") # symbol table for "body" block
        self.visit(node.body, body_block_symbol_table)

    
    def visit_Defvar(self, node, table):
        #print(f"visiting: defvar")
        pass

            
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

        createArray_funcition_symbol = FunctionSymbol("createArray", "Array", [{"iden": "x", "type": "Int"}] )
        table.put(createArray_funcition_symbol)

        getArray_funcition_symbol = FunctionSymbol("getArray", "Array", [{"iden": "A", "type": "Array"}] )
        table.put(getArray_funcition_symbol)

        printArray_funcition_symbol = FunctionSymbol("printArray", "Array", [{"iden": "A", "type": "Array"}] )
        table.put(printArray_funcition_symbol)

        arrayLength_funcition_symbol = FunctionSymbol("arrayLength", "Int", [{"iden": "A", "type": "Array"}] )
        table.put(arrayLength_funcition_symbol)

        exit_funcition_symbol = FunctionSymbol("exit", "Int", [{"iden": "n", "type": "Int"}] )
        table.put(exit_funcition_symbol)


    def get_parameters(self, node):
        parameters = []
        flist = node.flist
        if not isinstance(flist, AST.Empty):
            if flist.iden:
                parameters.append({"iden": flist.iden, "type": flist.type})
            while hasattr(flist, "flist"):
                flist = flist.flist
                if (not isinstance(flist, AST.Empty)):
                    parameters.append({"iden": flist.iden, "type": flist.type})
        parameters.reverse()
        return parameters