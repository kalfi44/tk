#!/usr/bin/python

import scanner
import ply.yacc as yacc


tokens = scanner.tokens
'''
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
'''
class Node:
     def __init__(self,type,children=None,leaf=None):
          self.type = type
          if children:
               self.children = children
          else:
               self.children = [ ]
          self.leaf = leaf

class Program(Node):
    def __init__(self, declarations, fundefs, instructions):
        self.declarations = declarations
        self.fundefs = fundefs
        self.instructions = instructions

class BinOp(Node):
  def __init__(self, left, op, right):
    self.left = left
    self.rigth = right
    self.op = op

class Assignment(Node):
  def _init_(self, id, expr):
    self.id = id
    self.expr = expr

class AssignOp(Node):
  def __init__(self, left, op, right):
    self.left = left
    self.op = op
    self.rigth = right

class Group(Node):
  def __init__(self,interior):
    self.interior = interior

class InstructionList(Node):
    def __init__(self):
        self.instructions = []
    
    def addInstruction(self, instr):
        self.instructions.append(instr)

class LabeledInstruction(Node):
    def __init__(self, id, instr):
        self.id = id
        self.instr = instr

class AssignmentInstruction(Node):
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr

class ChoiceInstruction(Node):
    def __init__(self, condition, action, alternateAction=None):
        self.condition = condition
        self.action = action
        self.alternateAction = alternateAction

class WhileInstruction(Node):
    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction

class ReturnInstruction(Node):
    def __init__(self, expression):
        self.expression = expression

class BreakInstruction(Node):
    pass

class ContinueInstruction(Node):
    pass

class MatrixLine(Node):
  def __init__(self):
    self.interior = []

  def addInterior(self, interior):
    self.interior.append(interior)

class ValueList(Node):
  def __init__(self):
    self.values = []

  def addValue(self, value):
    self.values.append(value)

  def __str__(self):
    m_str = ' '.join(map(str, self.values))
    return m_str

class Value(Node):
  def __init__(self, value):
    self.value = value

  def __str__(self):
    m_str = str(self.value)
    return m_str

def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


def p_matrixline(t):
  '''matrixline : '[' matrixline ';' valuelist ']'
                | '[' valuelist ']' '''
  t[0] = MatrixLine()
  interior = ValueList()
  interior.addValue(t[2])
  t[0].addInterior(interior)
  print(*t[0].interior, sep = ", ")

def p_valuelist(t):
  '''valuelist : valuelist ',' value
               | value'''
  t[0] = ValueList()
  for x in range(len(t)-1):
    t[0].addValue(Value(t[x+1]))
  #print(*t[0].values) 

def p_value(t):
  '''value : STRING
           | INTNUM
           | FLOATNUM'''
  t[0] = Value(t[1])







parser = yacc.yacc()