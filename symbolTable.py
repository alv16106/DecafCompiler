from enum import Enum

class type_enum(Enum):
    Char = 0
    Boolean = 1
    Integer = 2

class STable:
    def __init__(self, name='', entrys={}, parent=None, tt=None, stype='scope'):
        self.name = name
        self.entrys = entrys
        self.parent = parent
        self.typeTable = tt
        self.scopeType = stype
    
    def lookup(self, name):
        if name not in self.entrys:
            if self.parent:
                return self.parent.lookup(name)
            return False
        return self.entrys[name]
        
    def add(self, symbol):
        self.entrys[symbol.name] = symbol
        
    def delete(self, name):
        if name in self.entrys:
            del self.entrys[name]
    
    def addType(self, t):
        self.typeTable.add(t)

class Symbol:
    def __init__(self, name, stype, offset=0, param=False):
        self.name = name
        self.stype = stype
        self.offset = offset
        self.param = param


class TypeItem:
    def __init__(self, name, size, type='struct', paramlist={}, ret=None):
        self.name = name
        self.size = size
        self.paramlist = paramlist
        self.type = type
        self.ret = ret
    
    def addParam(self, param):
        self.paramlist[param.name] = param

class TypeTable:
    def __init__(self):
        self.entrys = {}
        self.entrys['char'] = TypeItem('String', 1)
        self.entrys['int'] = TypeItem('Integer', 4)
        self.entrys['bool'] = TypeItem('Boolean', 1)

    def addParam(self, name, param):
        if name in self.entrys:
            self.entrys[name].addParam(param)
            return True
        return False

    def addSize(self, name, size):
        if name in self.entrys:
            self.entrys[name].size += size
            return True
        return False

    def add(self, name, t):
        self.entrys[name] = t
    
    def getSize(self, name):
        if name in self.entrys:
            return self.entrys[name].size

        return None

    def getParams(self, name):
        if name in self.entrys:
            return self.entrys[name].paramlist

        return None