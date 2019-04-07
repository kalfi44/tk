#Jakub Kalfas 
#Teoria Kompilacji 2019 
#Zadanie 1

import sys
import ply.lex as lex

literals = "+-*/()\{\}[]';,:=<>"

t_ignore = '  \t'

reserved = {
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'for' : 'FOR',
    'break' : 'BREAK',
    'continue' : 'CONTINUE',
    'return' : 'RETURN',
    'zeroes' : 'ZEROES',
    'ones' : 'ONES',
    'print' : 'PRINT',
    'eye' : 'EYE',
 }


tokens = [
    'DOTADD',
    'DOTSUB',
    'DOTMUL',
    'DOTDIV',
    'ADDASSIGN',
    'SUBASSIGN',
    'MULASSIGN',
    'DIVASSIGN',
    'GREATEREQUAL',
    'LOWEREQUAL',
    'NOTEQUAL',
    'EQUAL',
    'FLOATNUM',
    'INTNUM',
    'ID',
    'COMMENT',
    'STRING',
] + list(reserved.values())

t_DOTADD    = r'\.\+'
t_DOTSUB   = r'\.-'
t_DOTMUL   = r'\.\*'
t_DOTDIV  = r'\./'
t_ADDASSIGN = r'\+='
t_SUBASSIGN = r'-='
t_MULASSIGN = r'\*='
t_DIVASSIGN = r'/='
t_GREATEREQUAL = r'>='
t_LOWEREQUAL = r'<='
t_NOTEQUAL = r'!='
t_EQUAL = r'=='
t_ignore_COMMENT = r'\#.*'


# A regular expression rule with some action code
def t_FLOATNUM(t):
     r'(\.\d+|\d+\.\d*)([Ee][-+]?d+)?'
     t.value = float(t.value)    
     return t

def t_INTNUM(t):
     r'\d+'
     t.value = int(t.value)    
     return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID') #Check fro reserved words
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_string(t):
    r'".*"'
    t.type = 'STRING' 
    t.value = t.value[1:-1] #cut double quotes
    return t

def t_error(t):
    print("line %d: illegal character '%s'" %(t.lineno, t.value[0]) )
    t.lexer.skip(1)

def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1



lexer = lex.lex()
fh = None
try:
    fh = open(sys.argv[1] if len(sys.argv) > 1 else "example_full.txt", "r");
    lexer.input( fh.read() )
except IOError:
    print("open error\n")
