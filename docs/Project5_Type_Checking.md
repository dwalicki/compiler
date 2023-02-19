# Project 5 - Type Checking

So far, everything you have coded has been on the "Happy Path."  We
have assumed that programs are correct.  All of the test programs in
`tests/Programs/` are correct programs.  However, most programmers
make mistakes from time to time (or even most of the time).  It would
be nice to give them some useful error messages.  That is the goal of
this project.

## An Example

Many of the programming mistakes made by programmers are related to
bad usage of types and names.  Here are a few examples:

```
print 2 + 3.4;       // Type error: int + float
print x;             // Error. 'x' is undefined.

const pi = 3.14159;
pi = 2.0;            // Error. pi is const.
```

Ideally, it would be nice to tell the programmer exactly what's wrong
with a nice error message.

## Dynamic Checking

One approach to error handling is to rely upon runtime checks.  As a
program executes, you can check for type errors, bad variable names,
and other kinds of problems.  This is the basis of dynamic typing, an
approach taken by languages such as Python.

To make such checking work, the runtime environment of the program
needs to carry additional information about the program.  For example,
every value would need to know its associated type.  Different
operators such as `+` and `-` would need to check the types of their
operands before they execute.  You may have already implemented such
checks in your interpreter.

A criticism of dynamic checking is that it makes programs run
significantly slower due to repeated checking.   Also, programming
errors aren't discovered unless the code actually executes (a
potential problem for rarely executed code paths).  

## Static Checking

A different approach to error handling is to try and catch all errors
in advance as a special step before any code ever runs or is
generated.  This idea is the basis of static type checking.

A type-checker, in some sense, is an "interpreter" that *only*
performs error checking.  Instead of literally executing a program, a
checker looks at the program model and determines what it would do *if* it
actually executed.  As an example, suppose you had an arithmetic
expression like this:

```
2 + 3
```

Instead of literally performing that calculation, a type checker would
view the expression as a higher-level operation like this:

```
int + int
```

It would then conclude that the result of the calculation has type "int".
This is *NOT* the same as actually performing the calculation. It's
just reasoning about the nature of the calculation. The actual values
don't matter (whatever they are, you know the result is still an "int").

In the process of examining the code, a type checker will uncover
errors.  For example, if it encountered a fragment of code like this:

```
2 + true
```

It would look at the underlying types and see:

```
int + bool
```

Because the types of the left and right operands don't match up,
an error would be reported.

## Your Task

Your task is to implement a type-checker for Wabbit.  It will
run after parsing has taken place, but before any kind of
code generation or interpretation.

The structure of the type-checker is going to be similar to the
interpreter.  You'll write a high-level function like this:

```
def typecheck(model, context):
    ...
    if isinstance(node, ModelClass):
       # Type-check "node" in the environment "context"
       ...
       return result_type
```

The input to typecheck() will be an object from model.py (node) along
with an object respresenting the known information about environment
(context).  In this case, the context might contain information about
variable declarations, types, and other details needed to check the
code.  Typically, the return result of type-checking will be the type
of the Wabbit value that would be produced by the operation.

## Tips

This part of the project is very open ended.  Finding every possible
programming problem is likely to be difficult given the timing
of the project.   However, you should be able to detect certain
kinds of "easy" problems like name errors, type errors in math
expressions, and other things.

You could choose to do nothing in which case your compiler will
likely "work" for correct code, but will fail miserably if
someone gives it an incorrect Wabbit program.

## Testing

The testing of this part of the project involves making intentional
Wabbit programming errors.  Most of these errors relate to types and
names.  Here are some examples:

```
print 2 + 3.4;       // Type error: int + float
print x;             // Error. 'x' is undefined.

const pi = 3.14159;
pi = 2.0;            // Error. pi is immutable.
```

To run a check, you might have it work as a stand-alone step. For
example:

```
bash $ python check.py errors.wb
Line 1: Type error: int + float
Line 2: 'x' undefined
Line 5: 'pi' is immutable.
bash $
```

The `tests/Error` directory has an assortment of programs with errors.

## Tips

This part of the project is very open ended.  Finding every possible
programming problem is likely to be difficult given the timing
of the project.   However, you should be able to detect certain
kinds of "easy" problems like name errors, type errors in math
expressions, and other things.

For success, you need to focus on specific programming elements in
isolation.  For example, consider an assignment statement like this:

```
location = expression;
```

Now, think about everything that could possibly go wrong with it?

* The expression on the right could have a type error inside of it.  For example, `x = 2 + 3.5;`.  To find this, you must check the expression separately.
* The type of the location on the left is different than the type of the expression on the right (you're trying to assign an `int` to a `float`).
* The location on the left doesn't exist (undefined name)
* The location on the left is immutable (const)

A lot of this is about being a language lawyer and understanding fine details.

## What are the Consequences of Bad Type Checking?

If you fail to find errors, the main consequence is that your compiler
will provide a very poor user experience to the hapless Wabbit user.
Instead of giving an informative error message, your compiler will
either crash on its own (internal compiler error) or the generated
code will crash somehow (e.g., die with a segmentation fault).
Neither of those failure modes are very helpful. People will
flame Wabbit on Hacker News for its lousy error handling.

On the other hand, if you do no type checking whatsoever, your
compiler will still happily compile correct programs.  So, at least
there's still that.

## Note about Functions

When you make your type checker to handle functions, you'll need to
worry about scoping of variables (local vs. global scope) as well
as issues related to function calls themselves.  For example, making
sure the number of arguments match, the types of the arguments match,
and so forth.  There are a lot of picky details.  Expect this to take
a lot of time.  You may want to wait until later.



