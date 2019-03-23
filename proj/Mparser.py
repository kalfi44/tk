#!/usr/bin/python

import scanner
import ply.yacc as yacc


tokens = scanner.tokens

precedence = (
   # to fill ...
   ("nonassoc", 'IF'),
   ("nonassoc", 'ELSE'),
   ("right", '='),
   ("nonassoc", '<', '>', 'GREATEREQUAL','LOWEREQUAL','NOTEQUAL','EQUAL'),
   ("left",'+','-'),
   ("left",'*','/'),
   # to fill ...
)

class Node:
     def __init__(self,type,children=None,leaf=None):
          self.type = type
          if children:
               self.children = children
          else:
               self.children = [ ]
          self.leaf = leaf

class BinOp(Node):
  def __init__(self,left,op,right):
    self.type = "binop"
    self.left = left
    self.rigth = right
    self.op = op
    
def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


def p_expression_assignop(t):
    '''expression : ID '=' expression
                  | ID ADDASSIGN expression
                  | ID SUBASSIGN expression
                  | ID MULASSIGN expression
                  | ID DIVASSIGN expression'''
    if t[1] == '=' : t[0] = t[2]
    elif t[1] == '+='  : t[0] += t[2]
    elif t[1] == '-=': t[0] -= t[2]
    elif t[1] == '*=': t[0] *= t[2]
    elif t[1] == '/=': t[0] /= t[2]

def p_expression_binop(t):
    '''expression : term
                  | ID
                  | expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression '>' expression
                  | expression '<' expression
                  | expression GREATEREQUAL expression
                  | expression LOWEREQUAL expression
                  | expression NOTEQUAL expression
                  | expression EQUAL expression'''                                    
    if len(t) == 2:
      value = t[1]
      t[0] = value
    else:
      if t[2] == '+'  : t[0] = t[1] + t[3]
      elif t[2] == '-': t[0] = t[1] - t[3]
      elif t[2] == '*': t[0] = t[1] * t[3]
      elif t[2] ==  '/': t[0] = t[1] / t[3]
      elif t[2] ==  '<': t[0] = t[1] < t[3]
      elif t[2] ==  '>': t[0] = t[1] > t[3]
      elif t[2] == '>=': t[0] = t[1] >= t[3]
      elif t[2] ==  '<=': t[0] = t[1] <= t[3]
      elif t[2] ==  '!=': t[0] = t[1] != t[3]
      elif t[2] ==  '==': t[0] = t[1] == t[3]

def p_expression_group(t):
    'expression : "(" expression ")"'
    t[0] = t[2]

def p_term(p):
    '''term : INTNUM
            | FLOATNUM
            | STRING'''
    p[0] = p[1]

'''
def p_expression_number(t):
    """expression : INTNUM
                  | FLOATNUM"""
    t[0] = t[1]

def p_instructions_opt_1(p):
    """instructions_opt : instructions """

def p_instructions_opt_2(p):
    """instructions_opt : """

def p_instructions_1(p):
    """instructions : instructions instruction """

def p_instructions_2(p):
    """instructions : instruction """
'''

# to finish the grammar
# ....


    


parser = yacc.yacc()
