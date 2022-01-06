from utils.symbol_table import *
import utils.AST as AST
from compiler_levels.semantic.node_visitor import NodeVisitor
from compiler_levels.semantic.semantic_errors import SemanticErrors
import config

class TypeChecker(NodeVisitor):

    def __init__(self):
        self.create_and_push_builtin_funcs(config.global_symbol_table)
    
    def visit_Prog1(self, node, table):
        #print(f"visiting: prog1")
        self.visit(node.func, config.global_symbol_table)

    def visit_Prog2(self, node, table):
        #print(f"visiting: prog2")
        self.visit(node.func,config.global_symbol_table)
        self.visit(node.prog, config.global_symbol_table)


    def visit_Func(self, node, table):
        #print(f"visiting: func")
        function_symbol = table.get(node.iden.iden_value["name"])
        function_name = function_symbol.name
        function_body_block = []
        for i in range(len(table.children)):
            if table.children[i].name == function_name+"_function_body_block_table":
                function_body_block = table.children[i]

        self.visit(node.body, function_body_block)

        

    def visit_Body1(self, node, table):
        #print(f"visiting: body1")
        self.visit(node.stmt, table)
            


    def visit_Body2(self, node, table):
        #print(f"visiting: body2")
        self.visit(node.stmt, table)
        self.visit(node.body, table)


    def visit_Stmt1(self, node, table):
        #print(f"visiting: stmt1")
        self.visit(node.expr, table)
            

    def visit_Stmt2(self, node, table):
        #print(f"visiting: stmt2")
        self.visit(node.defvar, table)


    def visit_Stmt3(self, node, table):
        #print(f"visiting: stmt3")
        self.visit(node.expr, table)
        if_block_symbol_table = SymbolTable(table, "if_block") # symbol table for "if" block
        self.visit(node.stmt, if_block_symbol_table)


    def visit_Stmt4(self, node, table):
        #print(f"visiting: stmt4")
        self.visit(node.expr, table)
        if_block_symbol_table = SymbolTable(table, "if_block") # symbol table for "if" block
        self.visit(node.stmt, if_block_symbol_table)
        else_block_symbol_table = SymbolTable(table, "else_block") # symbol table for "else" block
        self.visit(node.stmt2, else_block_symbol_table)


    def visit_Stmt5(self, node, table):
        #print(f"visiting: stmt5")
        self.visit(node.expr, table)
        do_block_symbol_table = SymbolTable(table, "do_block") # symbol table for "do" block of a while
        self.visit(node.stmt, do_block_symbol_table)


    def visit_Stmt6(self, node, table):
        #print(f"visiting: stmt6")
        self.visit(node.expr, table)
        foreach_block_symbol_table = SymbolTable(table, "foreach_block") # symbol table for "foreach" block
        name = node.iden.iden_value["name"]
        type = "Int"
        iden = VariableSymbol(name, type)
        foreach_block_symbol_table.put(iden)
        self.visit(node.stmt, foreach_block_symbol_table)



    def visit_Stmt7(self, node, table):
        #print(f"visiting: stmt7")
        res = self.visit(node.expr, table)
        #finding function name
        function_name = []
        while not "_function_body_block_table" in table.name and table:
            table = table.parent
            #print("checked", table.name)
        #found the function name
        if table:
            function_name = table.name.split("_function_body_block_table")[0]
            function_symbol = config.global_symbol_table.get(function_name)
            function_type = function_symbol.type.type_value["name"]
            if res != function_type:
                SemanticErrors.add_error({"message": f"{node.expr.lineno}: Returning wrong type for function '{function_name}'. must return: '{function_type}', you're returning: '{res}'", "lineno":node.expr.lineno})
        # did'nt found the corresponding function to this return
        else:
            SemanticErrors.add_error({"message": f"{node.expr.lineno}: Shouldn'n have put return here!","lineno": node.expr.lineno})
            


    def visit_Stmt8(self, node, table):
        #print(f"visiting: stmt8")
        body_block_symbol_table = SymbolTable(table, "body_block") # symbol table for "body" block
        self.visit(node.body, body_block_symbol_table)

    
    def visit_Defvar(self, node, table):
        #print(f"visiting: defvar")
        pass

            
    def visit_Expr1(self, node, table):
        #function call
        #print(f"visiting: expr1")
        function_iden = node.iden.iden_value["name"]
        function_symbol = table.get(function_iden)
        #check if function exists with this id
        # if not found, it's type automatically(in get function) is set to None
        if isinstance(function_symbol, FunctionSymbol):
            #print("function FOUND", function_iden)
            # get parameters
            #print("******", function_symbol.parameters)
            parameters = []
            for parameter in function_symbol.parameters:
                try:
                    parameter = parameter["type"].type_value["name"]
                except:
                    parameter =  parameter["type"] # this is for builtin functions
                parameters.append(parameter)
            parameters.reverse()

            # get arguments
            arguments = []
            clist = node.clist
            if not isinstance(clist, AST.Empty):
                if clist.expr:
                    res = self.visit(clist, table)
                    if not isinstance(res, str):
                        res = res.type_value["name"]
                    arguments.append(res)
                    while hasattr(clist, "clist"):
                        clist = clist.clist
                        if (not isinstance(clist, AST.Empty)):
                            res = self.visit(clist, table)
                            if not isinstance(res, str):
                                res = res.type_value["name"]
                            arguments.append(res)

            
            #print(f"{node.clist.lineno}: function: {function_iden}, arguments: {arguments}, parameters: {parameters}")
            # check number of arguments with number of parameters 
            if len(parameters) != len(arguments):
                # handle semantic error
                    SemanticErrors.add_error({"message": f"{node.clist.lineno}: Function '{function_iden}' expected {len(parameters)} arguments but got {len(arguments)} instead", "lineno": node.clist.lineno})
                    return function_symbol.type

            # check arguments types with parameters types
            for i in range(len(function_symbol.parameters)):
                par_type = parameters[i]
                arg_type = arguments[i]
                if par_type != arg_type:
                    # handle semantic error
                    SemanticErrors.add_error({"message": f"{node.clist.lineno}: {i+1}th argument of function '{function_iden}' type must be '{par_type}'", "lineno":node.clist.lineno})
                    return function_symbol.type
            # if number of arguments and their types where correct, return function iden's type
            return function_symbol.type
        

        #function is not declared but it can be called becasue of error handling, it returns "Nil"        
        else:
            #print("function not found", function_iden)
            # tries to create a symbol with function_name and type Nil
            # returns False if there is an id with that function_name

            result = table.get(function_iden, check_parent=False)
            #if there is not a var with the same name in the same scope then it would make a function that returns "Nil" in the same scope
            if not result:
                SemanticErrors.add_error({"message": f'{node.iden.lineno}: Function: \'{function_iden}\' not defined', "lineno": node.iden.lineno})
                new_declared_func_for_error_handling = FunctionSymbol(function_iden, "Nil",[])
                table.put(new_declared_func_for_error_handling)

            #if there is a var in the same scope with this name, return it's type
            else:
                SemanticErrors.add_error({"message": f'{node.iden.lineno}: \'{function_iden}\' is not a function', "lineno": node.iden.lineno})
                return result.type


    def visit_Expr2(self, node, table):
        # calling an Array
        #print(f"visiting: expr2")
        type_of_array_iden = self.visit(node.expr, table)
        type_of_array_index = self.visit(node.expr2, table)
        if type_of_array_iden == "Array" and type_of_array_index == "Int":
            return "Int"

        else:
            #print(type_of_array_iden, type_of_array_index)
            SemanticErrors.add_error({"message": f'{node.expr.lineno}: Id of the aray must of type \'Array\'!', "lineno": node.expr.lineno})
            if type_of_array_index != "Int":
                SemanticErrors.add_error({"message": f'{node.expr.lineno}: index of the array must be of type \'Int\'!', "lineno": node.expr.lineno})
            return "Nil"






    def visit_Expr3(self, node, table):
        #print(f"visiting: expr3")
        condition_expr = self.visit(node.expr, table)
        true_block_expr = self.visit(node.expr2, table)
        false_block_expr = self.visit(node.expr3, table)
        if condition_expr == "Nil":
            # Therefore condition would be false
            return false_block_expr
        return true_block_expr



    def visit_Expr4(self, node, table):
        #print(f"visiting: expr4")
        first_operand = self.visit(node.expr, table)
        second_operand = self.visit(node.expr2, table)
        operator = node.oper["name"]
        #print(f'first operand type is {first_operand} and second is {second_operand} , operand: {operator}')


        #check if it's like id = expr
        first_operand_is_iden = isinstance(node.expr, AST.Expr7)

        #dynamic type error handling! Nil type can be converted to Int or Array!
        #if operator is "=", assignment and first operand is a iden of type "Nil" you can assign anything to it
        if operator == "=" and first_operand == "Nil" and second_operand !="Nil" and first_operand_is_iden:
            first_operand_name = node.expr.iden.iden_value["name"]
            first_operand_symbol = table.get(first_operand_name)
            first_operand_symbol.type = second_operand
            first_operand = second_operand
            return second_operand

        if first_operand != second_operand:
            SemanticErrors.add_error({"message": f'{node.expr.lineno}: Two sides of \'{operator}\' must be of same type! expr1 is of type: \'{first_operand}\' and expr2 is of type: \'{second_operand}\' ', "lineno":node.expr.lineno})
            return "Nil"
        #print(f'first operand type is {first_operand} and second is {second_operand}')
        return first_operand


    def visit_Expr5(self, node, table):
        #print(f"visiting: expr5")
        #operator
        return self.visit(node.expr, table)


    def visit_Expr6(self, node, table):
        #print(f"visiting: expr6")
        return self.visit(node.expr, table)


    def visit_Expr7(self, node, table):
        #print(f"visiting: expr7")
        #search in table for the iden of this var, if not found, returns None
        result = self.visit(node.iden, table)
        if not result:
            # for error handling we should create that var
            new_declared_symbol_for_error_handling = VariableSymbol(node.iden.iden_value["name"],"Nil")
            table.put(new_declared_symbol_for_error_handling)
            return "Nil"
        return result
        

    def visit_Expr8(self, node, table):
        #print(f"visiting: expr8")pr
        return self.visit(node.num, table)


    # No need to traverse flist, It is done in function definition in preprocess


    def visit_Clist1(self, node, table):
        #print(f"visiting: clist1")
        pass


    def visit_Clist2(self, node, table):
        #print(f"visiting: clist2")
        return self.visit(node.expr, table)
        

    def visit_Clist3(self, node, table):
        #print(f"visiting: clist3")
        self.visit(node.clist, table)
        return self.visit(node.expr, table)


    def visit_Type(self, node, table):
        #print(f"visiting: type")
        pass


    def visit_Num(self, node, table):
        #print(f"visiting: num")
        return "Int" 


    def visit_Iden(self, node, table):
        #print(f"visiting: iden")
        name = node.iden_value["name"]
        symbol = table.get(name)
        if not symbol:
            SemanticErrors.add_error({"message": f"{node.lineno}: '{name}' is not declared", "lineno":node.lineno})
            new_declared_variable_for_error_handling = FunctionSymbol(name, "Nil", [])
            table.put(new_declared_variable_for_error_handling)
            return "Nil"
        return symbol.type

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
