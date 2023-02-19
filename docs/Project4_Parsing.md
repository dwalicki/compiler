# Project 4 - Parsing

In this project, we'll write a proper parser that allows
us to build data models directly from source code as opposed to having
to build them by hand in the initial project.   

Parsing is one of the more difficult parts of writing a compiler and
parsing theory is usually major topic in compiler books.  However, the
fundamental idea behind how parsing works is actually fairly
straightforward.  In this project, we'll write the parser by hand.
The project proceeds in two phases--the parsing of statements followed
by the parsing of expressions.

## The Problem

In a nutshell, parsing is a problem of pattern matching.  The Wabbit
language has a variety of different features.  For example, a `print`
statement:

```
print 42;
```

Or an binary expression:

```
1 + 2
```

The goal of a parser is to recognize these patterns in the token sequence
and convert those patterns into the AST/model that you already
defined.  For example:

```
PrintStatement(Integer('42'))
Add(Integer('1'), Integer('2'))
```

## Syntax Specification

The first problem involves the specification of syntax.  How do you
precisely define the above patterns?  One approach is to use a grammar
written as a BNF or EBNF. In a BNF, each language feature is described
by a kind of equation.  Here's the definition of a `print` statement:

```
print_statement := PRINT expression SEMI
```

In this definition, words in all-caps such as `PRINT` and `SEMI`
represent tokens.  The lowercase `expression` refers to a pattern that
must be parsed separately and which is defined by its own equation
(not shown here).

Every feature of Wabbit can be described in such manner. You will find
an example if you look at the end of the [Wabbit
Specification](Wabbit-Specification.md).

An alternative approach for specifying syntax is to use syntax
diagrams.  See [WabbitSyntax](WabbitSyntax.pdf) for an example.

## How Parsing Works at a High Level

Parsing algorithms generally work left-to-right with the token stream.
Structurally, you will write a separate parsing function for each
Wabbit programming language feature.  For example:

```
def parse_print_statement(parser):
    ...

def parse_while_statement(parser):
    ...

def parse_if_statement(parser):
    ...

def parse_expression(parser):
    ...

...
```

Within each function, you will walk left-to-right either matching a token
or descending into a lower-level parsing rule.   The final result of
each parsing function is a node from your model or AST.  As an example, here
is pseudocode for parsing a `print` statement:

```
def parse_print_statement(parser):
    parser.expect('PRINT')     # Requires next token to match or error
    value = parse_expression(parser)
    parser.expect('SEMI')
    return PrintStatement(value)
```

There are obviously a few more details that need to be worked out, but
we'll discuss this as a group.

## Part 1 - Statements

For the first part of the project, we will focus on matching Wabbit
statements.  To do this, we're going to restrict expression parsing to
only work with a single integer value and nothing else.  With this
restriction, here are examples of the statements we'll parse:

```
break;
continue;
print 1;
const x = 1;
var x int;
if 1 { print 2; } else { print 3; }
while 1 { print 2; }
1;             
```

For testing, we will be working from the first 9 programs found in
`tests/Parser`. Each of these programs contains some sample code along
with further instructions/tips about how to proceed.

## Part 2 - Expressions

The second part of the project will expand the parsing of expressions.
Expression parsing is probably the most difficult part of writing the
parser because expressions need to capture precedence rules from math
class.  For example, how is the following expression to be parsed?

```
2 + 3 * 4 < 30 / 6 - 7
```

There are essentially different parsing precedence "levels".  For example, to
evaluate this expression, multiplication and division must go first:

```
2 + (3 * 4) < (30 / 6) - 7      # 2 + Mul(3, 4) < Div(30, 6) - 7
```

Addition and subtraction then go next:

```
(2 + (3 * 4)) < ((30 / 6) - 7)  # Add(2, Mul(3, 4)) < Sub(Div(30, 6), 7)
```

The relation goes last, producing the following AST:

```
Lt(Add(2, Mul(3, 4)), Sub(Div(30, 6), 7))
```

A major challenge involves figuring out how to group terms with
similar precedence levels together.  One way to do this is to define a
separate parsing rule for each level.  Alternatively, you could
implement something such as the [Shunting Yard
Algorithm](https://en.wikipedia.org/wiki/Shunting_yard_algorithm).
The [Crafting Interpreters](https://craftinginterpreters.com/parsing-expressions.html)
book also has a good chapter on the problem of expression parsing.

For testing of expressions, we will continue to work with programs
10-18 in `tests/Parser`.  Each program contains comments with further
instructions.

## Part 3 - An Interpreter

Once your parser is able to handle more complete programs, you should
hook it up to the interpreter you wrote in Project 2.  Have your
compiler accept a filename as input, parse the file into an AST/model,
and execute the model using your interpreter.

The `tests/Programs` directory has a series of more complete programs
that attempt to exercise all of the core features of Wabbit.  See how
many of these programs you can get to run.

Here is an example of what it might look like to run the parser and
see the resulting output on one of these programs:

```
bash $ cat tests/Programs/12_loop.wb
/* 12_loop.wb

   Test of a while-loop
*/

var n int = 1;
var value int = 1;

/* Prints out the first 10 factorials */
while n <= 10 {
    value = value * n;
    print value ;
    n = n + 1;
}
```

Run the parser on the file (assumes you're working the `wabbit/`
directory)

```
bash $ python parser.py ../tests/Programs/12_loop.wb
Statements([Variable(Name(n), Typename(int), Integer(1)), ...])
```

The exact output will vary according to how you've defined your
AST/model.

Here's what it might look like to run the program through the
interpreter:

```
bash $ python interp.py ../tests/Programs/12_loop.wb
1
2
6
24
120
720
5040
40320
362880
bash $
```

If this works, congratulate yourself. You just wrote the core of a
interpreted language like Python--albeit a really slow one.

## Tips

A significant portion of this project will be live-coded as a
group. By far, the most difficult part of parsing concerns
expressions.  Expect significant discussion around that.

One subtlety of Wabbit is that variable assignment is an expression.

```
x = 2 + 3;
```

The value of an assignment is the right hand side.  So, statements
such as this are legal:

```
print x = 2 + 3;     // Prints 5, assigns to x.
```

Assignments can also be chained:

```
x = y = 2 + 3;
```

This is to be interpreted to mean the following:

```
x = (y = 2 + 3);
```

If you are going to tackle functions, think about all of the different
parts involved (parameter lists, arguments, function calls, return
statements, etc.).  Depending on the status of functions in other
parts of your compiler, you may want to defer this until later.


