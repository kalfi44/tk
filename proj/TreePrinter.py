from __future__ import print_function
import AST

TOKEN ="| "

def addToClass(cls):
    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

class TreePrinter:
	@addToClass(AST.Program)	
	def printTree(self, indent=0):
		return self.printTree(indent+1)

	@addToClass(AST.InstructionList)	
	def printTree(self, indent=0):
		return "".join(map(lambda x: x.printTree(indent), self.instructions))

	@addToClass(AST.Instruction)	
	def printTree(self, indent=0):
		return self.printTree(indent)

	@addToClass(AST.Assignment)
	def printTree(self, indent=0):
		return TOKEN * indent + self.name + "=\n" + self.val.printTree(indent+1)

	@addToClass(AST.AssignmentList)	
	def printTree(self, indent=0):
		return "".join(map(lambda x: x.printTree(indent), self.declarations))

	@addToClass(AST.AssignmentWithOperation)
	def printTree(self, indent):
		return TOKEN * indent + self.name + self.op + "\n" + self.val.printTree(indent)

	@addToClass(AST.Expression)
	def printTree(self, indent=0):
		l_str="" 
		r_str=""
		if isinstance(self.left, str) or isinstance(self.left, int) or isinstance(self.left, float):
			l_str = TOKEN * (indent+1) + str(self.left) 
		else:
			l_str = self.left.printTree(indent+1)
		if isinstance(self.right, str) or isinstance(self.right, int) or isinstance(self.right, float):
			r_str = TOKEN * (indent+1) + str(self.right)
		else:
			r_str = self.right.printTree(indent+1)
		return TOKEN * indent + str(self.op) + "\n" + l_str + r_str

	@addToClass(AST.GroupedExpression)
	def printTree(self, indent=0):
		return self.val.printTree(indent)

	@addToClass(AST.UnaryExpression)
	def printTree(self, indent=0):
		m_str = " "
		if isinstance(self.exp, str) or isinstance(self.exp, int) or isinstance(self.exp, float):
			m_str = str(self.op) + " " + str(self.exp) + "\n"
		else:
			m_str = str(self.op) + " " + self.exp.printTree()
		return TOKEN * indent + m_str 

	@addToClass(AST.MatrixCellAssignment)
	def printTree(self, indent=0):
		return TOKEN * indent + str(self.matrixid) + "[" +str(self.row)+ ","+str(self.col)+ "]=\n" + TOKEN * (indent+1) + str(self.val) + "\n"

	@addToClass(AST.Term)
	def printTree(self, indent=0):
		if isinstance(self.val, str) or isinstance(self.val, int) or isinstance(self.val, float):
			return TOKEN * (indent) + str(self.val) + "\n"
		return self.val.printTree(indent)

	@addToClass(AST.MatrixFunction)
	def printTree(self, indent=0):
		return TOKEN * indent + self.type + "\n" + TOKEN * (indent+1) + str(self.arg) + "\n"

	@addToClass(AST.PrintInstruction)
	def printTree(self, indent=0):
		if isinstance(self.expr, str) or isinstance(self.expr, int) or isinstance(self.expr, float):
			return TOKEN * indent + "print\n" + TOKEN * (indent + 1) + str(self.expr) + "\n"
		return TOKEN * indent + "print\n" + self.expr.printTree(indent+1) + "\n"

	@addToClass(AST.PrintInstruction)
	def printTree(self, indent=0):
		if isinstance(self.expr, str) or isinstance(self.expr, int) or isinstance(self.expr, float):
			return TOKEN * indent + "print\n" + TOKEN * (indent + 1) + str(self.expr) + "\n"
		return TOKEN * indent + "print\n" + self.expr.printTree(indent+1) + "\n"

	@addToClass(AST.PrintInstruction)
	def printTree(self, indent=0):
		if isinstance(self.expr, str) or isinstance(self.expr, int) or isinstance(self.expr, float):
			return TOKEN * indent + "print\n" + TOKEN * (indent + 1) + str(self.expr) + "\n"
		return TOKEN * indent + "print\n" + self.expr.printTree(indent+1) + "\n"

	@addToClass(AST.PrintInstruction)
	def printTree(self, indent=0):
		if isinstance(self.expr, str) or isinstance(self.expr, int) or isinstance(self.expr, float):
			return TOKEN * indent + "print\n" + TOKEN * (indent + 1) + str(self.expr)
		return TOKEN * indent + "print\n" + self.expr.printTree(indent+1)

	@addToClass(AST.ForInstr)
	def printTree(self, indent=0):
		return TOKEN * indent + "FOR\n" + self.rang.printTree(indent+1) + self.instr.printTree(indent+1)

	@addToClass(AST.Range)
	def printTree(self, indent=0):
		return TOKEN * indent + str(self.id) + "\n" + TOKEN * indent + "range\n" + TOKEN * (indent+1) + str(self.s) + "\n" + TOKEN * (indent+1) + str(self.e) + "\n" 

	@addToClass(AST.ValueList)
	def printTree(self, indent=0):
		#m_str = TOKEN*indent 
		m_str = "".join(map(lambda x: x.printTree(indent), self.values))
		return m_str

	@addToClass(AST.Value)
	def printTree(self, indent=0):
		return TOKEN * indent + str(self.value) +"\n"

	@addToClass(AST.Matrix)
	def printTree(self, indent=0):
		m_str = "".join(map(lambda x: x.printTree(indent), self.lines))
		return m_str

	@addToClass(AST.MatrixLineList)
	def printTree(self, indent=0):
		m_str = "".join(map(lambda x: x.printTree(indent), self.lines))
		return m_str 

	@addToClass(AST.Condition)
	def printTree(self,indent=0):
		return TOKEN * indent + str(self.op) + "\n" + TOKEN * (indent+1) + str(self.left) + "\n" + TOKEN * (indent+1) + str(self.right) + "\n"  
	
	@addToClass(AST.WhileInstr)
	def printTree(self, indent=0):
		return TOKEN * indent + "WHILE\n" + self.cond.printTree(indent+1) + self.instr.printTree(indent+1)

	@addToClass(AST.IfInstr)
	def printTree(self, indent=0):
		if self.othercase is None:
			return TOKEN * indent + "IF\n" + self.cond.printTree(indent+1) + self.instr.printTree(indent+1) 
		else:
			return TOKEN * indent + "IF\n" + self.cond.printTree(indent+1) + self.instr.printTree(indent+1) + TOKEN * indent + "ELSE\n" + self.othercase.printTree(indent+1)


	@addToClass(AST.MatrixLine)
	def printTree(self, indent=0):
		m_str = ""
		for v in self.interior:
			m_str += str(v) + " ; "
		return  TOKEN * indent + m_str + "\n"