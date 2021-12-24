import ply.lex as lex

# List of token names.   This is always required
reserved = {
    'function': 'FUNCTION',
    'returns': 'RETURNS',
    'end': 'END',
    'if': 'IF',
    'while': 'WHILE',
    'do': 'DO',
    'foreach': 'FOREACHCH',
    'return': 'RETURN',
    'Int': 'INT',
    'Array': 'ARRAY',
    'Nil': 'NIL'
}

tokens = [
    'ID',
    'NUMBER',
    'PLUS_PLUS',  # ++
    'MINUS_MINUS',  # --
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
t_PLUS_PLUS = r'\+\+'
t_MINUS_MINUS = r'--'
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
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Comment: defining a token rule that returns no value
def t_COMMENT(t):
    r'--[^\n]*\n'
    pass

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


#File
file = open("code.txt", "r")
data = file.read()

# Build the lexer
lexer = lex.lex()

lexer.input(data)

# Tokenize
'''while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok)'''
for tok in lexer:
    # print(tok)
    print(tok.value, tok.type)
