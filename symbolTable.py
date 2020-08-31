from enum import Enum

class type_enum(Enum):
    String = 0
    Boolean = 1
    Integer = 2
    Float = 3

class STable:
    def __init__(self, name='', entrys={}, parent=None):
        self.name = name
        self.entrys = entrys
        self.parent = parent
    
    def lookup(self, name):
        if name not in self.entrys:
            if self.parent:
                return self.parent.lookup(name)
            return False
        return self.entrys[name]
        
    def add(self, name, symbol):
        self.entrys[name] = symbol
        
    def delete(self, name):
        if name in self.entrys:
            del self.entrys[name]

class Symbol:
    def __init__(self, name, stype, offset=0, param=False):
        self.name = name
        self.stype = stype
        self.offset = offset
        self.param = param


class TypeItem:
    def __init__(self, name, size, paramlist=None):
        self.name = name
        self.size = size
        self.paramlist = paramlist
    
    def addParam(self, param):
        self.paramlist.append(param)
