# Format the program data structure
from model import *


def format_wabbit(node: Node):
    return _format(node, Context())


class Context:
    def __init__(self, indent=""):
        self.indent = indent

    def new(self):
        return Context(self.indent + "    ")


def _format(node: Node, ctx: Context) -> str:
    if isinstance(node, Integer):
        return node.value
    elif isinstance(node, Float):
        return node.value
    elif isinstance(node, Bool):
        return node.value
    elif isinstance(node, Name):
        return node.text
    elif isinstance(node, Typename):
        return node.text
    elif isinstance(node, Op):
        return node.symbol
    elif isinstance(node, Unary):
        return f"{_format(node.op, ctx)}{_format(node.operand, ctx)}"
    elif isinstance(node, BinOp):
        return (
            f"{_format(node.lhs, ctx)} {_format(node.op, ctx)} {_format(node.rhs, ctx)}"
        )
    elif isinstance(node, PrintStatement):
        return f"print {_format(node.value, ctx)};\n"
    elif isinstance(node, BreakStatement):
        return "break;\n"
    elif isinstance(node, ContinueStatement):
        return "continue;\n"
    elif isinstance(node, Grouping):
        return f"({_format(node.value, ctx)})"
    elif isinstance(node, ConstDeclaration):
        code = f"const {_format(node.name, ctx)}"
        if node.type:
            code += f" {_format(node.type, ctx)}"
        code += " = " + _format(node.value, ctx) + ";\n"
        return code
    elif isinstance(node, VarDeclaration):
        code = f"var {_format(node.name, ctx)}"
        if node.type:
            code += f" {_format(node.type, ctx)}"
        if node.value:
            code += " = " + _format(node.value, ctx)
        return code + ";\n"
    elif isinstance(node, Assignment):
        return f"{_format(node.lhs, ctx)} = {_format(node.rhs, ctx)};\n"
    elif isinstance(node, IfStatement):
        code = f"if {_format(node.test, ctx)} " + "{\n"
        code += _format(node.consequence, ctx.new()) + ctx.indent + "}"
        if node.alternative:
            code += " else {\n"
            code += _format(node.alternative, ctx.new()) + ctx.indent + "}"
        return code + "\n"
    elif isinstance(node, WhileStatement):
        code = f"while {_format(node.test, ctx)} " + "{\n"
        code += _format(node.body, ctx.new()) + "}"
        return code + "\n"
    elif isinstance(node, ReturnStatement):
        code = f"return {_format(node.value, ctx)};\n"
        return code
    elif isinstance(node, FuncDeclaration):
        code = f"func {_format(node.name, ctx)}("
        param_str = []
        for param in node.parameters:
            param_str.append(f"{_format(param.name, ctx)}: {_format(param.type, ctx)}")
        code += ", ".join(param_str)
        code += f") {_format(node.return_type, ctx)} " + "{\n"
        code += _format(node.body, ctx.new()) + ctx.indent + "}\n"
        return code
    elif isinstance(node, FunctionCall):
        code = f"{_format(node.name, ctx)}("
        arg_str = []
        for arg in node.arguments:
            arg_str.append(f"{_format(arg, ctx)}")
        code += ", ".join(arg_str)
        code += ")"
        return code
    elif isinstance(node, Statements):
        code = ""
        for statement in node.statements:
            code += ctx.indent + _format(statement, ctx)
        return code
    else:
        raise RuntimeError(f"Node type not recognized: {node}")
