# Project 2 - The Interpreter

In this project, you will build an interpreter that directly executes
Wabbit from the associated data model.  Essentially you will be able
to take all of the models you defined in project 1 and make them run
in some way. The purpose of this project is to understand how programs
evaluate--basically the semantic properties of programs.

## Overview

In order to write a compiler for a programming language, it helps to
have some kind of understanding of how programs written in the
programming language are actually supposed to work. A language is
more than just "syntax" or a data model.  There have to be some kind
of semantic rules that describe what happens when a program in the
language executes.   Knowing the semantics is also essential for
testing.

One way to specify the semantics is to write an interpreter, which is a
progra that directly executes the data model. This might seem like
cheating--after all, our final goal is not to write an interpreter,
but a compiler. However, if you can't write an interpreter, chances
are you can't write a compiler either.  So, the purpose of doing
this is to pin down fine details as well as our overall
understanding of what needs to happen when programs run.  Writing an
interpreter will also help understand things that are *NOT* supposed
to happen (i.e., programming errors).

## Writing an Interpreter

To write an interpreter, start by defining a top-level function called
"interpret()".  For each class in your model,  you'll 
write a conditional check and some code that directly executes that
element. As an example, here's what a print statement might look like:

```
def interpret(node, context):
    ...
    if isinstance(node, PrintStatement):
        value = interpret(node, context)
        print(value)
	return None
```

The input to the interpret() will be an object from your model (node)
along with an object respresenting the execution environment
(context).  In executing certain nodes, the context might be
modified (for example, when executing assignment expressions,
making variable definitions, etc.).  The return result will
represent a value in Wabbit although statements such as `print`
might not return any interesting value.  

## Testing

You should test your interpreter by having it directly run the program models
you created in Project 1.   Specifically, you should be able to execute
the programs in `tests\Model\program1-8.wb`.

## Tips

A common confusion when writing the interpreter is understanding the
difference between expressions and statements.  An expression is code
that represents a value when evaluated.  For example, `2`, `2+3`, or
`2+(3*4)` are all expressions.  A statement is code that carries out
some kind of control-flow action or has a side-effect when evaluated.
For example, `print`, `if`, and `while` are statements.  Statements do
NOT return values. From an organizational perspective, it might make
sense to divide the interpreter into separate parts related to
expressions and statements.

A significant challenge in writing the interpreter is wrapping your
brain around the difference between the implementation language of the
interpreter (e.g., Python) and the language being interpreted
(Wabbit).  For example, Python has its own system of types, data
representation, and so forth.  This system is NOT the same as Wabbit.
For example, dividing two integers like `7/4` produces `1.75` in
Python.  In Wabbit, the result is truncated to `1`.

To more cleanly separate things in your mind, it might make sense to
define a special data structure representing a Wabbit value. This
structure would hold the Wabbit type and a Python value holding
the associated value. For example:

```
class WValue:
    def __init__(self, wtype, pvalue):
        self.wtype = wtype      # Wabbit type 
	self.pvalue = pvalue    # Value (as represented in Python)

# Examples
x = WValue('int', 3)
y = WValue('float', 3.5)
```

A naming convention may also help. In this code, names starting with
"w" are associated with Wabbit whereas names starting with "p" are
associated with Python.

Here's what an interpret function might look like with this special type:

```
def interpret(node, context) -> WValue:
    if isinstance(node, Integer):
        return WValue('int', int(node.value))
    ...
```

The use of a special `WValue` class also allows you to more easily
handle corner cases.  For instance, the `print` statement in Wabbit
always includes a newline EXCEPT when printing characters.  You could
write an explicit check for that:

```
def interpret(node, context):
    ...
    if isinstance(node, PrintStatement):
        wvalue = interpret(node.value)
	if wvalue.wtype == 'char':
	    print(wvalue.pvalue., end='')
	else:
	    print(wvalue.pvalue)
```

If you are using a language other than Python, you will almost
certainly need to define a special `WValue` type that relies upon
inheritance, interfaces, tagged unions, or enums.  Otherwise, you may
find it difficult to get your interpreter to type-check correctly when
compiling.

## Note about Functions

Implementing functions is likely to be the most difficult part of this
project.  This is because functions require you to think in more
detail about environments, scoping rules, stack frames, and other
runtime details.  Many of these details take you into the realm of
programming language theory.  As this isn't a course on "programming
languages" per se, it's best to view the implementation of functions
as a challenge.  Based on your understanding of how functions work
in a typical programming language, try to implement them.

It's also okay to ignore functions for now.  You can come back to it
later after we have further discussion.





