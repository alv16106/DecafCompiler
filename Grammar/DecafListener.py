# Generated from Decaf.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .DecafParser import DecafParser
else:
    from DecafParser import DecafParser

# This class defines a complete listener for a parse tree produced by DecafParser.
class DecafListener(ParseTreeListener):

    # Enter a parse tree produced by DecafParser#program.
    def enterProgram(self, ctx:DecafParser.ProgramContext):
        pass

    # Exit a parse tree produced by DecafParser#program.
    def exitProgram(self, ctx:DecafParser.ProgramContext):
        pass


    # Enter a parse tree produced by DecafParser#declaration.
    def enterDeclaration(self, ctx:DecafParser.DeclarationContext):
        pass

    # Exit a parse tree produced by DecafParser#declaration.
    def exitDeclaration(self, ctx:DecafParser.DeclarationContext):
        pass


    # Enter a parse tree produced by DecafParser#singleVar.
    def enterSingleVar(self, ctx:DecafParser.SingleVarContext):
        pass

    # Exit a parse tree produced by DecafParser#singleVar.
    def exitSingleVar(self, ctx:DecafParser.SingleVarContext):
        pass


    # Enter a parse tree produced by DecafParser#listVar.
    def enterListVar(self, ctx:DecafParser.ListVarContext):
        pass

    # Exit a parse tree produced by DecafParser#listVar.
    def exitListVar(self, ctx:DecafParser.ListVarContext):
        pass


    # Enter a parse tree produced by DecafParser#structDeclaration.
    def enterStructDeclaration(self, ctx:DecafParser.StructDeclarationContext):
        pass

    # Exit a parse tree produced by DecafParser#structDeclaration.
    def exitStructDeclaration(self, ctx:DecafParser.StructDeclarationContext):
        pass


    # Enter a parse tree produced by DecafParser#structInstantiation.
    def enterStructInstantiation(self, ctx:DecafParser.StructInstantiationContext):
        pass

    # Exit a parse tree produced by DecafParser#structInstantiation.
    def exitStructInstantiation(self, ctx:DecafParser.StructInstantiationContext):
        pass


    # Enter a parse tree produced by DecafParser#varType.
    def enterVarType(self, ctx:DecafParser.VarTypeContext):
        pass

    # Exit a parse tree produced by DecafParser#varType.
    def exitVarType(self, ctx:DecafParser.VarTypeContext):
        pass


    # Enter a parse tree produced by DecafParser#methodDeclaration.
    def enterMethodDeclaration(self, ctx:DecafParser.MethodDeclarationContext):
        pass

    # Exit a parse tree produced by DecafParser#methodDeclaration.
    def exitMethodDeclaration(self, ctx:DecafParser.MethodDeclarationContext):
        pass


    # Enter a parse tree produced by DecafParser#methodType.
    def enterMethodType(self, ctx:DecafParser.MethodTypeContext):
        pass

    # Exit a parse tree produced by DecafParser#methodType.
    def exitMethodType(self, ctx:DecafParser.MethodTypeContext):
        pass


    # Enter a parse tree produced by DecafParser#parameter.
    def enterParameter(self, ctx:DecafParser.ParameterContext):
        pass

    # Exit a parse tree produced by DecafParser#parameter.
    def exitParameter(self, ctx:DecafParser.ParameterContext):
        pass


    # Enter a parse tree produced by DecafParser#parameterType.
    def enterParameterType(self, ctx:DecafParser.ParameterTypeContext):
        pass

    # Exit a parse tree produced by DecafParser#parameterType.
    def exitParameterType(self, ctx:DecafParser.ParameterTypeContext):
        pass


    # Enter a parse tree produced by DecafParser#block.
    def enterBlock(self, ctx:DecafParser.BlockContext):
        pass

    # Exit a parse tree produced by DecafParser#block.
    def exitBlock(self, ctx:DecafParser.BlockContext):
        pass


    # Enter a parse tree produced by DecafParser#statement.
    def enterStatement(self, ctx:DecafParser.StatementContext):
        pass

    # Exit a parse tree produced by DecafParser#statement.
    def exitStatement(self, ctx:DecafParser.StatementContext):
        pass


    # Enter a parse tree produced by DecafParser#ifStmt.
    def enterIfStmt(self, ctx:DecafParser.IfStmtContext):
        pass

    # Exit a parse tree produced by DecafParser#ifStmt.
    def exitIfStmt(self, ctx:DecafParser.IfStmtContext):
        pass


    # Enter a parse tree produced by DecafParser#whileStmt.
    def enterWhileStmt(self, ctx:DecafParser.WhileStmtContext):
        pass

    # Exit a parse tree produced by DecafParser#whileStmt.
    def exitWhileStmt(self, ctx:DecafParser.WhileStmtContext):
        pass


    # Enter a parse tree produced by DecafParser#assignStmt.
    def enterAssignStmt(self, ctx:DecafParser.AssignStmtContext):
        pass

    # Exit a parse tree produced by DecafParser#assignStmt.
    def exitAssignStmt(self, ctx:DecafParser.AssignStmtContext):
        pass


    # Enter a parse tree produced by DecafParser#returnStmt.
    def enterReturnStmt(self, ctx:DecafParser.ReturnStmtContext):
        pass

    # Exit a parse tree produced by DecafParser#returnStmt.
    def exitReturnStmt(self, ctx:DecafParser.ReturnStmtContext):
        pass


    # Enter a parse tree produced by DecafParser#location.
    def enterLocation(self, ctx:DecafParser.LocationContext):
        pass

    # Exit a parse tree produced by DecafParser#location.
    def exitLocation(self, ctx:DecafParser.LocationContext):
        pass


    # Enter a parse tree produced by DecafParser#relationOp.
    def enterRelationOp(self, ctx:DecafParser.RelationOpContext):
        pass

    # Exit a parse tree produced by DecafParser#relationOp.
    def exitRelationOp(self, ctx:DecafParser.RelationOpContext):
        pass


    # Enter a parse tree produced by DecafParser#methodCallExpr.
    def enterMethodCallExpr(self, ctx:DecafParser.MethodCallExprContext):
        pass

    # Exit a parse tree produced by DecafParser#methodCallExpr.
    def exitMethodCallExpr(self, ctx:DecafParser.MethodCallExprContext):
        pass


    # Enter a parse tree produced by DecafParser#conditionalOp.
    def enterConditionalOp(self, ctx:DecafParser.ConditionalOpContext):
        pass

    # Exit a parse tree produced by DecafParser#conditionalOp.
    def exitConditionalOp(self, ctx:DecafParser.ConditionalOpContext):
        pass


    # Enter a parse tree produced by DecafParser#negationExpr.
    def enterNegationExpr(self, ctx:DecafParser.NegationExprContext):
        pass

    # Exit a parse tree produced by DecafParser#negationExpr.
    def exitNegationExpr(self, ctx:DecafParser.NegationExprContext):
        pass


    # Enter a parse tree produced by DecafParser#locationExpr.
    def enterLocationExpr(self, ctx:DecafParser.LocationExprContext):
        pass

    # Exit a parse tree produced by DecafParser#locationExpr.
    def exitLocationExpr(self, ctx:DecafParser.LocationExprContext):
        pass


    # Enter a parse tree produced by DecafParser#equalityOp.
    def enterEqualityOp(self, ctx:DecafParser.EqualityOpContext):
        pass

    # Exit a parse tree produced by DecafParser#equalityOp.
    def exitEqualityOp(self, ctx:DecafParser.EqualityOpContext):
        pass


    # Enter a parse tree produced by DecafParser#literalExpr.
    def enterLiteralExpr(self, ctx:DecafParser.LiteralExprContext):
        pass

    # Exit a parse tree produced by DecafParser#literalExpr.
    def exitLiteralExpr(self, ctx:DecafParser.LiteralExprContext):
        pass


    # Enter a parse tree produced by DecafParser#negativeExpr.
    def enterNegativeExpr(self, ctx:DecafParser.NegativeExprContext):
        pass

    # Exit a parse tree produced by DecafParser#negativeExpr.
    def exitNegativeExpr(self, ctx:DecafParser.NegativeExprContext):
        pass


    # Enter a parse tree produced by DecafParser#parentExpr.
    def enterParentExpr(self, ctx:DecafParser.ParentExprContext):
        pass

    # Exit a parse tree produced by DecafParser#parentExpr.
    def exitParentExpr(self, ctx:DecafParser.ParentExprContext):
        pass


    # Enter a parse tree produced by DecafParser#higherArithOp.
    def enterHigherArithOp(self, ctx:DecafParser.HigherArithOpContext):
        pass

    # Exit a parse tree produced by DecafParser#higherArithOp.
    def exitHigherArithOp(self, ctx:DecafParser.HigherArithOpContext):
        pass


    # Enter a parse tree produced by DecafParser#arithOp.
    def enterArithOp(self, ctx:DecafParser.ArithOpContext):
        pass

    # Exit a parse tree produced by DecafParser#arithOp.
    def exitArithOp(self, ctx:DecafParser.ArithOpContext):
        pass


    # Enter a parse tree produced by DecafParser#methodCall.
    def enterMethodCall(self, ctx:DecafParser.MethodCallContext):
        pass

    # Exit a parse tree produced by DecafParser#methodCall.
    def exitMethodCall(self, ctx:DecafParser.MethodCallContext):
        pass


    # Enter a parse tree produced by DecafParser#arg.
    def enterArg(self, ctx:DecafParser.ArgContext):
        pass

    # Exit a parse tree produced by DecafParser#arg.
    def exitArg(self, ctx:DecafParser.ArgContext):
        pass


    # Enter a parse tree produced by DecafParser#higher_arith_op.
    def enterHigher_arith_op(self, ctx:DecafParser.Higher_arith_opContext):
        pass

    # Exit a parse tree produced by DecafParser#higher_arith_op.
    def exitHigher_arith_op(self, ctx:DecafParser.Higher_arith_opContext):
        pass


    # Enter a parse tree produced by DecafParser#arith_op.
    def enterArith_op(self, ctx:DecafParser.Arith_opContext):
        pass

    # Exit a parse tree produced by DecafParser#arith_op.
    def exitArith_op(self, ctx:DecafParser.Arith_opContext):
        pass


    # Enter a parse tree produced by DecafParser#rel_op.
    def enterRel_op(self, ctx:DecafParser.Rel_opContext):
        pass

    # Exit a parse tree produced by DecafParser#rel_op.
    def exitRel_op(self, ctx:DecafParser.Rel_opContext):
        pass


    # Enter a parse tree produced by DecafParser#eq_op.
    def enterEq_op(self, ctx:DecafParser.Eq_opContext):
        pass

    # Exit a parse tree produced by DecafParser#eq_op.
    def exitEq_op(self, ctx:DecafParser.Eq_opContext):
        pass


    # Enter a parse tree produced by DecafParser#cond_op.
    def enterCond_op(self, ctx:DecafParser.Cond_opContext):
        pass

    # Exit a parse tree produced by DecafParser#cond_op.
    def exitCond_op(self, ctx:DecafParser.Cond_opContext):
        pass


    # Enter a parse tree produced by DecafParser#literal.
    def enterLiteral(self, ctx:DecafParser.LiteralContext):
        pass

    # Exit a parse tree produced by DecafParser#literal.
    def exitLiteral(self, ctx:DecafParser.LiteralContext):
        pass


    # Enter a parse tree produced by DecafParser#int_literal.
    def enterInt_literal(self, ctx:DecafParser.Int_literalContext):
        pass

    # Exit a parse tree produced by DecafParser#int_literal.
    def exitInt_literal(self, ctx:DecafParser.Int_literalContext):
        pass


    # Enter a parse tree produced by DecafParser#char_literal.
    def enterChar_literal(self, ctx:DecafParser.Char_literalContext):
        pass

    # Exit a parse tree produced by DecafParser#char_literal.
    def exitChar_literal(self, ctx:DecafParser.Char_literalContext):
        pass


    # Enter a parse tree produced by DecafParser#bool_literal.
    def enterBool_literal(self, ctx:DecafParser.Bool_literalContext):
        pass

    # Exit a parse tree produced by DecafParser#bool_literal.
    def exitBool_literal(self, ctx:DecafParser.Bool_literalContext):
        pass



del DecafParser