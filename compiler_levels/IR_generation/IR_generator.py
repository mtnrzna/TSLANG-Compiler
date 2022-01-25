from atexit import register
from utils.symbol_table import *
import utils.AST as AST
from utils.node_visitor import NodeVisitor
import config


class IRGenerator(NodeVisitor):

    reginster_index = 0
    label_index = 0
    
    def visit_Prog1(self, node, table):
        #print(f"visiting: prog1")
        func_code = self.visit(node.func, config.global_symbol_table)
        code = func_code
        config.IR_code = self.delete_empty_lines_from_code(code)
        return code

    def visit_Prog2(self, node, table):
        #print(f"visiting: prog2")
        func_code = self.visit(node.func,config.global_symbol_table)
        prog_code = self.visit(node.prog, config.global_symbol_table)
        code = func_code +"\n"+ prog_code
        config.IR_code = self.delete_empty_lines_from_code(code)
        return code


    def visit_Func(self, node, table):
        #print(f"visiting: func")
        function_symbol = table.get(node.iden.iden_value["name"])
        function_name = function_symbol.name
        function_body_block = self.find_symbol_table(f"{function_name}_function_body_block_table", table)

        parameters = self.get_parameters(node)
        function_name= node.iden.iden_value["name"]

        self.reginster_index = 0
        for param in parameters:
            self.initiate_var_symbol_register(param, table)

        func_body_code = self.visit(node.body, function_body_block)
        code = f'''proc {function_name}
{func_body_code}'''
        return code
        
        

    def visit_Body1(self, node, table):
        #print(f"visiting: body1")
        stmt_code = self.visit(node.stmt, table)
        code = stmt_code
        if not stmt_code:
            code = ""
        else:
            code = stmt_code
        return code


    def visit_Body2(self, node, table):
        #print(f"visiting: body2")
        stmt_code = self.visit(node.stmt, table)
        body_code = self.visit(node.body, table)

        if not stmt_code:
            code = body_code
        else:
            code = f'''{stmt_code}{body_code}'''
        return code 


    def visit_Stmt1(self, node, table):
        #print(f"visiting: stmt1")
        res = self.visit(node.expr, table)
        expr_code = res["code"]
        code = expr_code
        return code
            

    def visit_Stmt2(self, node, table):
        #print(f"visiting: stmt2")
        self.visit(node.defvar, table)


    def visit_Stmt3(self, node, table):
        #print(f"visiting: stmt3")
        res = self.visit(node.expr, table)
        expr_code = res["code"]
        expr_returned_reg = res["reg"]
        if_block_symbol_table = self.find_symbol_table(f"if_block_{node.lineno}", table) # symbol table for "if" block
        stmt_code = self.visit(node.stmt, if_block_symbol_table)

        label = self.create_label()
        code = f'''{expr_code}
\tjz {expr_returned_reg}, {label}
{stmt_code}
{label}:'''

        return code

        

        


    def visit_Stmt4(self, node, table):
        #print(f"visiting: stmt4")
        res = self.visit(node.expr, table)
        expr_code = res["code"]
        expr_returned_reg = res["reg"]

        if_block_symbol_table = self.find_symbol_table(f"if_block_{node.lineno}", table) # symbol table for "if" block
        stmt_code = self.visit(node.stmt, if_block_symbol_table)

        else_block_symbol_table = self.find_symbol_table(f"else_block_{node.lineno}", table) # symbol table for "else" block
        stmt2_code = self.visit(node.stmt2, else_block_symbol_table)

        label = self.create_label()
        code = f'''{expr_code}
\tjz {expr_returned_reg}, {label}
{stmt_code}
{label}:
{stmt2_code}'''

        return code



    def visit_Stmt5(self, node, table):
        #print(f"visiting: stmt5")
        res = self.visit(node.expr, table)
        expr_code = res["code"]
        expr_returned_reg = res["reg"]

        do_block_symbol_table = self.find_symbol_table(f"do_block_{node.lineno}", table) # symbol table for "do" block of a while
        stmt_code = self.visit(node.stmt, do_block_symbol_table)

        label = self.create_label()
        code = f'''{expr_code}
\tjz {expr_returned_reg}, {label}
{stmt_code}
{label}:'''

        return code


    def visit_Stmt6(self, node, table):
        #print(f"visiting: stmt6")
        return ""
    #********************************************************



    def visit_Stmt7(self, node, table):
        #print(f"visiting: stmt7")
        res = self.visit(node.expr, table)
        expr_code = res["code"]
        expr_returned_reg = res["reg"]

        code = f'''{expr_code}
\tmov r0, {expr_returned_reg}
\tret'''
        return code
            


    def visit_Stmt8(self, node, table):
        #print(f"visiting: stmt8")
        body_block_symbol_table = self.find_symbol_table(f"body_block_{node.lineno}", table) # symbol table for "body" block
        body_code = self.visit(node.body, body_block_symbol_table)
        code = body_code
        return code

    
    def visit_Defvar(self, node, table):
        #print(f"visiting: defvar")
        name = node.iden.iden_value["name"]
        self.initiate_var_symbol_register(name, table)
        

            
    def visit_Expr1(self, node, table):
        #function call
        pass 
    #8888888888888888888888888888888888888888


    def visit_Expr2(self, node, table):
        # calling an Array
        array_iden = self.visit(node.expr, table)
        array_reg = table.get(array_iden)["reg"]

        res2 = self.visit(node.expr2, table)
        expr2_returned_code = res2["code"]
        expr2_returned_reg = res2["returned_reg"]

        tmp_reg = self.create_register()
        tmp_reg2 = self.create_register()
        tmp_reg3 = self.create_register()

        return {"reg": tmp_reg3, 
        "code" : f'''{expr2_returned_code}
\tmul {tmp_reg}, {tmp_reg}, 8
\tadd {tmp_reg2}, {array_reg}, {tmp_reg}
\ld {tmp_reg3}, {tmp_reg2}'''}




    def visit_Expr3(self, node, table):
        #print(f"visiting: expr3")
        res = self.visit(node.expr, table)
        expr_returned_code = res["code"]
        expr_returned_reg = res["reg"]

        res2 = self.visit(node.expr2, table)
        expr2_returned_code = res2["code"]
        expr2_returned_reg = res2["reg"]

        res3 = self.visit(node.expr3, table)
        expr3_returned_code = res3["code"]
        expr3_returned_reg = res3["reg"]

        
        tmp_reg = self.create_register()
        label = self.create_label()
        label2 = self.create_label()
        return {"reg": tmp_reg, 
        "code" : f'''{expr_returned_code}
\tjz {expr_returned_reg}, {label}
{expr2_returned_code}
\tmov {tmp_reg}, {expr2_returned_reg}
\jmp {label2}
{label}:
{expr3_returned_code}
\tmov {tmp_reg}, {expr3_returned_reg}
{label2}:'''}




    def visit_Expr4(self, node, table):
        #print(f"visiting: expr4")
        operator = node.oper["name"]

        res = self.visit(node.expr, table)
        expr_returned_code = res["code"]
        expr_returned_reg = res["reg"]

        res2 = self.visit(node.expr2, table)
        expr2_returned_code = res2["code"]
        expr2_returned_reg = res2["reg"]

        if operator == "=":
            return {"reg": expr_returned_reg, 
            "code" : f'''{expr_returned_code}
{expr2_returned_code}
\tmov {expr_returned_reg}, {expr2_returned_code}'''}
        
        if operator == "+":
            return {"reg": expr_returned_reg, 
            "code" : f'''{expr_returned_code}
{expr2_returned_code}
\tadd {expr_returned_reg}, {expr_returned_reg}, {expr2_returned_reg}'''}
        
        if operator == "-":
            return {"reg": expr_returned_reg, 
            "code" : f'''{expr_returned_code}
{expr2_returned_code}
\tsub {expr_returned_reg}, {expr_returned_reg}, {expr2_returned_reg}'''}

        if operator == "*":
            return {"reg": expr_returned_reg, 
            "code" : f'''{expr_returned_code}
{expr2_returned_code}
\tmul {expr_returned_reg}, {expr_returned_reg}, {expr2_returned_reg}'''}
        
        if operator == "/":
            return {"reg": expr_returned_reg, 
            "code" : f'''{expr_returned_code}
{expr2_returned_code}
\tdiv {expr_returned_reg}, {expr_returned_reg}, {expr2_returned_reg}'''}

        if operator == "%":
            return {"reg": expr_returned_reg, 
            "code" : f'''{expr_returned_code}
{expr2_returned_code}
\tmod {expr_returned_reg}, {expr_returned_reg}, {expr2_returned_reg}'''}
        
        if operator == "<":
            return {"reg": expr_returned_reg, 
            "code" : f'''{expr_returned_code}
{expr2_returned_code}
\tcmp< {expr_returned_reg}, {expr_returned_reg}, {expr2_returned_reg}'''}

        if operator == ">":
            return {"reg": expr_returned_reg, 
            "code" : f'''{expr_returned_code}
{expr2_returned_code}
\tcmp> {expr_returned_reg}, {expr_returned_reg}, {expr2_returned_reg}'''}

        if operator == "==":
            return {"reg": expr_returned_reg, 
            "code" : f'''{expr_returned_code}
{expr2_returned_code}
\tcmp= {expr_returned_reg}, {expr_returned_reg}, {expr2_returned_reg}'''}
        
        if operator == "<=":
            return {"reg": expr_returned_reg, 
            "code" : f'''{expr_returned_code}
{expr2_returned_code}
\tcmp<= {expr_returned_reg}, {expr_returned_reg}, {expr2_returned_reg}'''}

        if operator == ">=":
            return {"reg": expr_returned_reg, 
            "code" : f'''{expr_returned_code}
{expr2_returned_code}
\tcmp>= {expr_returned_reg}, {expr_returned_reg}, {expr2_returned_reg}'''}

        if operator == "!=":
            label = self.create_label()
            label2 = self.create_label()

            return {"reg": expr_returned_reg, 
            "code" : f'''{expr_returned_code}
{expr2_returned_code}
\tcmp= {expr_returned_reg}, {expr_returned_reg}, {expr2_returned_reg}
\tjz {expr_returned_reg}, {label}
\tmov {expr_returned_reg}, 0
\tjmp {label2}
{label}:
\tmov {expr_returned_reg}, 1
{label2}:'''}

        if operator == "||":
            label = self.create_label()
            label2 = self.create_label()
            label3 = self.create_label()
            
            return {"reg": expr_returned_reg, 
            "code" : f'''{expr_returned_code}
{expr2_returned_code}
\tjz {expr_returned_reg}, {label}
\tmov {expr_returned_reg}, 1
\tjmp {label3}
{label}: 
\tjz {expr2_returned_reg}, {label2}
\tmov {expr_returned_reg}, 1
\tjmp {label3}
{label2}: 
\tmov {expr_returned_reg}, 0
{label3}:'''}

        if operator == "&&":
            label = self.create_label()
            label2 = self.create_label()
            label3 = self.create_label()
            
            return {"reg": expr_returned_reg, 
            "code" : f'''{expr_returned_code}
{expr2_returned_code}
\tjz {expr_returned_reg}, {label2}
\tjz {expr2_returned_reg}, {label2}
{label}:
\tmov {expr_returned_reg}, 1
\tjmp {label3}
{label2}:
\tmov {expr_returned_reg}, 0
{label3}:'''}


    def visit_Expr5(self, node, table):
        #print(f"visiting: expr5")
        operator = node.oper["name"]

        res = self.visit(node.expr, table)
        expr_returned_code = res["code"]
        expr_returned_reg = res["reg"]


        if operator == "!":
            label = self.create_label()
            label2 = self.create_label()
            return {"reg": expr_returned_reg, 
            "code" : f'''{expr_returned_code}
\tjz {expr_returned_reg}, {label}
\tmov {expr_returned_reg}, 0
\tjmp {label2}
{label}:
\tmov {expr_returned_reg}, 1
{label2}:'''}

        if operator == "+":
            return {"reg": expr_returned_reg,
            "code" : expr_returned_code}
        
        if operator == "-":
            tmp_reg = self.create_register()
            return {"reg": expr_returned_reg,
            "code" : f'''{expr_returned_code}
\tmul {tmp_reg}, {expr_returned_reg}, 2
\tsub {expr_returned_reg}, {tmp_reg}, {expr_returned_reg}'''}



    def visit_Expr6(self, node, table):
        #print(f"visiting: expr6")
        res = self.visit(node.expr, table)
        expr_returned_code = res["code"]
        expr_returned_reg = res["reg"]
        return {"reg": expr_returned_reg,
        "code" : expr_returned_code}


    def visit_Expr7(self, node, table):
        #print(f"visiting: expr7")
        name = node.iden.iden_value["name"]
        iden_reg = table.get(name).reg
        return {"reg": iden_reg,
        "code" : ""}
        

    def visit_Expr8(self, node, table):
        #print(f"visiting: expr8")pr
        num = self.visit(node.num, table)
        num_reg = self.create_register()
        return {"reg": num_reg ,
        "code" : f'''
\tmov {num_reg}, {num}'''}
        


    # flist rules are handled inside visit_func


    def visit_Num(self, node, table):
        #print(f"visiting: num")
        num = node.num_value["name"]
        return num




    def create_and_push_builtin_funcs(self, table):
       pass

    def create_register(self):
        self.reginster_index += 1
        return f"r{self.reginster_index - 1}"

    
    def create_label(self, name=None):
        self.label_index += 1
        if name:
            return f"{name}{self.label_index - 1}"
        return f"label{self.label_index - 1}"


    def find_symbol_table(self, name, parent):
        for i in range(len(parent.children)):
            if parent.children[i].name == name:
                return parent.children[i]


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


    def initiate_var_symbol_register(self, name, table):
        var_symbol = table.get(name)
        setattr(var_symbol, "reg", self.create_register())
        self.reginster_index += 1

    
    def update_var_symbol_register(self, name, value, table):
        var_symbol = table.get(name)
        code = f"\tmov {var_symbol}, {value}"
        return code

    def delete_empty_lines_from_code(self, code):
        lines = code.split("\n")
        non_empty_lines = [line for line in lines if line.strip() != ""]
        modified_code = ""
        for line in non_empty_lines:
            modified_code += line + "\n"
        return modified_code
