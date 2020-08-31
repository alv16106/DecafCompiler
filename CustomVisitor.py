from Grammar.DecafVisitor import DecafVisitor
from Grammar.DecafParser import DecafParser

from stack import DecafStack
from AST import ASTNode, node_enum
from symbolTable import *

class CustomVisitor(DecafVisitor):

    def __init__(self):
        self.scope = DecafStack()
        self.errors = []
        self.typeTable = TypeTable()
        self.offset = 0

    def error(self):
        self.flag = True
    
    def enterScope(self, name):
        parent = self.scope.peek()
        st = STable(name, parent=parent)
        self.scope.push(st)

    # pops the current scope off the stack
    def exitScope(self):
        if self.scope.isEmpty():
            pass
        else:
            return self.scope.pop()

    # getError method to return error message as string
    def getError(self, name):
        return "DECLARATION ERROR " + name


    #Inicio de los metodos que si hacen algo
    # Visit a parse tree produced by DecafParser#singleVar.
    def visitSingleVar(self, ctx:DecafParser.SingleVarContext):
        name = str(ctx.ID())
        scope = self.scope.peek()
        vartype = ctx.vType.getText()

        # if is inside struct
        if scope.stype == 'struct':
            # add to type table under structs name
            pass

        # if is struct declaration
        if 'struct' in vartype:
            # add struct to type table
            pass

        #else is just normal var, add symbol to table
        s = Symbol(name, vartype, self.offset)
        self.offset += self.typeTable.getSize(vartype)
        scope.add(name, s)

        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#listVar.
    def visitListVar(self, ctx:DecafParser.ListVarContext):
        name = str(ctx.ID())
        scope = self.scope.peek()
        vartype = ctx.vType.getText()

        size = int(ctx.size.getText())

        s = Symbol(name, vartype, self.offset)
        self.offset += (self.typeTable.getSize(vartype) * size)
        scope.add(name, s)

        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#structDeclaration.
    def visitStructDeclaration(self, ctx:DecafParser.StructDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#structInstantiation.
    def visitStructInstantiation(self, ctx:DecafParser.StructInstantiationContext):
        return self.visitChildren(ctx)
