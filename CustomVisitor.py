from Grammar.DecafVisitor import DecafVisitor
from Grammar.DecafParser import DecafParser

from stack import DecafStack
from AST import ASTNode, node_enum
from symbolTable import *

class CustomVisitor(DecafVisitor):

    def __init__(self):
        self.scope = DecafStack()
        self.errors = []
        self.anonCounter = 0
        self.offset = 0

    def error(self):
        self.flag = True
    
    def enterScope(self, name, t='scope'):
        parent = self.scope.peek()
        st = STable(name, parent=parent, stype=t, tt=TypeTable(), entrys={})
        self.scope.push(st)
        print('entering scope', name)

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

    # Visit a parse tree produced by DecafParser#program.
    def visitProgram(self, ctx:DecafParser.ProgramContext):
        self.enterScope('GLOBAL')
        return self.visitChildren(ctx)

    # Visit a parse tree produced by DecafParser#singleVar.
    def visitSingleVar(self, ctx:DecafParser.SingleVarContext):
        name = str(ctx.ID())
        scope = self.scope.peek()
        vartype = ctx.vType.getText()

        # if is inside struct
        if scope.scopeType == 'struct':
            # add to type table under structs name
            tt = scope.parent.typeTable
            param = Symbol(name, vartype, 0)

            # Add size and parameter to struct type in parent scope
            tt.addSize(name, tt.getSize(vartype))
            tt.addParam(scope.name, param)
            return self.visitChildren(ctx)

        # if is struct declaration
        elif 'struct' in vartype:
            # add struct to symbol table
            sName = name.replace('struct', '')

            struct = Symbol(name, sName, self.offset)
            scope.add(struct)

            structParams = scope.typeTable.getParams(sName)
            for param in structParams:
                s = Symbol(sName + param.name, param.stype, self.offset)
                self.offset += scope.typeTable.getSize(vartype)
                scope.add(s)
            
            return self.visitChildren(ctx)

        #else is just normal var, add symbol to table
        s = Symbol(name, vartype, self.offset)
        self.offset += scope.typeTable.getSize(vartype)
        print('Adding variable', name, 'to scope', scope.name)
        scope.parent and print(scope.parent.entrys)
        scope.add(s)
        scope.parent and print(scope.parent.entrys)

        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#listVar.
    def visitListVar(self, ctx:DecafParser.ListVarContext):
        name = str(ctx.ID())
        scope = self.scope.peek()
        vartype = ctx.vType.getText()

        size = int(str(ctx.NUM()))

        s = Symbol(name, vartype, self.offset)
        print(scope.typeTable.entrys['int'])
        self.offset += (scope.typeTable.getSize(vartype) * size)
        scope.add(s)
        print("NANIIIIII")

        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#structDeclaration.
    def visitStructDeclaration(self, ctx:DecafParser.StructDeclarationContext):
        name = str(ctx.ID())
        scope = self.scope.peek()

        self.enterScope(name, 'struct')

        s = TypeItem(name, 0, 'struct', {})
        scope.addType(s)
        visited = self.visitChildren(ctx)

        self.exitScope()
        return visited


    # Visit a parse tree produced by DecafParser#methodDeclaration.
    def visitMethodDeclaration(self, ctx:DecafParser.MethodDeclarationContext):
        name = str(ctx.ID())
        scope = self.scope.peek()
        returnType = ctx.returnType.getText()
        
        s = TypeItem(name, 0, 'method', {}, returnType)
        
        for param in ctx.parameter():
            values = self.visitParameter(param)
            s.addParam(values)

        scope.addType(s)

        # enter method scope
        self.enterScope(name, 'method')

        # visit
        visit = self.visitChildren(ctx)

        self.exitScope()
        
        return visit
    
    # Visit a parse tree produced by DecafParser#parameter.
    def visitParameter(self, ctx:DecafParser.ParameterContext):
        name = str(ctx.ID())
        scope = self.scope.peek()
        vartype = ctx.vType.getText()
        
        s = Symbol(name, vartype, self.offset, param=True)

        scope.add(s)

        v = self.visitChildren(ctx)

        return s

    # Visit a parse tree produced by DecafParser#ifStmt.
    def visitIfStmt(self, ctx:DecafParser.IfStmtContext):
        self.enterScope('block' + str(self.anonCounter), 'if')
        self.anonCounter += 1

        visit = self.visitChildren(ctx)
        
        self.exitScope()
        return visit

    # Visit a parse tree produced by DecafParser#whileStmt.
    def visitWhileStmt(self, ctx:DecafParser.WhileStmtContext):
        self.enterScope('block' + str(self.anonCounter), 'if')
        self.anonCounter += 1

        visit = self.visitChildren(ctx)
        
        self.exitScope()
        return visit
