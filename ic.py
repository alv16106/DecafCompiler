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
    
    # Literals return just their string
    def visitInt_literal(self, ctx:DecafParser.Int_literalContext):
        return ICNode(None, code=ctx.getText())

    def visitChar_literal(self, ctx:DecafParser.Char_literalContext):
        return ICNode(None, code=ctx.getText())

    def visitBool_literal(self, ctx:DecafParser.Bool_literalContext):
        if ctx.getText() == 'true':
            return ICNode(None, code='1')
        return ICNode(None, code='0')
    
    # Negation and negative    
    def visitNegativeExpr(self, ctx:DecafParser.NegativeExprContext):
        t = self.visit(ctx.expression())
        new_temp = self.get_temporal()
        code = []
        negative = ICNode('-', right=t)
        if lt := t.lt:
            code += t.code
            code.append(new_temp + ' = NEG ' + lt )
            self.free_temporal(lt)
        else:
            code.append(new_temp + ' = NEG '  + t.code)
        
        negative.code = code
        negative.lt = new_temp

        return negative
    
    def visitNegationExpr(self, ctx:DecafParser.NegativeExprContext):
        t = self.visit(ctx.expression())
        new_temp = self.get_temporal()
        code = []
        negated = ICNode('!', right=t)
        if lt := t.lt:
            code += t.code
            code.append(new_temp + ' = NOT ' + lt )
            self.free_temporal(lt)
        else:
            code.append(new_temp + ' = NOT '  + t.code)

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
        code += left_node.code if isinstance(left_node.code, list) else []
        code += right_node.code if isinstance(right_node.code, list) else []

        new_temp = self.get_temporal()
        
        code.append(self.gen_code(new_temp, (left_node.lt or left_node.code), op, (right_node.lt or right_node.code)))


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
        code += left_node.code if isinstance(left_node.code, list) else []
        code += right_node.code if isinstance(right_node.code, list) else []

        new_temp = self.get_temporal()
        
        code.append(self.gen_code(new_temp, (left_node.lt or left_node.code), op, (right_node.lt or right_node.code)))


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
        code += left_node.code if isinstance(left_node.code, list) else []
        code += right_node.code if isinstance(right_node.code, list) else []

        new_temp = self.get_temporal()
        
        code.append(self.gen_code(new_temp, (left_node.lt or left_node.code), op, (right_node.lt or right_node.code)))


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
        code += left_node.code if isinstance(left_node.code, list) else []
        code += right_node.code if isinstance(right_node.code, list) else []

        new_temp = self.get_temporal()
        
        code.append(self.gen_code(new_temp, (left_node.lt or left_node.code), op, (right_node.lt or right_node.code)))


        harith.code = code
        harith.lt = new_temp

        print(code)

        return harith

    def visitArithOp(self, ctx:DecafParser.ArithOpContext):
        op = ctx.op.getText()

        left_node = self.visit(ctx.left)
        right_node = self.visit(ctx.right)

        self.free_temporal(left_node.lt)
        self.free_temporal(right_node.lt)

        arith = ICNode(op, right_node, left_node)

        code = []
        code += left_node.code if isinstance(left_node.code, list) else []
        code += right_node.code if isinstance(right_node.code, list) else []

        new_temp = self.get_temporal()
        
        code.append(self.gen_code(new_temp, (left_node.lt or left_node.code), op, (right_node.lt or right_node.code)))


        arith.code = code
        arith.lt = new_temp

        return arith
    
    def visitParentExpr(self, ctx:DecafParser.ParentExprContext):
        return self.visit(ctx.expression())