from Grammar.DecafVisitor import DecafVisitor
from Grammar.DecafParser import DecafParser
import inspect
from stack import DecafStack
from errors import genericError
from evaluador import Evaluator
from ic import ICGenerator
from symbolTable import *

class CustomVisitor(DecafVisitor):

    def __init__(self):
        self.scope = DecafStack()
        self.errors = []
        self.anonCounter = 0
        self.offset = 0
        self.TypeValidator = Evaluator(scopes=self.scope)
        self.icGenerator = ICGenerator(scopes=self.scope) 

    def error(self):
        self.flag = True
    
    def enterScope(self, name, t='scope'):
        parent = self.scope.peek()
        st = STable(name, parent=parent, stype=t, tt=TypeTable(), entrys={})
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

    # Visit a parse tree produced by DecafParser#program.
    def visitProgram(self, ctx:DecafParser.ProgramContext):
        self.enterScope('GLOBAL')
        return self.visitChildren(ctx)

    # Visit a parse tree produced by DecafParser#singleVar.
    def visitSingleVar(self, ctx:DecafParser.SingleVarContext):
        name = str(ctx.ID())
        scope = self.scope.peek()
        type_text = ctx.vType.getText()

        vartype = scope.typeExists(type_text.replace('struct', '')).name

        # if is inside struct
        if scope.scopeType == 'struct':
            # add to type table under structs name
            tt = scope.parent.typeTable
            param = Symbol(name, vartype, 0)

            # Add size and parameter to struct type in parent scope
            tt.addSize(name, tt.getSize(type_text))
            tt.addParam(scope.name, param)
            return self.visitChildren(ctx)

        # if is struct declaration
        elif 'struct' in type_text:
            # add struct to symbol table
            sName = type_text.replace('struct', '')

            struct = Symbol(name, sName, self.offset)
            scope.add(struct)

            structParams = scope.typeTable.getParams(sName)
            for param in structParams.values():
                s = Symbol(sName + param.name, param.stype, self.offset)
                self.offset += scope.typeTable.getSize(sName)
                scope.add(s)
            
            return self.visitChildren(ctx)

        #else is just normal var, add symbol to table
        s = Symbol(name, vartype, self.offset)
        self.offset += scope.typeTable.getSize(type_text)
        scope.add(s)

        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#listVar.
    def visitListVar(self, ctx:DecafParser.ListVarContext):
        name = str(ctx.ID())
        scope = self.scope.peek()
        vartype = ctx.vType.getText().replace('struct', '')

        size = int(str(ctx.NUM()))

        if scope.scopeType == 'struct':
            t = scope.parent.typeExists(vartype)
            tt = scope.parent.typeTable
            param = Symbol(name, t.name, 0, listSize=size)
            
            tt.addSize(name, t.size * size)
            tt.addParam(scope.name, param)
            return self.visitChildren(ctx)

        s = Symbol(name, vartype, self.offset, listSize=size)
        self.offset += (scope.typeExists(vartype).size * size)
        scope.add(s)

        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#structDeclaration.
    def visitStructDeclaration(self, ctx:DecafParser.StructDeclarationContext):
        name = str(ctx.ID())
        scope = self.scope.peek()

        self.enterScope(name, 'struct')

        s = TypeItem(name, 0, type_enum.Struct, {})
        scope.addType(s)
        visited = self.visitChildren(ctx)

        self.exitScope()
        return visited


    # Visit a parse tree produced by DecafParser#methodDeclaration.
    def visitMethodDeclaration(self, ctx:DecafParser.MethodDeclarationContext):
        name = str(ctx.ID())
        scope = self.scope.peek()
        returnType = ctx.returnType.getText()
        s = TypeItem(name, 0, 'method', {}, scope.typeExists(returnType).name)
        
        for param in ctx.parameter():
            values = self.visitParameter(param)
            s.addParam(values)

        scope.addType(s)

        # enter method scope
        self.enterScope(name, 'method')

        # visit
        visit = self.visitChildren(ctx)
        code = self.icGenerator.visitChildren(ctx)
        print('El codigo es ', code)

        self.exitScope()
        
        return visit
    
    # Visit a parse tree produced by DecafParser#parameter.
    def visitParameter(self, ctx:DecafParser.ParameterContext):
        name = str(ctx.ID())
        scope = self.scope.peek()

        type_text = ctx.vType.getText()

        vartype = scope.typeExists(type_text).name
        
        s = Symbol(name, vartype, self.offset, param=True)

        scope.add(s)

        return s

    # Visit a parse tree produced by DecafParser#ifStmt.
    def visitIfStmt(self, ctx:DecafParser.IfStmtContext):
        self.enterScope('ifblock' + str(self.anonCounter), 'if')
        self.anonCounter += 1

        expt = self.TypeValidator.visit(ctx.expression())
        if expt != type_enum.Boolean:
            error = genericError('Expected boolean expression for if', ctx.start.line)
            self.TypeValidator.errors.append(error)

        visit = self.visitChildren(ctx)
        
        self.exitScope()
        return visit

    # Visit a parse tree produced by DecafParser#whileStmt.
    def visitWhileStmt(self, ctx:DecafParser.WhileStmtContext):
        self.enterScope('whileblock' + str(self.anonCounter), 'if')
        self.anonCounter += 1

        expt = self.TypeValidator.visit(ctx.expression())

        if expt != type_enum.Boolean:
            error = genericError('Expected boolean expression for while', ctx.start.line)
            self.TypeValidator.errors.append(error)

        visit = self.visitChildren(ctx)
        
        self.exitScope()
        return visit
    
    #Operations
    def visitRelationOp(self, ctx:DecafParser.RelationOpContext):
        self.TypeValidator.visit(ctx)
        return self.visitChildren(ctx)
    
    def visitConditionalOp(self, ctx:DecafParser.ConditionalOpContext):
        self.TypeValidator.visit(ctx)
        return self.visitChildren(ctx)
    
    def visitEqualityOp(self, ctx:DecafParser.EqualityOpContext):
        self.TypeValidator.visit(ctx)
        return self.visitChildren(ctx)
    
    def visitHigherArithOp(self, ctx:DecafParser.HigherArithOpContext):
        self.TypeValidator.visit(ctx)
        return self.visitChildren(ctx)

    def visitArithOp(self, ctx:DecafParser.ArithOpContext):
        self.TypeValidator.visit(ctx)
        return self.visitChildren(ctx)
    
    #Assign
    def visitAssignStmt(self, ctx:DecafParser.ArithOpContext):
        self.TypeValidator.visit(ctx)
        return self.visitChildren(ctx)