import sys
from antlr4 import *

from printer import get_tree
from Grammar.DecafLexer import DecafLexer
from Grammar.DecafParser import DecafParser
from CustomVisitor import CustomVisitor
from errors import printErrors

def comp(text):
    input = InputStream(text)
    lexer = DecafLexer(input)
    stream = CommonTokenStream(lexer)
    parser = DecafParser(stream)
    tree = parser.program()

    visitor = CustomVisitor()
    visitor.visit(tree)

    (view, _) = get_tree(tree)
    view.render('tree.gv', "./uimamalona/static/img")

    return visitor

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

    (view, _) = get_tree(tree)
    view.render('tree.gv', "./uimamalona/static/img")

if __name__ == '__main__':
    main(sys.argv)