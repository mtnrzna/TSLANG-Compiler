from os import error


class SymbolTable:
    def __init__(self, parent_table = None):
        if parent_table:
            self.parent_table = parent_table
        self.variables = [] 
        self.functions = []
    
   

    def add_var(self, id, type, value):
        result = self.check_if_id_exist_in_this_scope(id)

        if result is False:
            var = (id , type, value)
            self.variables.append(var)
            return var
        
        # id already exists
        error = result
        print(error)
        return error
        

    def add_func(self, id, returned_type, argumants):
        result = self.check_if_id_exist_in_this_scope(id)

        if result is False:
            new_symbol_table = SymbolTable(parent_table= self)
            func = (id , returned_type, new_symbol_table, argumants)
            self.functions.append(func)
            return func
        
        # id already exists
        error = result
        print(error)
        return error
            

    def check_if_id_exist_in_this_scope(self):
        if self.get_var_in_this_scope(self, id):
            error = f"There is a variable with this id in this scope"
            return error
        elif self.get_func_in_this_scope(self, id):
            error = f"There is a function with this id in this scope"
            return error
        else: #  get_var returned False
            return False



    def get_var_in_this_scope(self, id):
        for var in list(self.variables):
            if var.id == id:
                return var
        return False

        
    def get_func_in_this_scope(self, id):
        for func in list(self.functions):
            if func.id == id:
                return func
        return False
    

    def get_var(self, id):
        for var in list(self.variables):
            if var.id == id:
                return var
        if hasattr(self, "parent_table"):
            return self.parent_table.get_var(id)
        return False
    

    def get_func(self, id):
        for func in list(self.functions):
            if func.id == id:
                return func
        if hasattr(self, "parent_table"):
            return self.parent_table.get_func(id)
        return False
