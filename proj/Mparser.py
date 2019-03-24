#!/usr/bin/python

import scanner
import ply.yacc as yacc


tokens = scanner.tokens

precedence = (
   # to fill ...
   ("nonassoc", 'IF'),
   ("nonassoc", 'ELSE'),
   ("nonassoc", 'WHILE'),
   ("right", '='),
   ("nonassoc", '<', '>', 'GREATEREQUAL','LOWEREQUAL','NOTEQUAL','EQUAL'),
   ("left",'+','-', 'DOTADD', 'DOTSUB'),
   ("left",'*','/', 'DOTMUL', 'DOTDIV'),
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

class DeclarationList(Node):
  def __init__(self):
    self.declarations = []

  def addDeclaration(self, dec):
    self.declarations.append(dec)

  def __str__(self):
    m_str = '\n'.join(map(str, self.declarations))
    return m_str

class AssignmentWithOperation(Node):
  def __init__(self, name, op, val):
    self.name = name
    self.op = op
    self.val = val

  def __str__(self):
    m_str = str(self.name) + " " + str(self.op) + " " + str(self.val)
    return m_str

class Expresion(Node):
  def __init__(self, left, op, right):
    self.left = left
    self.op = op
    self.right = right

  def __str__(self):
    m_str = str(self.left) + " " + str(self.op) + " " + str(self.right)
    return m_str 

class Condition(Node):
  def __init__(self, left, op, right):
    self.left = left
    self.op = op
    self.right = right

  def __str__(self):
    m_str = str(self.left) + " " + str(self.op) + " " + str(self.right)
    return m_str 


class Term(Node):
  def __init__(self, val):
    self.val = val

  def __str__(self):
    m_str = str(self.val)
    return m_str

class GroupedExpresion(Node):
  def __init__(self, val):
    self.val =val

  def __str__(self):
    m_str = "(" + str(self.val) + ")" 
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

class UnaryDeclaration(Node):
  def __init__(self, name, op, val):
    self.name = name
    self.op = op
    self.val = val

  def __str__(self):
    m_str = str(self.name) + "= {oper: " + str(self.op) + "} " + str(self.val)
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

class InstructionList(Node):
  def __init__(self):
    self.instructions = []

  def addInstruction(self, instr):
    self.instructions.append(instr)

  def __str__(self):
    m_str = '\n'.join(map(str, self.instructions))
    return m_str

class Instruction(Node):
  def __str__(self):
    return str(self)

class PrintInstruction(Node):
  def __init__(self, expr):
    self.expr = expr

  def __str__(self):
    m_str = "print " + str(self.expr)
    return m_str 

class ReturnInstruction(Node):
  def __init__(self, expr):
    self.expr = expr

  def __str__(self):
    m_str = "Return " + str(self.expr)
    return m_str 


class ElifInstr(Node):
  def __init__(self, cond, instr):
    self.cond = cond
    self.instr = instr

  def __str__(self):
    m_str = "Elif: " + str(self.cond) + " then: " + str(self.instr)
    return m_str 

class ElifInstrList(Node):
  def __init__(self):
    self.cases = []

  def addCase(self, case):
    self.cases.append(case)

  def __str__(self):
    m_str = ' '.join(map(str, self.cases))
    return m_str

class ElseInstr(Node):
  def __init__(self, instr):
    self.instr = instr

  def __str__(self):
    return "Else: " + str(self.instr)

class IfInstr(Node):
  def __init__(self, cond, instr, othercase):
    self.cond = cond
    self.instr = instr
    self.othercase = othercase

  def __str__(self):
    m_str = "If: " + str(self.cond) + " then: " + str(self.instr)  +" " + str(self.othercase)
    return m_str 

class WhileInstr(Node):
  def __init__(self, cond, instr):
    self.cond = cond
    self.instr = instr
  def __str__(self):
    m_str = "While: " + str(self.cond) + " then: " + str(self.instr)
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


def p_program(t):
  ''' program : instrlist'''
  t[0] = t[1]
  print(t[0])

def p_instrlist(t):
  '''instrlist : instrlist instruction
               | instruction '''
  t[0] = InstructionList()
  for x in range(len(t)-1):
    t[0].addInstruction((t[x+1]))
  #print(t[0])  

def p_instruction(t):
  ''' instruction : printinstr ';'
                  | declarationlist  
                  | ifinstr 
                  | continueinstr ';'
                  | theninstr ';' 
                  | whileinstr 
                  | returninstr ';'
                  | breakinstr ';' '''
  t[0] = t[1]

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

def p_declaration(t):
  '''declaration : ID '=' matrix ';'
                 | ID '=' valuelist ';' 
                 | ID '=' matrixfunction ";"
                 | ID '=' expression ";"
                 | ID '=' '-' ID ';'
                 | ID '=' ID "'" ';'
                 | ID ADDASSIGN expression ";"
                 | ID SUBASSIGN expression ";"
                 | ID MULASSIGN expression ";"
                 | ID DIVASSIGN expression ";"
                 | ID '[' INTNUM ',' INTNUM ']' '=' value ';' ''' #decalres one matrix cell, sth like this A[1,2] = 0;
  if len(t) == 10:
    t[0] = MatrixCellDeclatration(t[1], t[3], t[5], t[8])
  elif len(t) == 6:
    if t[3] == '-':
      t[0] = UnaryDeclaration(t[1],t[3],t[4])
    else: 
      t[0] = UnaryDeclaration(t[1],t[4],t[3])
  elif len(t) == 5:
    t[0] = AssignmentWithOperation(t[1],t[2],t[3])
  else:
    t[0] = Declaration(t[1],t[3])
  #print(t[0])

def p_ifinstr(t):
  '''ifinstr : IF '(' condition ')' instruction
             | IF '(' condition ')' '{' instrlist '}'
             | IF '(' condition ')' instruction elifinstrlist
             | IF '(' condition ')' '{' instrlist '}' elifinstrlist'''
  if len(t) == 6:
    t[0] = IfInstr(t[3],t[5],None)
  elif len(t) == 7:
    t[0] = IfInstr(t[3],t[5],t[6])
  elif len(t) == 8:
    t[0] = IfInstr(t[3],t[6],None)
  else:
    t[0] = IfInstr(t[3],t[6],t[8])
#print(t[0])

def p_elifinstrlist(t):
  '''elifinstrlist : elifinstrlist elifinstr
                   | elifinstrlist elseinstr
                   | elifinstr'''
  t[0] = ElifInstrList()
  for x in range(len(t)-1):
    t[0].addCase((t[x+1]))
  print(t[0]) 

def p_elifinstr(t):
  '''elifinstr : ELSE IF '(' condition ')' instruction
               | ELSE IF '(' condition ')' '{' instrlist '}' '''
  if len(t) == 9: 
    t[0] = ElifInstr(t[4],t[7])
  elif len(t) == 10:  
    t[0] = ElifInstr(t[4],t[7])
  else:
    t[0] = ElifInstr(t[4],t[6])
  #print(t[0]) 

def p_elseinstr(t):
  ''' elseinstr : ELSE instruction
                | ELSE '{' instrlist '}' '''
  if len(t) == 3 :
    t[0] = ElseInstr(t[2])
  else:
    t[0] = ElseInstr(t[3])

def p_whileinstr(t):
  '''whileinstr : WHILE '(' condition ')' instruction
                | WHILE '(' condition ')' '{' instrlist '}' '''
  if len(t) == 6:
    t[0] = WhileInstr(t[3], t[5])
  else:
    t[0] = WhileInstr(t[3], t[6])


def p_returninstr(t):
  '''returninstr : RETURN expression '''
  t[0] = ReturnInstruction(t[2])

def p_printinstr(t):
  '''printinstr : PRINT expression '''
  t[0] = PrintInstruction(t[2])

def p_breakinstr(t):
  '''breakinstr : BREAK '''
  t[0] = t[1]

def p_continueinstr(t):
  '''continueinstr : CONTINUE '''
  t[0] = t[1]

def p_theninstr(t):
  '''theninstr : THEN '''
  t[0] = t[1] 

def p_matrix(t):
  '''matrix : '[' matrixline ']' '''
  t[0] = Matrix()
  t[0].addLine(t[2])
  #print(t[0])

def p_matrixline(t):
  '''matrixline : matrixline ";" valuelist 
                | valuelist '''
  matrixln = MatrixLine()
  for x in range(len(t)):
    if x%2==1:
      matrixln.addInterior(t[x])
  t[0] = matrixln

def p_expression(t):
  '''expression : ID
                | value
                | condition
                | '(' expression ')'
                | expression '+' expression
                | expression '-' expression
                | expression '*' expression
                | expression '/' expression
                | expression DOTADD expression
                | expression DOTSUB expression
                | expression DOTMUL expression
                | expression DOTDIV expression'''              
  if len(t) == 2:
    t[0] = Term(t[1])
  elif len(t) == 3:
    t[0] = GroupedExpresion(t[2])
  else:
    t[0] = Expresion(t[1],t[2],t[3])     

def p_condition(t):
  '''condition : expression GREATEREQUAL expression
               | expression LOWEREQUAL expression
               | expression NOTEQUAL expression
               | expression EQUAL expression
               | expression '<' expression
               | expression '>' expression'''
  t[0] = Condition(t[1],t[2],t[3])             

def p_valuelist(t):
  '''valuelist : valuelist ',' value
               | value'''
  t[0] = ValueList()
  for x in range(len(t)-1):
    t[0].addValue(Value(t[x+1]))
  #print(*t[0].values) 

#TO_DO zeoroes, ones, eye can be changed to one instance, sth like matrix_function_label
def p_matrixfunction(t):
  '''matrixfunction : ZEROES '(' INTNUM ')'
                    | ONES '(' INTNUM ')'
                    | EYE '(' INTNUM ')' '''
  t[0] = MatrixFunction(t[1], t[3])
  #print(t[0])

def p_value(t):
  '''value : STRING
           | INTNUM
           | FLOATNUM'''
  t[0] = Value(t[1])


parser = yacc.yacc()