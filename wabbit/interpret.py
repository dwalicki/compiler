from model import *


# formal type system mapping
class WType:
    pass


class WInt(WType):
    def __init__(self, value):
        self.value = int(value)

    def __repr__(self):
        return f"WInt({self.value})"


class WFloat(WType):
    def __init__(self, value):
        self.value = int(value)

    def __repr__(self):
        return f"WFloat({self.value})"


class WBool(WType):
    pass


class WChar(WType):
    pass


class WVoid(WType):
    pass


class WUndefined:
    pass


class WEnvironment:
    def __init__(self):
        self.data = {}

    def define(self, name, val):
        # what if it already exists?
        self.data[name] = val

    def lookup(self, name):
        # what if it doesn't exist?
        return self.data[name]

    def store(self, name, value):
        # what if it doesn't exist?
        self.data[name] = value


# Interprets a node of Wabbit code and returns a value from Wabbit
def interpret(node: Node, environ: WEnvironment) -> WType:
    """
    Interpret each node
    :param node:
    :return:
    """
    if isinstance(node, Integer):
        pass
    elif isinstance(node, Float):
        pass
    elif isinstance(node, BinOp):
        pass
    elif isinstance(node, Op):
        pass
    elif isinstance(node, Name):
        val = environ.lookup(node.text)
        if isinstance(val, WUndefined):
            raise RuntimeError(f"Undefined name: {node.text}")
    elif isinstance(node, PrintStatement):
        val = interpret(node.value, environ)
        print(val)
        return WVoid()
    elif isinstance(node, VarDeclaration):
        # what if there is no value?
        if node.value:
            val = interpret(node.value, environ)
        else:
            val = ...
        environ.define(node.name.text, val)
        return WVoid()
    elif isinstance(node, FuncDeclaration):
        pass
    elif isinstance(node, Statements):
        return_val = WVoid
        for statement in node.statements:
            return_val = interpret(statement)
        return return_val
    else:
        raise RuntimeError(f"Interpreter failure on node: {node}")
