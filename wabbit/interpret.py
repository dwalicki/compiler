from model import *


# formal type system mapping
class WType:
    pass


class WInt(WType):
    def __init__(self, value):
        self.value = int(value)

    def __repr__(self):
        return f'WInt({self.value})'


class WFloat(WType):
    def __init__(self, value):
        self.value = float(value)

    def __repr__(self):
        return f'WFloat({self.value})'


class WBool(WType):
    """Converts a string 'true' or 'false' to a bool type"""

    def __init__(self, value):
        assert value in {'true', 'false', True, False}
        self.value = True if (value == 'true' or value == True) else False

    def __repr__(self):
        return f'WBool({self.value})'


class WChar(WType):
    """One character"""

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'WChar({self.value})'


class WVoid(WType):
    def __init__(self):
        self.value = None

    def __repr__(self):
        return f'WVoid()'


@dataclass
class WFunc(WType):
    name: Name
    parameters: list[Parameter]
    return_type: Type
    body: Statements


class WUndefined:
    pass


class WEnvironment:
    def __init__(self, parent=None):
        self.data = {}
        self.parent = parent

    def define(self, name, val):
        # what if it already exists?
        self.data[name] = val

    def lookup(self, name: str) -> WType | WUndefined:
        if name not in self.data:
            if self.parent:
                return self.parent.lookup(name)
            else:
                return WUndefined()
        else:
            return self.data[name]

    def store(self, name, value):
        # what if it doesn't exist?
        self.data[name] = value


class WBreak(Exception):
    pass


class WContinue(Exception):
    pass


class WReturn(Exception):
    def __init__(self, value):
        self.value = value


def interpret_wabbit(node: Node):
    environ = WEnvironment()
    return interpret(node, environ)


# Interprets a node of Wabbit code and returns a value from Wabbit
def interpret(node: Node, environ: WEnvironment) -> WType:
    """
    Interpret each node
    :param environ:
    :param node:
    :return:
    """
    if node is None:
        return WVoid()
    if isinstance(node, Expression):
        return interpret_expression(node, environ)
    elif isinstance(node, Statement):
        interpret_statement(node, environ)
        return WVoid()
    elif isinstance(node, Statements):
        for statement in node.statements:
            interpret_statement(statement, environ)
        return WVoid()
    else:
        raise RuntimeError(f"Interpreter failure on node: {node}")


def interpret_expression(node: Node, environ: WEnvironment) -> WType:
    if isinstance(node, Integer):
        return WInt(node.value)
    elif isinstance(node, Float):
        return WFloat(node.value)
    elif isinstance(node, Bool):
        return WBool(node.value)
    elif isinstance(node, Unary):
        opval = interpret_expression(node.operand, environ)
        op = node.op
        if isinstance(opval, WInt):
            match op.symbol:
                case '-':
                    return WInt(-opval.value)
                case '+':
                    return WInt(opval.value)
        elif isinstance(opval, WFloat):
            match op.symbol:
                case '-':
                    return WFloat(-opval.value)
                case '+':
                    return WFloat(opval.value)
        elif isinstance(opval, WBool):
            if op.symbol == '!':
                return WBool(not opval.value)
    elif isinstance(node, BinOp):
        left = interpret_expression(node.lhs, environ)
        right = interpret_expression(node.rhs, environ)
        op = node.op
        if type(left) == WInt:
            match op.symbol:
                case '+':
                    result = WInt(left.value + right.value)
                case '-':
                    result = WInt(left.value - right.value)
                case '*':
                    result = WInt(left.value * right.value)
                case '/':
                    result = WInt(left.value / right.value)
                case '==':
                    result = WBool(left.value == right.value)
                case '<':
                    result = WBool(left.value < right.value)
                case '>':
                    result = WBool(left.value > right.value)
                case _:
                    raise RuntimeError(f'unsupported integer operator {op.symbol} on node {node}')
            return result
        elif type(left) == WFloat:
            match op.symbol:
                case '+':
                    result = WFloat(left.value + right.value)
                case '-':
                    result = WFloat(left.value - right.value)
                case '*':
                    result = WFloat(left.value * right.value)
                case '/':
                    result = WFloat(left.value / right.value)
                case '==':
                    result = WBool(left.value == right.value)
                case '<':
                    result = WBool(left.value < right.value)
                case '>':
                    result = WBool(left.value > right.value)
                case _:
                    raise RuntimeError(f'unsupported float operator {op.symbol} on node {node}')
            return result

    elif isinstance(node, Grouping):
        return interpret_expression(node.value, environ)
    elif isinstance(node, Op):
        pass
    elif isinstance(node, FunctionCall):
        func = interpret_expression(node.name, environ)
        if func is not WUndefined():
            args = [interpret_expression(arg, environ) for arg in node.arguments]
            # match arguments with parameters by order, name, or both
            global_parent = environ
            while global_parent.parent:
                global_parent = global_parent.parent
            func_env = WEnvironment(parent=global_parent)

            # add args to function environment
            for (pname, arg) in zip(func.parameters, args):
                func_env.define(pname.text, arg)
            # evaluate statements
            try:
                interpret(func.body, func_env)
            except WReturn as e:
                return e.value
        else:
            raise RuntimeError(f'Undefined function {node.name}')
    elif isinstance(node, Name):
        val = environ.lookup(node.text)
        if isinstance(val, WUndefined):
            raise RuntimeError(f'Undefined name: {node.text}')
        return val
    else:
        raise RuntimeError(f'Interpreter error: unsupported expression type on node: {node}')


def interpret_statement(node: Node, environ: WEnvironment):
    if isinstance(node, Assignment):
        val = interpret_expression(node.rhs, environ)
        environ.define(node.lhs.text, val)
        return WVoid()
    elif isinstance(node, PrintStatement):
        val = interpret(node.value, environ)
        if type(val) in {WFloat, WInt}:
            print(val.value)
        elif type(val) == WBool:
            print('true' if val.value else 'false')
        elif type(val) == WChar:
            print(val.value, end='')
        return WVoid()
    elif isinstance(node, VarDeclaration):
        # what if there is no value?
        if node.value:
            val = interpret(node.value, environ)
        else:
            val = None
        environ.define(node.name.text, val)
        return WVoid()
    elif isinstance(node, ConstDeclaration):
        if node.value:
            val = interpret_expression(node.value, environ)
        else:
            val = None
        environ.define(node.name.text, val)
        return WVoid()
    elif isinstance(node, IfStatement):
        test = interpret_expression(node.test, environ)
        if test.value:
            interpret(node.consequence, environ)
        else:
            interpret(node.alternative, environ)
    elif isinstance(node, WhileStatement):
        while True:
            testval = interpret_expression(node.test, environ)
            if not testval.value:
                break
            try:
                interpret(node.body, environ)
            except WBreak:
                break
            except WContinue:
                pass
    elif isinstance(node, BreakStatement):
        raise WBreak()
    elif isinstance(node, ContinueStatement):
        raise WContinue()
    elif isinstance(node, FuncDeclaration):
        return_type = interpret_type(node.return_type, environ)
        parameters = [p.name for p in node.parameters]
        environ.define(node.name.text, WFunc(node.name, parameters, return_type, node.body))
    elif isinstance(node, ReturnStatement):
        value = interpret_expression(node.value, environ)
        raise WReturn(value)
    elif isinstance(node, Statements):
        return_val = WVoid
        for statement in node.statements:
            return_val = interpret(statement, environ)
        return return_val
    else:
        raise RuntimeError(f'Interpreter failure: unexpected statement type on node: {node}')


typemap = {
    'int': WInt,
    'float': WFloat,
    'char': WChar,
    'bool': WBool
}


def interpret_type(node: Node, environ: WEnvironment) -> WType:
    if isinstance(node, Typename):
        return typemap[node.text]


if __name__ == '__main__':
    import sys
