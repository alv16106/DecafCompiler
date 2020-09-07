from enum import Enum

class type_enum(Enum):
    Char = 0
    Boolean = 1
    Integer = 2
    Struct = 3
    Error = 4
    Void = 5

class STable:
    def __init__(self, name='', entrys={}, parent=None, tt=None, stype='scope'):
        self.name = name
        self.entrys = entrys
        self.parent = parent
        self.typeTable = tt
        self.scopeType = stype
    
    def lookup(self, name):
        if name not in self.entrys:
            return self.parent and self.parent.lookup(name)
        return self.entrys[name]
        
    def add(self, symbol):
        self.entrys[symbol.name] = symbol
        
    def delete(self, name):
        if name in self.entrys:
            del self.entrys[name]
    
    def addType(self, t):
        self.typeTable.add(t)

    def typeExists(self, t, spec=None):
        if t in self.typeTable.entrys:
            entry = self.typeTable.entrys[t]
            return ((entry.type == spec) or not spec) and entry
        return self.parent and self.parent.typeExists(t, spec)

class Symbol:
    def __init__(self, name, stype, offset=0, param=False, listSize=0):
        self.name = name
        self.stype = stype
        self.offset = offset
        self.param = param
        self.listSize = listSize


class TypeItem:
    def __init__(self, name, size=0, type='struct', paramlist={}, ret=None):
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
        self.entrys['char'] = TypeItem(type_enum.Char, 1)
        self.entrys['int'] = TypeItem(type_enum.Integer, 4)
        self.entrys['boolean'] = TypeItem(type_enum.Boolean, 1)
        self.entrys['void'] = TypeItem(type_enum.Void, 0)

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

    def add(self, t):
        self.entrys[t.name] = t
    
    def getSize(self, name):
        if name in self.entrys:
            return self.entrys[name].size

        return None

    def getParams(self, name):
        if name in self.entrys:
            return self.entrys[name].paramlist

        return None