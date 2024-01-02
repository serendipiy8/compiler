import ply.lex as lex

#define lexical unit

# 词法分析器
reserved = {
    'int': 'INTEGER',
    'char': 'CHAR',
    'float': 'FLOAT',
    'double': 'DOUBLE',
}

tokens = [
    'IDENTIFIER', 'CONSTANT', 'STRING_CONSTANT',
    'PLUS', 'MINUS', 'MUL', 'DIV', 'MOD', 'INCREMENT', 'DECREMENT',
    'ASSIGN',
    'EQUALS', 'NOT_EQUALS', 'LESS_THAN', 'GREATER_THAN', 'LESS_EQUALS', 'GREATER_EQUALS',
    'LOGICAL_NOT', 'LOGICAL_OR', 'LOGICAL_AND',
    'BITWISE_OR', 'BITWISE_XOR', 'BITWISE_AND', 'SHIFT_LEFT', 'SHIFT_RIGHT', 'BITWISE_NOT',
    'COLON', 'CONDITIONAL_OPERATOR',
    'COMMA',
    'OPEN_PAREN', 'CLOSE_PAREN',
    'OPEN_BRACKET', 'CLOSE_BRACKET',
    'OPEN_BRACE', 'CLOSE_BRACE',
    'TIMES',
    'SEMICOLON',
    'DOT', 'ARROW',
] + list(reserved.values())

t_PLUS = r'\+'
t_MUL = r'\*'
t_DIV = r'/'
t_MOD = r'%'
t_INCREMENT = r'\+\+'
t_DECREMENT = r'--'
t_ASSIGN = r'='
t_EQUALS = r'=='
t_NOT_EQUALS = r'!='
t_LESS_THAN = r'<'
t_GREATER_THAN = r'>'
t_LESS_EQUALS = r'<='
t_GREATER_EQUALS = r'>='
t_LOGICAL_NOT = r'!'
t_LOGICAL_OR = r'\|\|'
t_LOGICAL_AND = r'&&'
t_BITWISE_OR = r'\|'
t_BITWISE_XOR = r'\^'
t_BITWISE_AND = r'&'
t_SHIFT_LEFT = r'<<'
t_SHIFT_RIGHT = r'>>'
t_BITWISE_NOT = r'~'
t_COLON = r':'
t_CONDITIONAL_OPERATOR = r'\?'
t_COMMA = r','
t_OPEN_PAREN = r'\('
t_CLOSE_PAREN = r'\)'
t_OPEN_BRACKET = r'\['
t_CLOSE_BRACKET = r'\]'
t_OPEN_BRACE = r'\{'
t_CLOSE_BRACE = r'\}'
t_SEMICOLON = r';'
t_DOT = r'\.'
t_ARROW = r'->'
t_TIMES = r'\*'

t_ignore = ' \t'

def t_MINUS(t):
    r'-'
    return t

def t_NewLine(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_CONSTANT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING_CONSTANT(t):
    r'"[^"]*"'
    return t

def t_FLOAT(t):
    r'-?\d+(\.\d+)?'
    t.value = float(t.value)
    return t

def t_DOUBLE(t):
    r'double'
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()

