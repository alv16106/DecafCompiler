import sys
from antlr4 import *

from printer import get_tree
from Grammar.DecafLexer import DecafLexer
from Grammar.DecafParser import DecafParser
from CustomVisitor import CustomVisitor

def main(argv):
    input = FileStream(argv[1])
    lexer = DecafLexer(input)
    stream = CommonTokenStream(lexer)
    parser = DecafParser(stream)
    tree = parser.program()

    visitor = CustomVisitor()
    visitor.visit(tree)

    (view, _) = get_tree(tree)
    view.view()

if __name__ == '__main__':
    main(sys.argv)