import sys
from antlr4 import *

from printer import get_tree
from Grammar.DecafLexer import DecafLexer
from Grammar.DecafParser import DecafParser
from CustomVisitor import CustomVisitor
from errors import printErrors

def main(argv):
    file = "tests/help.txt"
    if len(argv) > 1:
        file = argv[1]
    input = FileStream(file)
    lexer = DecafLexer(input)
    stream = CommonTokenStream(lexer)
    parser = DecafParser(stream)
    tree = parser.program()

    visitor = CustomVisitor()
    visitor.visit(tree)

    printErrors(visitor.TypeValidator.errors)

    print(visitor.scope.peek().entrys)

    (view, _) = get_tree(tree)
    view.view()

if __name__ == '__main__':
    main(sys.argv)