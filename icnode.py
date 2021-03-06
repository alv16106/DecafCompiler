TEMPORALS = 'T1 T2 T3 T4 T5 T6 T7 T8'.split()
RETURN_REGISTER = 'EAX'

def printable_code(code):
    return '\n'.join(code)

class ICNode:

    def __init__(self, operation, right=None, left=None, code=[], lt=''):
        self.operation = operation
        self.leftChild = right
        self.rightChild = left
        self.code = code
        self.lt = lt
    
    def setRightChild(self, child):
        self.rightChild = child

    def setLeftChild(self, child):
        self.leftChild = child
    
    def __str__(self):
        return "Code: " + printable_code(self.code) + "\nlt: " + self.lt