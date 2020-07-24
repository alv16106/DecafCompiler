from graphviz import Digraph
from antlr4.tree.Trees import Trees
from Grammar.DecafParser import DecafParser


TERMINAL_NODE_TYPE = "<class 'antlr4.tree.Tree.TerminalNodeImpl'>"
ERROR_NODE_TYPE = "<class 'antlr4.tree.Tree.ErrorNodeImpl'>"

def get_name(node):
    s = node.toString(DecafParser.ruleNames, node.stop)
    return s.replace('[', ']').replace(']', '').split(' ')[0]

def convert(tree, diagram, current):
    children = tree.getChildCount()
    parentID = current
    for a in range(children):
        child = tree.getChild(a)
        t = str(type(child))
        # significa que es un literal
        if t == TERMINAL_NODE_TYPE:
            label = child.getText()
            color = "white"
        elif t == ERROR_NODE_TYPE:
            label = child.getText()
            color = "red"
        else:
            label = get_name(child)
            color = "blue"

        current += 1
        diagram.node(str(current), label, color=color)
        diagram.edge(str(parentID), str(current))
        if child.getChildCount() > 0:
            _, current = convert(child, diagram, current)
    
    return diagram, current

def get_tree(root):
    D = Digraph("Tree", "tree.gv")
    D.node('0', get_name(root))
    return convert(root, D, 0)