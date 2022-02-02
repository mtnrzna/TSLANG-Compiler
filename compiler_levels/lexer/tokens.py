class Tokens(object):

    def __init__(self, lexer_messages):
        self.lexer_messages = lexer_messages

    # List of token names.   This is always required
    reserved = {
        'function': 'FUNCTION',
        'returns': 'RETURNS',
        'end': 'END',
        'if': 'IF',
        'else': 'ELSE',
        'while': 'WHILE',
        'do': 'DO',
        'foreach': 'FOREACH',
        'of': 'OF',
        'return': 'RETURN',
        'val': 'VAL',
        'Int': 'INT',
        'Array': 'ARRAY',
        'Nil': 'NIL'
    }

    tokens = [
        'ID',
        'NUMBER',
        'EQUAL_EQUAL',  # ==
        'EXCL_EQUAL',  # !=
        'SMALL_EQUAL',  # <=
        'BIG_EQUAL',  # >=
        'PIPE_PIPE',  # !!
        'AMP_AMP',  # &&
        'EQUAL',
        'PLUS',
        'MINUS',
        'MULTIPLY',
        'DIVIDE',
        'PERCENT',
        'SMALL',  # <
        'BIG',  # >
        'QUEST_MARK',  # ?
        'EXCL_MARK',  # !
        'COLON',
        'SEMICOLON',
        'COMMA',
        'LBRACKET',  # [
        'RBRACKET',  # ]
        'LPARANT',  # (
        'RPARANT',  # )
        ] + list(reserved.values())

    # Regular expression rules for simple tokens
    t_EQUAL_EQUAL = r'=='
    t_EXCL_EQUAL = r'!='
    t_SMALL_EQUAL = r'<='
    t_BIG_EQUAL = r'>='
    t_PIPE_PIPE = r'\|\|'
    t_AMP_AMP = r'&&'
    t_EQUAL = r'='
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_MULTIPLY = r'\*'
    t_DIVIDE = r'/'
    t_PERCENT = r'%'
    t_SMALL = r'<'
    t_BIG = r'>'
    t_QUEST_MARK = r'\?'
    t_EXCL_MARK = r'!'
    t_COLON = r':'
    t_SEMICOLON = r';'
    t_COMMA = r','
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_LPARANT = r'\('
    t_RPARANT = r'\)'


    # A regular expression rule with some action code
    def t_ID(self, t):
        r"""[a-zA-Z_][a-zA-Z_0-9]*"""
        t.type = self.reserved.get(t.value, 'ID')
        return t


    def t_NUMBER(self, t):
        r"""\d+"""
        t.value = int(t.value)
        return t


    # Comment: defining a token rule that returns no value
    def t_COMMENT(self, t):
        r"""--[^\n]*"""  # $ is for when the code ends with a comment
        pass


    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r"""\n+"""
        t.lexer.lineno += len(t.value)


    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'


    # Error handling rule
    def t_error(self, t):
        self.lexer_messages.add_message({"message":f"Illegal character '{t.value[0]}'","lineno": t.lexer.lineno})
        t.lexer.skip(1)
