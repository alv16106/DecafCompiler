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
    def visitMethodCall(self, ctx:DecafParser.MethodCallExprContext):
        method_name = str(ctx.ID())
        scope = self.scopes.peek()
        method = scope.typeExists(method_name, 'method')

        print(method_name, 'in methodCall', ctx.start.line)

        if not method:
            error = notDefinedError('method', method_name, ctx.start.line)
            self.errors.append(error)
            return type_enum.Error

        values = []
        params = [param.stype for param in method.paramlist.values()]

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
    
    def visitAssignStmt(self, ctx:DecafParser.AssignStmtContext):
        left_type = self.visit(ctx.left)
        right_type = self.visit(ctx.right)

        print(left_type, right_type)

        if right_type !=  left_type:
            error = genericError('Can only assign to two expressions with the same type', ctx.start.line)
            self.errors.append(error)
            return type_enum.Error

        return type_enum.Boolean

    def visitLocation(self, ctx:DecafParser.LocationExprContext):
        var_name = ctx.name.text
        scope = self.scopes.peek()
        var = scope.lookup(var_name)
        value = type_enum.Error

        if not var:
            error = notDefinedError('variable', var_name, ctx.start.line)
            self.errors.append(error)
            return type_enum.Error
        
        value = var.stype
        
        if ctx.expr:
            
            if not var.listSize:
                error = genericError('symbol of type %s is non suscriptable' % var.stype, ctx.start.line)
                self.errors.append(error)
                return type_enum.Error

            num_expr = ctx.expr.getText()

            try:
                num = int(num_expr)
                if num < 0 or (num > var.listSize - 1):
                    error = genericError('Index out of range', ctx.start.line)
                    self.errors.append(error)
                    return type_enum.Error
            except ValueError:
                pass

            visit = self.visit(ctx.expr)

            if visit != type_enum.Integer:
                error = genericError('Index must be an integer', ctx.start.line)
                self.errors.append(error)
                return type_enum.Error
        
        if ctx.loc:
            struct = scope.typeExists(var.stype, type_enum.Struct)

            if not struct:
                error = genericError('Location passed but %s is not a struct' % var_name, ctx.start.line)
                self.errors.append(error)
                return type_enum.Error
            
            if ctx.loc.name.text not in struct.paramlist:
                error = genericError('Location %s not defined in struct of %s of type %s' % (ctx.loc.name.text, var_name, var.stype), ctx.start.line)
                self.errors.append(error)
                return type_enum.Error
            
            value = struct.paramlist[ctx.loc.name.text].stype
        
        return value

    #Operations
    def visitRelationOp(self, ctx:DecafParser.RelationOpContext):
        op = ctx.op.getText()

        left_type = self.visit(ctx.left)
        right_type = self.visit(ctx.right)

        if right_type != type_enum.Integer or left_type != type_enum.Integer:
            error = expectedError(type_enum.Integer, '%s, %s' % (left_type, right_type) , ctx.start.line)
            self.errors.append(error)
            return type_enum.Error

        return type_enum.Boolean
    
    def visitConditionalOp(self, ctx:DecafParser.ConditionalOpContext):
        op = ctx.op.getText()

        left_type = self.visit(ctx.left)
        right_type = self.visit(ctx.right)

        if right_type != type_enum.Integer or left_type != type_enum.Integer:
            error = expectedError(type_enum.Boolean, '%s, %s' % (left_type, right_type) , ctx.start.line)
            self.errors.append(error)
            return type_enum.Error

        return type_enum.Boolean
    
    def visitEqualityOp(self, ctx:DecafParser.EqualityOpContext):
        op = ctx.op.getText()

        left_type = self.visit(ctx.left)
        right_type = self.visit(ctx.right)

        if right_type !=  left_type:
            error = genericError('Can only apply %s to two expressions with the same type' % op, ctx.start.line)
            self.errors.append(error)
            return type_enum.Error

        return type_enum.Boolean
    
    def visitHigherArithOp(self, ctx:DecafParser.HigherArithOpContext):
        op = ctx.op.getText()

        left_type = self.visit(ctx.left)
        right_type = self.visit(ctx.right)

        if right_type != type_enum.Integer or left_type != type_enum.Integer:
            error = expectedError(type_enum.Integer, '%s %s %s' % (left_type, op, right_type) , ctx.start.line)
            self.errors.append(error)
            return type_enum.Error

        return type_enum.Integer

    def visitArithOp(self, ctx:DecafParser.ArithOpContext):
        op = ctx.op.getText()

        left_type = self.visit(ctx.left)
        right_type = self.visit(ctx.right)

        if right_type != type_enum.Integer or left_type != type_enum.Integer:
            error = expectedError(type_enum.Integer, '%s %s %s' % (left_type, op, right_type) , ctx.start.line)
            self.errors.append(error)
            return type_enum.Error

        return type_enum.Integer
