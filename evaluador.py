from Grammar.DecafVisitor import DecafVisitor
from Grammar.DecafParser import DecafParser

from symbolTable import type_enum
from errors import genericError, notDefinedError, expectedError

class Evaluator(DecafVisitor):
    def __init__(self, scopes):
        self.scopes = scopes
        self.errors = []
    
    # Literals return their type
    def visitInt_literal(self, ctx:DecafParser.Int_literalContext):
        self.visitChildren(ctx)
        return type_enum.Integer

    def visitChar_literal(self, ctx:DecafParser.Char_literalContext):
        self.visitChildren(ctx)
        return type_enum.Char

    def visitBool_literal(self, ctx:DecafParser.Bool_literalContext):
        self.visitChildren(ctx)
        return type_enum.Boolean
    
    # Expressions
    def visitMethodCallExpr(self, ctx:DecafParser.MethodCallExprContext):
        method_name = str(ctx.ID())
        scope = self.scopes.peek()
        method = scope.typeExists(method_name, 'method')

        values = []
        params = [param.stype for param in method.paramlist]

        if not method:
            error = notDefinedError('method', method_name, ctx.start.line)
            self.errors.append(error)
            return type_enum.Error

        for argument in ctx.arg():
            values.append(self.visitArg(argument))
        
        if params != values:
            error = expectedError(params, values, ctx.line.start)
            self.errors.append()
            return type_enum.Error
            
        return method.ret
    
    def visitArg(self, ctx:DecafParser.ArgContext):
        return self.visitChildren(ctx)

    def visitNegationExpr(self, ctx:DecafParser.NegationExprContext):
        t = self.visit(ctx.expression())
        if t != type_enum.Boolean:
            error = genericError('Can only negate (!) boolean expressions', ctx.start.line)
            self.errors.append(error)
            return type_enum.Error
        return type_enum.Boolean
    
    def visitNegativeExpr(self, ctx:DecafParser.NegativeExprContext):
        t = self.visit(ctx.expression())
        if t != type_enum.Integer:
            error = genericError('Can only apply negative (-) to integer expressions', ctx.start.line)
            self.errors.append(error)
            return type_enum.Error
        return type_enum.Integer

    def visitLocationExpr(self, ctx:DecafParser.LocationExprContext):
        return self.visitChildren(ctx)

    #Operations
    def visitRelationOp(self, ctx:DecafParser.RelationOpContext):
        return self.visitChildren(ctx)
    
    def visitConditionalOp(self, ctx:DecafParser.ConditionalOpContext):
        return self.visitChildren(ctx)
    
    def visitEqualityOp(self, ctx:DecafParser.EqualityOpContext):
        return self.visitChildren(ctx)
    
    def visitHigherArithOp(self, ctx:DecafParser.HigherArithOpContext):
        return self.visitChildren(ctx)

    def visitArithOp(self, ctx:DecafParser.ArithOpContext):
        return self.visitChildren(ctx)
