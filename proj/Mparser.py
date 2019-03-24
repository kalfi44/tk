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

class DeclarationList(Node):
  def __init__(self):
    self.declarations = []

  def addDeclaration(self, dec):
    self.declarations.append(dec)

  def __str__(self):
    m_str = '\n'.join(map(str, self.declarations))
    return m_str

class MatrixFunction(Node):
  def __init__(self, type, arg):
    self.type = type
    self.arg = arg

  def __str__(self):
    m_str = "Function: " + str(self.type) + " arg:" + str(self.arg)
    return m_str 

class Declaration(Node):
  def __init__(self, name, val):
    self.name = name
    self.val = val

  def __str__(self):
    m_str  = str(self.name) + " = " + str(self.val)
    return m_str

class Matrix(Node):
  def __init__(self):
    self.lines = []

  def addLine(self, line):
    self.lines.append(line)

  def __str__(self):
    m_str = '\n'.join(map(str, self.lines))
    return m_str

class MatrixLineList(Node):
  def __init__(self):
    self.lines = []

  def addLine(self, line):
    self.lines.append(line)

  def __str__(self):
    m_str = '\n'.join(map(str, self.lines))
    return m_str

class MatrixLine(Node):
  def __init__(self):
    self.interior = []

  def addInterior(self, interior):
    self.interior.append(interior)

  def __str__(self):
    m_str = '\n'.join(map(str, self.interior))
    return m_str

class MatrixCellDeclatration(Node):
  def __init__(self, matrixid, row, col, val):
    self.matrixid = matrixid
    self.row = row
    self.col = col
    self.val = val

  def __str__(self):
    m_str = "In matrix: " + str(self.matrixid) + ": " + " r:" + str(self.row) + " c:" + str(self.col) + ", change val to:" + str(self.val)
    return m_str

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

#helps me debug
#  for x in range(len(t)):
#    print(str(x) + " ---- " + str(t[x]))


def p_declarationlist(t):
  '''declarationlist : declarationlist declaration
                     | declaration'''
  t[0] = DeclarationList()
  if len(t) == 2:
    t[0].addDeclaration(t[1])
  else:
    for x in range(len(t)-1):
      t[0].addDeclaration(t[x+1])
  #print(t[0])

#TO DO - only matrices work as for now
def p_declaration(t):
  '''declaration : ID '=' matrix ';'
                 | ID '=' valuelist ';' 
                 | ID '=' matrixfunction ";"
                 | ID '[' INTNUM ',' INTNUM ']' '=' value ';' ''' #decalres one matrix cell, sth like this A[1,2] = 0;
  if len(t) == 10:
    t[0] = MatrixCellDeclatration(t[1], t[3], t[5], t[8])
  else:
    t[0] = Declaration(t[1],t[3])
  #print(t[0])

def p_matrix(t):
  '''matrix : '[' matrixline ']' '''
  t[0] = Matrix()
  t[0].addLine(t[2])
  #print(t[0])

#TO_DO zeoroes, ones, eye can be changed to one instance, sth like matrix_function_label
def p_matrixfunction(t):
  '''matrixfunction : ZEROES '(' INTNUM ')'
                    | ONES '(' INTNUM ')'
                    | EYE '(' INTNUM ')' '''
  t[0] = MatrixFunction(t[1], t[3])
  print(t[0])


# seems unneccesarry and only makes grammar ambigous
#def p_matrixlinelist(t):
#  '''matrixlinelist : matrixlinelist ";" matrixline
#                    | matrixline '''
#  mlist = MatrixLineList()
#  for x in range(len(t)):
#    if x%2==1:
#      mlist.addLine(t[1])
#  t[0]=mlist
#  #print(t[0])

def p_matrixline(t):
  '''matrixline : matrixline ";" valuelist 
                | valuelist '''
  matrixln = MatrixLine()
  for x in range(len(t)):
    if x%2==1:
      matrixln.addInterior(t[x])
  t[0] = matrixln

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



'''
  if t[0] == '['
    print("sss")
    interior = ValueList()
    for x in range(len(t)-1):
      interior.addValue(Value(t[x+1]))
    matrix.addInterior(interior)
  else:
    interior = ValueList()
    for x in range(len(t)-1):
      interior.addValue(Value(t[x]))
    matrix.addInterior(interior)
  t[0] = matrix
  print(*t[0].interior, sep = ", ")
'''

parser = yacc.yacc()