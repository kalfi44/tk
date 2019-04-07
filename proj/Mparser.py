#!/usr/bin/python

import scanner
import AST
import TreePrinter
import ply.yacc as yacc

#Do porawy:
#zmodyfikować gramatykę
#DONE - dodać unarne 
#DONE - ify, elsy, while - instr i { instr } mozna uogólnić - did
#DONE - nazwa declaration jest myląca byc może expression/assigment będzie lepsza
#DONE - poprawic również same expresiion tak aby jego kosztem zmienić - zrobić bardziej kompatkowym assignment 
 
tokens = scanner.tokens

precedence = (
   # to fill ...
   ("nonassoc", 'IF'),
   ("nonassoc", 'ELSE'),
   ("nonassoc", 'WHILE'),
   ("right", '=', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN'),
   ("nonassoc", '<', '>', 'GREATEREQUAL','LOWEREQUAL','NOTEQUAL','EQUAL'),
   ("left",'+','-', 'DOTADD', 'DOTSUB'),
   ("left",'*','/', 'DOTMUL', 'DOTDIV'),
   # to fill ...
)

def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(t):
  ''' program : instrlist'''
  t[0] = t[1]
  #print(t[0])
  print(t[0].printTree())

def p_instrlist(t):
  '''instrlist : instrlist instruction
               | instruction '''
  t[0] = AST.InstructionList()
  for x in range(len(t)-1):
    t[0].addInstruction((t[x+1]))
  #print(t[0])#t[0].printTree()  

def p_instruction(t):
  ''' instruction : printinstr ';'
                  | assignmentlist  
                  | ifinstr 
                  | continueinstr ';'
                  | theninstr ';' 
                  | whileinstr 
                  | forinstr
                  | returninstr ';'
                  | breakinstr ';' '''
  t[0] = t[1]
  #print(t[0])

def p_assignmentlist(t):
  '''assignmentlist : assignmentlist assignment
                     | assignment'''
  t[0] = AST.AssignmentList()
  if len(t) == 2:
    t[0].addAssignment(t[1])
  else:
    for x in range(len(t)-1):
      t[0].addAssignment(t[x+1])
  #print(t[0])

def p_assignment(t):
  '''assignment : ID '=' expression ";"
                 | ID ADDASSIGN expression ";"
                 | ID SUBASSIGN expression ";"
                 | ID MULASSIGN expression ";"
                 | ID DIVASSIGN expression ";"
                 | ID '[' INTNUM ',' INTNUM ']' '=' value ';' ''' #decalres one matrix cell, sth like this A[1,2] = 0;
  if len(t) == 10:
    t[0] = AST.MatrixCellAssignment(t[1], t[3], t[5], t[8])
  elif len(t) == 5:
    if t[2] == "=":
      t[0] = AST.Assignment(t[1],t[3])
    else:
      t[0] = AST.AssignmentWithOperation(t[1],t[2],t[3])
  #print(t[0])

def p_ifinstr(t):
  '''ifinstr : IF '(' condition ')' groupedinstr
             | IF '(' condition ')' groupedinstr ELSE groupedinstr'''
  if len(t) == 6:
    t[0] = AST.IfInstr(t[3],t[5],None)
  else:
    t[0] = AST.IfInstr(t[3],t[5],t[7])
  #print(t[0])

def p_whileinstr(t):
  '''whileinstr : WHILE '(' condition ')' groupedinstr '''
  t[0] = AST.WhileInstr(t[3], t[5])

def p_forinstr(t):
  '''forinstr : FOR range groupedinstr '''
  t[0] = AST.ForInstr(t[2], t[3])
  

def p_groupedinstr(t):
  '''groupedinstr : '{' instrlist '}' 
                  | instruction'''
  if len(t) == 2:
    t[0] = t[1]
  else: 
    t[0] = t[2]

def p_returninstr(t):
  '''returninstr : RETURN expression '''
  t[0] = AST.ReturnInstruction(t[2])

def p_printinstr(t):
  '''printinstr : PRINT expression '''
  t[0] = AST.PrintInstruction(t[2])

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
  t[0] = AST.Matrix()
  t[0].addLine(t[2])
  #print(t[0])

def p_matrixline(t):
  '''matrixline : matrixline ";" valuelist 
                | valuelist '''
  matrixln = AST.MatrixLine()
  for x in range(len(t)):
    if x%2==1:
      matrixln.addInterior(t[x])
  t[0] = matrixln

def p_expression(t):
  '''expression : ID
                | condition
                | matrix
                | valuelist
                | matrixfunction
                | '-' expression 
                | expression "'" 
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
    t[0] = AST.Term(t[1])
  elif len(t) == 3:
    if t[1] == "-":
      t[0] = AST.UnaryExpression(t[2],t[1])
    else:
      t[0] = AST.UnaryExpression(t[1],t[2])
  elif len(t) == 4:
    if t[1] == "(":
      t[0] = AST.GroupedExpression(t[2])
    else:
      t[0] = AST.Expression(t[1],t[2],t[3])     
  #print(t[0])

def p_condition(t):
  '''condition : expression GREATEREQUAL expression
               | expression LOWEREQUAL expression
               | expression NOTEQUAL expression
               | expression EQUAL expression
               | expression '<' expression
               | expression '>' expression'''
  t[0] = AST.Condition(t[1],t[2],t[3])             

def p_range(t):
  """range : ID "=" INTNUM ":" INTNUM"""
  t[0] = AST.Range(t[1],t[3],t[5])

def p_valuelist(t):
  '''valuelist : valuelist ',' value
               | value'''
  t[0] = AST.ValueList()
  for x in range(len(t)-1):
    t[0].addValue(AST.Value(t[x+1]))
  #print(*t[0].values) 

#TO_DO zeoroes, ones, eye can be changed to one instance, sth like matrix_function_label
def p_matrixfunction(t):
  '''matrixfunction : ZEROES '(' INTNUM ')'
                    | ONES '(' INTNUM ')'
                    | EYE '(' INTNUM ')' '''
  t[0] = AST.MatrixFunction(t[1], t[3])
  #print(t[0])

def p_value(t):
  '''value : STRING
           | INTNUM
           | FLOATNUM'''
  t[0] = AST.Value(t[1])


parser = yacc.yacc()