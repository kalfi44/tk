
''''
def p_program(p):
  """program : instructions"""
  p[0] = Program(None, None, p[3])

def p_initliazation(t):
  '''init : ID '=' expression ";"'''
  t[0] = Initialize(t[1],t[3])

def p_initlist(t):
  '''initlist : initlist ',' init 
              | init '''
  if len(t) == 4 :
    t[0] = Init_List() if t[1] is None else t[1]
    t[0].addInit(t[1])
  else:
    p[0] = Init_List()
    p[0].addInit(t[1])


def p_expression_assignop(t):
    '''expression : ID ADDASSIGN expression
                  | ID SUBASSIGN expression
                  | ID MULASSIGN expression
                  | ID DIVASSIGN expression'''
    t[0] = AssignOp(t[0],t[1],t[3])

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
                  | expression EQUAL expression
                  | expression ADDASSIGN expression
                  | expression SUBASSIGN expression
                  | expression MULASSIGN expression
                  | expression DIVASSIGN expression
                  | expression DOTADD expression
                  | expression DOTSUB expression
                  | expression DOTMUL expression
                  | expression DOTDIV expression  '''                                  
    if len(t) == 3:
      if t[1] == '=':
        t[0] = Initialize(t[0], t[2])
      else:
        t[0] = AssignOp(t[0],t[1],t[2])
    elif len(t) >= 4:
      t[0] = BinOp(t[1],t[2],t[3])

def p_instructions(p):
        """instructions : instructions instruction
                        | instruction """
        if len(p) == 3:
            p[0] = InstructionList() if p[1] is None else p[1]
            p[0].addInstruction(p[2])
        else:
            p[0] = InstructionList()
            p[0].addInstruction(p[1])
    
def p_instruction(p):
    """instruction : labeled_instr
                   | assignment
                   | choice_instr
                   | while_instr
                   | return_instr
                   | break_instr
                   | continue_instr"""
    p[0] = p[1]
      
def p_labeled_instr(p):
    """labeled_instr : ID ':' instruction """
    id = p[1]
    instruction = p[3]
    p[0] = LabeledInstruction(id, instruction)

def p_assignment(p):
    """assignment : ID '=' expression ';' """
    id = p[1]
    expr = p[3]
    p[0] = AssignmentInstruction(id, expr)
    
def p_choice_instr(p):
    """choice_instr : IF '(' condition ')' instruction  %prec IF
                    | IF '(' condition ')' instruction ELSE instruction
                    | IF '(' error ')' instruction  %prec IF
                    | IF '(' error ')' instruction ELSE instruction """
    condition = p[3]
    action = p[5]
    alternateAction = None if len(p) < 8 else p[7]
    p[0] = ChoiceInstruction(condition, action, alternateAction)

def p_while_instr(p):
    """while_instr : WHILE '(' condition ')' instruction
                   | WHILE '(' error ')' instruction """
    condition = p[3]
    instruction = p[5]
    p[0] = WhileInstruction(condition, instruction)

    
def p_return_instr(p):
    """return_instr : RETURN expression ';' """
    expression = p[2]
    p[0] = ReturnInstruction(expression)
    
def p_continue_instr(p):
    """continue_instr : CONTINUE ';' """
    p[0] = ContinueInstruction()
    
def p_break_instr(p):
    """break_instr : BREAK ';' """
    p[0] = BreakInstruction()

def p_condition(p):
        '''condition : expression'''
        p[0] = p[1]

def p_term(p):
    '''term : INTNUM
            | FLOATNUM
            | STRING'''
    p[0] = p[1]


'''