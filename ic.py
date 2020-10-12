from Grammar.DecafVisitor import DecafVisitor
from Grammar.DecafParser import DecafParser

from symbolTable import type_enum
from icnode import ICNode, TEMPORALS

class  ICGenerator(DecafVisitor):
    def __init__(self, scopes):
        self.scopes = scopes
        self.label = 0
        self.used_temporals = set()
        self.available_temporals = set(TEMPORALS)
    
    def gen_label(self):
        self.label += 1
        return 'label%d' % self.label
    
    def get_temporal(self):
        e = self.available_temporals.pop()
        self.used_temporals.add(e)
        return e
    
    def free_temporal(self, temporal):
        if temporal in self.used_temporals:
            self.used_temporals.discard(temporal)
            self.available_temporals.add(temporal)
    
    def gen_code(self, *args):
        return '%s = %s %s %s' % args
    
    def get_location(self, scope, offset):
        return '%s[%s]' % (scope.capitalize(), str(offset))
    
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

        print(code)
        print(self.used_temporals)

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

        ifNode = ICNode('if')
        code = []

        elselabel = self.gen_label()

        expr = self.visit(ctx.expression()) 

        condition = expr.lt

        code += expr.code

        code.append('IFNOT ' + condition + ' goto ' + elselabel)

        ifblock = self.visit(ctx.ifblock)
        code += ifblock.code


        if ctx.elseblock():
            endlabel = self.gen_label()
            code.append('goto '+ endlabel)

            code.append(elselabel)
            elseblock = self.visit(ctx.elseblock)
            code += elseblock.code

            code.append(endlabel)
        else:
            code.append(elselabel)

        ifNode.code = code

        return ifNode

    def visitWhileStmt(self, ctx:DecafParser.WhileStmtContext):
        whileNode = ICNode('while')
        code = []

        conditionlabel = self.gen_label()
        elselabel = self.gen_label()

        expr = self.visit(ctx.expression())

        condition = expr.lt
        code.append(conditionlabel)
        code += expr.code

        code.append('IFNOT ' + condition + ' goto ' + elselabel)

        whileblock = self.visit(ctx.block())
        code += whileblock.code
        
        code.append('goto '+ conditionlabel)
        code.append(elselabel)

        whileNode.code = code
        
        return whileNode
    
    # visit locations
    def visitLocation(self, ctx:DecafParser.LocationExprContext, struct=None):
        var_name = ctx.name.text
        scope = self.scopes.peek()
        var, scopeName = scope.lookup(var_name)
        tokenEXPR = ctx.expr
        tokenLOC = ctx.loc

        if not tokenEXPR and not tokenLOC:
            return self.get_location(scopeName, var.offset)

        #We have a list
        elif tokenEXPR and not tokenLOC:
            size = scope.typeTable.getSize(var.stype)
            
            # EZ index is a number
            if (index := ctx.expr.getText()).isnumeric():
                return self.get_location(scopeName, var.offset + size * int(index))

            # Index is an expression
            locNode = ICNode('location')
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

        assignNode.code = code
        print(code)
        return assignNode
