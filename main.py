import sys
from antlr4 import *

from printer import get_tree
from Grammar.DecafLexer import DecafLexer
from Grammar.DecafParser import DecafParser
from CustomListener import CustomListener

def main(argv):
    input = FileStream(argv[1])
    lexer = DecafLexer(input)
    stream = CommonTokenStream(lexer)
    parser = DecafParser(stream)
    tree = parser.program()
    listener = CustomListener()
    walker = ParseTreeWalker()

    # creates the symbol table, and the ast tree
    walker.walk(listener, tree)

    (view, _) = get_tree(tree)
    view.view()

if __name__ == '__main__':
    main(sys.argv)