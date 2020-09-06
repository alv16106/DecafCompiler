
grammar Decaf;

fragment LETTER: ('a'..'z'|'A'..'Z') ;

fragment DIGIT: '0'..'9' ;

ID: LETTER (LETTER | DIGIT)* ;

NUM: DIGIT (DIGIT)* ;

CHAR: '\'' LETTER '\'';

SPACES : [ \t\r\n\f]+  ->channel(HIDDEN);

program 
    : 'class' 'Program' '{' (declaration)* '}' 
    ;

declaration
    : structDeclaration
    | varDeclaration 
    | methodDeclaration 
    | structInstantiation
    ;

varDeclaration
    : vType=varType name=ID ';' #singleVar
    | vType=varType name=ID '[' size=NUM ']' ';' #listVar
    ;

structDeclaration
    : 
    'struct' name=ID '{' (varDeclaration)* '}' 
    ;

structInstantiation
    : 'struct' struct=ID name=ID
    ;

varType
    : 'int' 
    | 'char' 
    | 'boolean' 
    | 'struct' ID 
    | structDeclaration 
    | 'void' 
    ;

methodDeclaration
    : returnType=methodType name=ID '(' (parameter (',' parameter)*)* ')' block 
    ;

methodType
    : 'int' 
    | 'char' 
    | 'boolean' 
    | 'void'
    ;

parameter
    : vType=parameterType name=ID 
    | vType=parameterType name=ID '[' ']' 
    ;

parameterType
    : 'int' 
    | 'char'
    | 'boolean' 
    ;

block
    : '{' (varDeclaration)* (statement)* '}' 
    ;

statement
    : ifStmt
    | whileStmt
    | returnStmt
    | methodCall ';' 
    | block 
    | assignStmt 
    | (expression)? ';' 
    ;

ifStmt
    : 'if' '(' expression ')' block ('else' block)?
    ;

whileStmt
    : 'while' '(' expression ')' block
    ;

assignStmt
    : left=location '=' right=expression
    ;

returnStmt
    : 'return' (expression)? ';'
    ;

location
    : (name=ID | name=ID '[' expr=expression ']') ('.' loc=location)? ;

expression
    : location #locationExpr
    | methodCall #methodCallExpr
    | literal #literalExpr
    | left=expression op=higher_arith_op right=expression #higherArithOp
    | left=expression op=arith_op right=expression #arithOp
    | left=expression op=rel_op right=expression #relationOp
    | left=expression op=eq_op right=expression #equalityOp
    | left=expression op=cond_op right=expression #conditionalOp
    | '-' expression #negativeExpr
    | '!' expression #negationExpr
    | '(' expression ')' #parentExpr
    ;

methodCall
    : method=ID '(' (arg (',' arg)*)* ')' 
    ;

arg
    : 
    expression ;

higher_arith_op
    : '*' 
    | '/' 
    | '%' 
    ;

arith_op
    : '+' 
    | '-' 
    ;

rel_op
    : '<' 
    | '>' 
    | '<=' 
    | '>=' 
    ;

eq_op
    : '=='
    | '!=' 
    ;

cond_op
    : '&&' 
    | '||' 
    ;

literal
    : int_literal 
    | char_literal
    | bool_literal
    ;

int_literal
    : NUM
    ;

char_literal
    :  CHAR 
    ;

bool_literal
    : 'true' 
    | 'false'
    ;

