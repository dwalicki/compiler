# Write a Compiler - Preparation Exercises

The following exercises are meant as a bit of warmup for the compiler
project. Don't spend tons of time on these, but coding a solution will
start to prepare you for the proper mindset.

## Exercise 1: Tokenizing

As input, a compiler needs to read source code.  To do this, it first
has to recognize certain pattens in the code such as names, number,
operators, and so forth.  This step is known as tokenizing.  Implement
the following `tokenize()` function.  It takes a string as input and
produces a sequence of tuples of the form `(toktype, value)` where
`toktype` is a token type and `value` is a string of the matching
text:

```
def tokenize(text):
    ...

assert list(tokenize("spam = x + 34 * 567")) == \
    [ ('NAME', 'spam'), ('ASSIGN', '='), ('NAME', 'x'), 
      ('OP', '+'), ('NUM', '34'),('OP', '*'), ('NUM', '567')]
```

## Exercise 2: Trees

Inside a compiler, source code is usually represented by some sort of tree
structure.  Trees are usually recursive in nature--as are the algorithms
for dealing with the data.   The following tree represents source code
in the form of an S-expression.   It's built using tuples.

```
tree = ('assign', 'spam', 
        ('binop', '+', 
                  ('name', 'x'),
                  ('binop', '*',
		            ('num', '34'),
			    ('num', '567'))))
```

Your task is to take this tree and turn it into an fragment of valid Python
code.  Specifically, you need to write a function `to_source()` that works
like this:

```
def to_source(tree):
    ... # you define

assert to_source(tree) == 'spam = x + 34 * 567'
```

## Exercise 3: Tree rewriting

Write a function that takes a tree of text strings as input and
creates a new tree where all of the numbers have been converted
from strings into integers:

```
def convert_numbers(tree):
    ...

tree = ('assign', 'spam', 
        ('binop', '+', 
                  ('name', 'x'),
                  ('binop', '*', ('num', '34'), ('num', '567'))))

assert convert_numbers(tree) == \
    ('assign', 'spam', ('binop', '+', ('name', 'x'), ('binop', '*', ('num', 34), ('num', 567))))    
```

## Exercise 4: Tree simplification

Write a function that takes a tree and looks for places where mathematical
operations can be carried out and simplified. A new simplified tree is returned:

```
def simplify_tree(tree):
    ...

tree = ('assign', 'spam', 
        ('binop', '+', 
                  ('name', 'x'),
                  ('binop', '*', ('num', 34), ('num', 567))))

assert simplify_tree(tree) == \
    ('assign', 'spam', ('binop', '+', ('name', 'x'), ('num', 19278)))
```

