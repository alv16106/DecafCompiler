from functools import reduce
from Grammar.DecafVisitor import DecafVisitor
from Grammar.DecafParser import DecafParser

from symbolTable import type_enum
from icnode import ICNode, TEMPORALS, RETURN_REGISTER

class  ICGenerator(DecafVisitor):
    def __init__(self, scopes, saved):
        self.scopes = scopes
        self.saved = saved
        self.anonCounter = 0
        self.label = 0
        self.used_temporals = set()
        self.available_temporals = set(TEMPORALS)
        self.code = []
    
    def gen_label(self):
        self.label += 1
        return 'label%d' % self.label
    
    def get_temporal(self):
        e = self.available_temporals.pop()
        self.used_temporals.add(e)
        return e
    
    def enterScope(self, name):
        entry = self.saved.get(name)
        self.scopes.push(entry)
    
    def exitScope(self):
        self.scopes.pop()
        
    
    def free_temporal(self, temporal):
        if temporal in self.used_temporals:
            self.used_temporals.discard(temporal)
            self.available_temporals.add(temporal)
    
    def gen_code(self, *args):
        return '%s = %s %s %s' % args
    
    def get_location(self, scope, offset):
        return '%s[%s]' % (scope.capitalize(), str(offset))
    
    # Visit a parse tree produced by DecafParser#program.
    def visitProgram(self, ctx:DecafParser.ProgramContext):
        return self.visitChildren(ctx)
    
    # Literals return just their string
    def visitInt_literal(self, ctx:DecafParser.Int_literalContext):
        return ICNode(None, lt=ctx.getText())

    def visitChar_literal(self, ctx:DecafParser.Char_literalContext):
        return ICNode(None, lt=ctx.getText())

    def visitBool_literal(self, ctx:DecafParser.Bool_literalContext):
        if ctx.getText() == 'true':
            return ICNode(None, lt='1')
        return ICNode(None, lt='0')
    
    # Negation and negative    
    def visitNegativeExpr(self, ctx:DecafParser.NegativeExprContext):
        t = self.visit(ctx.expression)
        new_temp = self.get_temporal()
        code = []
        negative = ICNode('-', right=t)
        code += t.code
        code.append(new_temp + ' = NEG ' + t.lt )
        self.free_temporal(t.lt)
        
        negative.code = code
        negative.lt = new_temp

        return negative
    
    def visitNegationExpr(self, ctx:DecafParser.NegativeExprContext):
        t = self.visit(ctx.expression)
        new_temp = self.get_temporal()
        code = []
        negated = ICNode('!', right=t)
        code += t.code
        code.append(new_temp + ' = NOT ' + t.lt )
        self.free_temporal(t.lt)

        negated.code = code
        negated.lt = new_temp
        
        return negated
    
    #Operations
    def visitRelationOp(self, ctx:DecafParser.RelationOpContext):
        op = ctx.op.getText()

        left_node = self.visit(ctx.left)
        right_node = self.visit(ctx.right)

        self.free_temporal(left_node.lt)
        self.free_temporal(right_node.lt)

        rel = ICNode(op, right_node, left_node)

        code = []
        code += left_node.code
        code += right_node.code

        new_temp = self.get_temporal()
        
        code.append(self.gen_code(new_temp, left_node.lt, op, right_node.lt))

        rel.code = code
        rel.lt = new_temp

        return rel
    
    def visitConditionalOp(self, ctx:DecafParser.ConditionalOpContext):
        op = ctx.op.getText()

        left_node = self.visit(ctx.left)
        right_node = self.visit(ctx.right)

        self.free_temporal(left_node.lt)
        self.free_temporal(right_node.lt)

        cond = ICNode(op, right_node, left_node)

        code = []
        code += left_node.code
        code += right_node.code

        new_temp = self.get_temporal()
        
        code.append(self.gen_code(new_temp, left_node.lt, op, right_node.lt))

        cond.code = code
        cond.lt = new_temp

        return cond
    
    def visitEqualityOp(self, ctx:DecafParser.EqualityOpContext):
        op = ctx.op.getText()

        left_node = self.visit(ctx.left)
        right_node = self.visit(ctx.right)

        self.free_temporal(left_node.lt)
        self.free_temporal(right_node.lt)

        eq = ICNode(op, right_node, left_node)

        code = []
        code += left_node.code
        code += right_node.code

        new_temp = self.get_temporal()
        
        code.append(self.gen_code(new_temp, left_node.lt, op, right_node.lt))

        eq.code = code
        eq.lt = new_temp

        return eq
    
    def visitHigherArithOp(self, ctx:DecafParser.HigherArithOpContext):
        op = ctx.op.getText()

        left_node = self.visit(ctx.left)
        right_node = self.visit(ctx.right)

        self.free_temporal(left_node.lt)
        self.free_temporal(right_node.lt)

        harith = ICNode(op, right_node, left_node)

        code = []
        code += left_node.code
        code += right_node.code

        new_temp = self.get_temporal()
        
        code.append(self.gen_code(new_temp, left_node.lt, op, right_node.lt))

        harith.code = code
        harith.lt = new_temp

        return harith

    def visitArithOp(self, ctx:DecafParser.ArithOpContext):
        op = ctx.op.getText()

        left_node = self.visit(ctx.left)
        right_node = self.visit(ctx.right)

        self.free_temporal(left_node.lt)
        self.free_temporal(right_node.lt)

        arith = ICNode(op, right_node, left_node)

        code = []
        code += left_node.code
        code += right_node.code

        new_temp = self.get_temporal()
        
        code.append(self.gen_code(new_temp, left_node.lt, op, right_node.lt))

        arith.code = code
        arith.lt = new_temp

        return arith
    
    def visitParentExpr(self, ctx:DecafParser.ParentExprContext):
        return self.visit(ctx.expression())
    

    # ifs and whiles
    def visitIfStmt(self, ctx:DecafParser.IfStmtContext):
        self.enterScope('ifblock' + str(self.anonCounter))
        self.anonCounter += 1

        ifNode = ICNode('if')
        code = []

        elselabel = self.gen_label()

        expr = self.visit(ctx.expression()) 

        condition = expr.lt
        self.free_temporal(condition)

        code += expr.code

        code.append('IFNOT ' + condition + ' goto ' + elselabel)

        ifblock = self.visit(ctx.ifblock)
        code += ifblock.code

        if ctx.elseblock:
            endlabel = self.gen_label()
            code.append('goto '+ endlabel)

            code.append(elselabel)
            elseblock = self.visit(ctx.elseblock)
            code += elseblock.code

            code.append(endlabel)
        else:
            code.append(elselabel)

        ifNode.code = code

        self.exitScope()

        return ifNode

    def visitWhileStmt(self, ctx:DecafParser.WhileStmtContext):
        self.enterScope('whileblock' + str(self.anonCounter))
        self.anonCounter += 1

        whileNode = ICNode('while')
        code = []

        conditionlabel = self.gen_label()
        elselabel = self.gen_label()

        expr = self.visit(ctx.expression())

        condition = expr.lt
        self.free_temporal(condition)

        code.append(conditionlabel)
        code += expr.code

        code.append('IFNOT ' + condition + ' goto ' + elselabel)

        whileblock = self.visit(ctx.block())
        code += whileblock.code
        
        code.append('goto '+ conditionlabel)
        code.append(elselabel)

        whileNode.code = code
        
        self.exitScope()

        return whileNode
    
    # visit locations
    def visitLocation(self, ctx:DecafParser.LocationExprContext, struct=None):
        var_name = ctx.name.text
        scope = self.scopes.peek()
        var, scopeName = scope.lookup(var_name)
        tokenEXPR = ctx.expr
        tokenLOC = ctx.loc
        locNode = ICNode('location')

        if not tokenEXPR and not tokenLOC:
            locNode.lt = self.get_location(scopeName, var.offset)
            return locNode

        #We have a list
        elif tokenEXPR and not tokenLOC:
            size = scope.typeTable.getSize(var.stype)
            
            # EZ index is a number
            if (index := ctx.expr.getText()).isnumeric():
                locNode.lt = self.get_location(scopeName, var.offset + size * int(index))
                return locNode

            # Index is an expression
            code = []
            expr = self.visit(tokenEXPR)
            # 2 new temporals, to compute the new offset
            new_temp = self.get_temporal()
            new_temp2 = self.get_temporal()
            # if expression is a location, we get a string, if not we get an ICNode
            location = expr
            if not isinstance(expr, str):
                code += expr.code
                location = expr.lt
                self.free_temporal(expr.lt)

            code.append(self.gen_code(new_temp, location, '*', size))
            code.append(self.gen_code(new_temp2, new_temp, '+', var.offset))

            self.free_temporal(new_temp)
            self.free_temporal(new_temp2)

            locNode.code = code
            locNode.lt = self.get_location(scopeName, new_temp2)

            return locNode
        
        # We have ourselves a struct boiiii
        elif tokenLOC:
            pass

    def visitAssignStmt(self, ctx:DecafParser.AssignStmtContext):
        destination = self.visit(ctx.left)
        right = self.visit(ctx.right)

        loc = destination

        assignNode = ICNode('=', left=destination, right=right)
        code = []

        code += right.code

        if not isinstance(destination, str):
            code += destination.code
            loc = destination.lt
        
        code.append(self.gen_code(loc, right.lt, '', ''))
        self.free_temporal(right.lt)

        assignNode.code = code
        return assignNode
    
    def visitBlock(self, ctx:DecafParser.BlockContext):
        blockNode = ICNode('none')
        code = []

        for statement in ctx.statement():
            v = self.visitStatement(statement)
            code += v.code if v else []
        
        blockNode.code = code

        return blockNode

    def visitStatement(self, ctx:DecafParser.StatementContext):
        vi = self.visit(ctx.getChild(0))
        return vi

    # Expressions
    def visitMethodCall(self, ctx:DecafParser.MethodCallExprContext):
        methodCallNode = ICNode('call')
        code = []

        method_label = str(ctx.ID())
        scope = self.scopes.peek()
        method = scope.typeExists(method_label, 'method')

        for argument in ctx.arg():
            argNode = self.visitArg(argument)
            code +=  argNode.code
            code.append('PushParam ' + argNode.lt)
            self.free_temporal(argNode.lt)
        
        code.append('LCall ' + method_label)

        code.append('PopParams ' + str(method.size))

        methodCallNode.lt = RETURN_REGISTER
        methodCallNode.code = code

        return methodCallNode

    def visitReturnStmt(self, ctx:DecafParser.ReturnStmtContext):
        expr = self.visit(ctx.expression())
        returnNode = ICNode('return')
        code = []
        
        code += expr.code
        code.append(self.gen_code(RETURN_REGISTER, expr.lt, '', ''))
        self.free_temporal(expr.lt)
        code.append('BX LR')

        returnNode.code = code

        return returnNode

    def visitMethodDeclaration(self, ctx:DecafParser.MethodDeclarationContext):
        name = str(ctx.ID())
        code = []

        scope = self.scopes.peek()
        method = scope.typeExists(name, 'method')

        code.append('BeginFunc ' + str(method.size))
        code.append(name+':')
        self.enterScope(name)
        visit = self.visitChildren(ctx)
        self.exitScope()

        code += visit.code
        self.free_temporal(visit.lt)
        code.append('\n')

        self.code += code

        print(self.used_temporals)

        return code