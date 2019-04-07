class Node:
     def __init__(self,type,children=None,leaf=None):
          self.type = type
          if children:
               self.children = children
          else:
               self.children = [ ]
          self.leaf = leaf

class Program(Node):
  def __init__(self, instrlist):
    self.instrlist = instrlist

class AssignmentList(Node):
  def __init__(self):
    self.declarations = []

  def addAssignment(self, dec):
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

class Expression(Node):
  def __init__(self, left, op, right):
    self.left = left
    self.op = op
    self.right = right

  def __str__(self):
    m_str = str(self.left) + " " + str(self.op) + " " + str(self.right)
    return m_str 

class UnaryExpression(Node):
  def __init__(self, exp, op):
    self.op = op
    self.exp = exp

  def __str__(self):
    m_str = str(self.op) + " " + str(self.exp)
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

class GroupedExpression(Node):
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

class Assignment(Node):
  def __init__(self, name, val):
    self.name = name
    self.val = val

  def __str__(self):
    m_str  = str(self.name) + " = " + str(self.val)
    return m_str

class UnaryAssignment(Node):
  def __init__(self, op, val):
    self.op = op
    self.val = val

  def __str__(self):
    m_str = "{oper: " + str(self.op) + "} " + str(self.val)
    return m_str

class Matrix(Node):
  def __init__(self):
    self.lines = []

  def addLine(self, line):
    self.lines.append(line)

  def __str__(self):
    m_str = ';'.join(map(str, self.lines))
    return m_str

class MatrixLineList(Node):
  def __init__(self):
    self.lines = []

  def addLine(self, line):
    self.lines.append(line)

  def __str__(self):
    m_str = ';'.join(map(str, self.lines))
    return m_str

class MatrixLine(Node):
  def __init__(self):
    self.interior = []

  def addInterior(self, interior):
    self.interior.append(interior)

  def __str__(self):
    m_str = ';'.join(map(str, self.interior))
    return m_str

class MatrixCellAssignment(Node):
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

class Range(Node):
  def __init__(self, id, s, e):
    self.id = id
    self.s = s
    self.e = e

  def __str__(self):
    return "for " + str(self.id) + " from " + str(self.s) + " to " + str(self.e)

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
    m_str = "While: " + str(self.cond) + " do: " + str(self.instr)
    return m_str

class ForInstr(Node):
  def __init__(self, rang, instr):
    self.rang = rang
    self.instr = instr
  def __str__(self):
    m_str = "for: " + str(self.rang) + " do: " + str(self.instr)
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