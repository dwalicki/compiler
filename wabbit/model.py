# model.py
from dataclasses import dataclass


# Defines the data structures that represent the different program
# elements (literals, expressions, statements, loops, etc.)


class Node:
    pass


class Expression(Node):
    pass


class Statement(Node):
    pass


class Declaration(Statement):
    pass


class Type(Node):
    pass


@dataclass
class Typename(Type):
    text: str


@dataclass
class Statements(Node):
    statements: list[Statement]


@dataclass
class Name(Expression):
    text: str


@dataclass
class Parameter(Expression):
    type: str


@dataclass
class Integer(Expression):
    value: str


@dataclass
class Float(Expression):
    value: str


@dataclass
class Bool(Expression):
    value: str


@dataclass
class BreakStatement(Statement):
    pass


@dataclass
class ContinueStatement(Statement):
    pass


@dataclass
class PrintStatement(Statement):
    value: Expression


@dataclass
class Function(Node):
    name: Name
    parameters: list[Parameter]
    return_type: Type
    body: Statements


@dataclass
class Op(Node):
    symbol: str


@dataclass
class BinOp(Expression):
    op: Op
    lhs: Expression
    rhs: Expression


@dataclass
class Unary(Expression):
    op: Op
    operand: Expression


@dataclass
class FunctionCall(Expression):
    name: Expression
    arguments: list[Expression]


@dataclass
class Grouping(Expression):
    value: Expression


@dataclass
class ConstDeclaration(Declaration):
    name: Name
    type: Type | None
    value: Expression | None


@dataclass
class VarDeclaration(Declaration):
    name: Name
    type: Type | None
    value: Expression | None


@dataclass
class Assignment(Statement):
    lhs: Name
    rhs: Expression


@dataclass
class IfStatement(Statement):
    test: Expression
    consequence: Statements
    alternative: Statements | None


@dataclass
class WhileStatement(Statement):
    test: Expression
    body: Statements


@dataclass
class Parameter(Declaration):
    name: Name
    type: Type


@dataclass
class FuncDeclaration(Declaration):
    name: Name
    parameters: list[Parameter]
    return_type: Type
    body: Statements


@dataclass
class ReturnStatement(Statement):
    value: Expression
