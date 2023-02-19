# Project 1 - The Model

To start the compiler project, we're going to focus on the problem of
representing programs as a proper data structure.  In this case, we're
focused on the problem of representing Wabbit.  See the
[Wabbit Specification](Wabbit-Specification.md).

## Setup

Before you begin, make sure you remember to make your own branch
of the repo.

```
bash $ git checkout -b yourname
bash $ git push origin -u yourname
```

Find the `wabbit/` directory.   This is where you will code your
compiler implementation.   If you need to do any setup related to
your programming language (creation of a project, etc.) do it here.

In the directory `tests/Model`, you will find a collection of very
short Wabbit programs.  These will be the focus of our attention for
this starting project.

## Programs as Data

The input to a compiler is typical presented as text strings called
source code. However, a compiler doesn't want to work with your
program as text. Text is messy and painful to work with. Instead, a
compiler would much rather have a proper data structure representing
the contents and structure of the program.  Typically, this is a tree
structure known as an "Abstract Syntax Tree" although I tend to
prefer the much more generic term "model."  Essentially, you need to
have some kind of data model that represents the structure of a
Wabbit program.

As an example, suppose you had a Wabbit statement such as
this:

```
print 2 + 3 * 4;
```

The source code is a raw string like this:

```
source = "print 2 + 3 * 4;"
```

However, we DON'T want that!   We want a data structure instead.
One possibility might be to encode the data into a series of
tagged tuples like this:

```
program = ('print', ('+', ('int', 2), ('*', ('int', 3), ('int', 4))))
```

In this representation, each tuple starts with a "tag" that indicates
what the tuple represents. The remaining values represent the contents.
Note: You can more clearly see the tree-like structure if you write
it out differently:

```
program = ('print',
                    ('+',
                         ('int', 2),
                         ('*',
                              ('int', 3),
                              ('int', 4),
                         ),
                    ),
          )
```

As subtle facet of this tree is that it encodes some rules about
operator precedence from math class.  For example, in the expression
`2 + 3 * 4`, the proper evaluation order is `2+(3*4)`, not `(2+3)*4`.
The tree structure reflects this.

Another possibility is to represent a program using a series of
class or structure definitions.   For example, in Python:

```
class Node:
      pass
      
class PrintStatement(Node):
    def __init__(self, value):
        self.value

class Integer(Node):
    def __init__(self, value):
        self.value

class Add(Node):
    def __init__(self, left, right):
        self.left = left
	self.right = right

class Mul(Node):
    def __init__(self, left, right):
        self.left = left
	self.right = right

program = PrintStatement(
                Add(
		    Integer(2),
                    Mul(
		        Integer(3),
			Integer(4)
			)
		)
	  )
```

Again, it's important to note that the representation involves nesting.  For
instance, the `+` operation involves a left and right side.  The right
side, in this case, involves another operation `*` with its own left
and right side.

This is not the only way to encode the data.  For example, instead of
having separate `Add` and `Mul` classes, one could also have a
more generic `BinOp` class representing a binary operator:

```
class Op:
    def __init__(self, op):
    	self.op = op
	
class BinOp:
    def __init__(self, op, left, right):
        self.op = op
	self.left = left
	self.right = right

program = PrintStatement(
               BinOp(Op('+'),
                     Integer(2),
                     BinOp('*',
                           Integer(3),
                           Integer(4)
                     )
               )
         )
```

The key point: whatever you do, it must be some kind of data structure.

## Working with the Model

The data model forms the core of the whole compiler.  Almost
everything that you'll do later will need to work with this data
structure.  To learn how to use it, one of the first tools you should
write is a code formatter.  A code formatter takes a program,
represented using the model, and turns it back into source code.  In
some sense, a formatter is like a reverse compiler.  

Here is an example of how a formatter might work:

```
# A sample program
program = ('print', ('+', ('int', 2), ('*', ('int', 3), ('int', 4))))

# Turn the program into source code
def format(node):
    if node[0] == 'print':
        return 'print ' + format(node[1]) + ';\n'
    elif node[0] == 'int':
        return str(node[1])
    elif node[0] == '+':
        return format(node[1]) + ' + ' + format(node[2])
    elif node[0] == '*':
        return format(node[1]) + ' * ' + format(node[2])
    else:
        raise RuntimeError("What?!?!")

# Convert the program to source
print(format(program))
```

A key aspect of working with the data model is case-analysis.  You'll
often need to write functions that are presented with an object (`node`)
and then need to carry out some kind of action based on its type.
The problem of deciding what to do is based on a type-tag or by performing
type-checks.   For example, you could also do this:

```
def format(node):
    if isinstance(node, PrintStatement):
        return 'print ' + format(node.value) + ';\n'
    elif isinstance(node, Integer):
        return str(node.value)
    ...
```

An essential aspect of working with the model is recursion.
Programs almost always involves a lot of deeply nested structures.
To handle this, formatting will involve a lot of recursive calls
to navigate the tree structure as individual parts are formatted.

## Your Task

Your task is to define the core data structures used by the compiler
and to write a formatting function that turns those data structures
into source.

We will start by encoding (by hand) the simple Wabbit programs
found in `tests/Model` into their corresponding AST structure.
The purpose of this is two-fold:

1. Make sure we understand the internal data structures
   used by the compiler. We will need this to do everything else.

2. Have some program structures that we can use for later testing,
   debugging, and experimentation.

To start, go find the file `tests/Model/program1.wb`. Now, start
thinking about how you would represent that program as a data structure.
We will slowly work through programs 1-8 in that directory.

## How to Structure Your Code

Since we're starting from scratch, it's a bit hard to know how to
structure the project.  My advice is to create a separate file
called `model.py` that has all of the class definitions in it:

```
# model.py

class Integer:
    ...

class PrintStatement:
    ...

class BinOp:
    ...
```

Then make a file `format.py` that has the code formatting feature in it.

```
# format.py

def format_wabbit(node):
    ...
```

Finally, make a file `main.py` that manually carries out some tests.
The main file might look something like this:

```
# main.py
from model import *
from format import format_wabbit

program1 = PrintStatement(Integer(42))
print(format_wabbit(program1))
```

You'll expand the `main.py` program with more test cases as your work
on examples.  Eventually, the compiler will grow a more proper `main()`
function, but for now it can start as a script.

## Tips

You can implement the compiler in any programming language that you
wish.  However, if you are using a language with a strong type system,
you will need to spend some amount of time thinking about the overall
organization of your data structures.  This could involve the
definition of an inheritance hierarchy, unions, or enums.  The
trickiest thing to handle is the nesting of objects.  This often involves
a recursive data structure that may require pointers/references.
It could also involve tricky issues related
to garbage collection and memory management.

Be aware that writing a compiler involves a large amount of string
and text processing (especially some of the later stages related
to parsing).  This is also something worth figuring out early--your
strategy for representing and manipulating strings.

This first part of the project can involve a steep learning curve as
you figure out some the basics. This is normal!  Take it slow and work
out the details.  Other parts of the compiler project will reuse a lot
of the project that you work out here.   Also expect some refactoring 
as the project evolves.












