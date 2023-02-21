# main.py
from format import format_wabbit
from interpret import interpret_wabbit
from model import *

program1 = PrintStatement(Integer("42"))

program2 = Statements(
    [
        PrintStatement(BinOp(Op("+"), Integer("2"), Integer("3"))),
        PrintStatement(BinOp(Op("+"), Unary(Op("-"), Integer("2")), Integer("3"))),
        PrintStatement(
            BinOp(
                Op("+"),
                Integer("2"),
                BinOp(Op("*"), Integer("3"), Unary(Op("-"), Integer("4"))),
            )
        ),
        PrintStatement(
            BinOp(
                Op("*"),
                Grouping(BinOp(Op("+"), Integer("2"), Integer("3"))),
                Integer("4"),
            )
        ),
        PrintStatement(
            BinOp(Op("-"), Float("2.0"), BinOp(Op("/"), Float("3.0"), Float("4")))
        ),
    ]
)

program3 = Statements(
    [
        ConstDeclaration(Name("pi"), None, Float("3.14159")),
        ConstDeclaration(Name("tau"), None, BinOp(Op("*"), Float("2.0"), Name("pi"))),
        VarDeclaration(Name("radius"), None, Float("4.0")),
        VarDeclaration(Name("perimeter"), Typename("float"), None),
        Assignment(Name("perimeter"), BinOp(Op("*"), Name("tau"), Name("radius"))),
        PrintStatement(Name("perimeter")),
    ]
)

program4 = Statements(
    [
        PrintStatement(Bool("true")),
        PrintStatement(BinOp(Op("=="), Integer("1"), Integer("1"))),
        PrintStatement(BinOp(Op("<"), Integer("0"), Integer("1"))),
        PrintStatement(BinOp(Op(">"), Integer("1"), Integer("0"))),
        PrintStatement(BinOp(Op("&&"), Bool("true"), Bool("true"))),
        PrintStatement(BinOp(Op("||"), Bool("false"), Bool("true"))),
        PrintStatement(Unary(Op("!"), Bool("false"))),
    ]
)

program5 = Statements(
    [
        VarDeclaration(Name("a"), Typename("int"), Integer("2")),
        VarDeclaration(Name("b"), Typename("int"), Integer("3")),
        VarDeclaration(Name("minval"), Typename("int"), None),
        IfStatement(
            BinOp(Op("<"), Name("a"), Name("b")),
            Statements([Assignment(Name("minval"), Name("a"))]),
            Statements([Assignment(Name("minval"), Name("b"))]),
        ),
        PrintStatement(Name("minval")),
    ]
)

program6 = Statements(
    [
        VarDeclaration(Name("x"), Typename("int"), Integer("1")),
        VarDeclaration(Name("fact"), Typename("int"), Integer("1")),
        WhileStatement(
            BinOp(Op("<"), Name("x"), Integer("11")),
            Statements(
                [
                    Assignment(Name("fact"), BinOp(Op("*"), Name("fact"), Name("x"))),
                    Assignment(Name("x"), BinOp(Op("+"), Name("x"), Integer("1"))),
                    PrintStatement(Name("fact")),
                ]
            ),
        ),
    ]
)

program7 = Statements(
    [
        VarDeclaration(Name("n"), None, Integer("5")),
        WhileStatement(
            Bool("true"),
            Statements(
                [
                    IfStatement(
                        BinOp(Op("=="), Name("n"), Integer("0")),
                        Statements([BreakStatement()]),
                        Statements(
                            [
                                PrintStatement(Name("n")),
                                Assignment(
                                    Name("n"), BinOp(Op("-"), Name("n"), Integer("1"))
                                ),
                                ContinueStatement(),
                            ]
                        ),
                    ),
                    Assignment(Name("n"), BinOp(Op("+"), Name("n"), Integer("1"))),
                ]
            ),
        ),
    ]
)

program8 = Statements(
    [
        FuncDeclaration(
            Name("add"),
            [
                Parameter(Name("x"), Typename("int")),
                Parameter(Name("y"), Typename("int")),
            ],
            Typename("int"),
            Statements([ReturnStatement(BinOp(Op("+"), Name("x"), Name("y")))]),
        ),
        VarDeclaration(
            Name("result"),
            None,
            FunctionCall(Name("add"), [Integer("2"), Integer("3")]),
        ),
        PrintStatement(Name("result")),
    ]
)


def format_programs():
    print("program 1:")
    print(format_wabbit(program1))

    print("program 2:")
    print(format_wabbit(program2))

    print("program 3:")
    print(format_wabbit(program3))

    print("program 4:")
    print(format_wabbit(program4))

    print("program5:")
    print(format_wabbit(program5))

    print("program 6:")
    print(format_wabbit(program6))

    print("program 7:")
    print(format_wabbit(program7))

    print("program 8:")
    print(format_wabbit(program8))


def interpret_programs():
    print("Running program 1:")
    interpret_wabbit(program1)

    print("running program 2:")
    interpret_wabbit(program2)

    print("running program 3:")
    interpret_wabbit(program3)

    print("runing program 4:")
    interpret_wabbit(program4)

    print("running program 5:")
    interpret_wabbit(program5)

    print("running program 6:")
    interpret_wabbit(program6)

    print("running program 7:")
    interpret_wabbit(program7)

    print("running program 8:")
    interpret_wabbit(program8)


if __name__ == "__main__":
    user_input = input(
        "Enter F to run format methods or I to run interpret methods'\n"
    ).upper()

    if user_input == "F":
        format_programs()
    elif user_input == "I":
        interpret_programs()
    else:
        print("Invalid entry please try again")
