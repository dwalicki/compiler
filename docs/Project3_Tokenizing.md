# Project 3 - Tokenizing

This project starts the process of building a parser that can take
Wabbit source text and turn it into the data model you created in
Project 1.   

## Overview

When a program is presented to a compiler, it is usually given in the
form of a text file.  A text file consists of raw characters.  The
contents would be read into a text string:

```
program = "print 123 + xy;"
```

Text strings look like arrays or lists of individual characters.
Conceptually, it's like this:

```
program = ['p','r','i','n','t',' ','1','2','3',' ','+','x','y',';']
```

This representation is inconvenient--it would be much easier to work
with more complete words.  For example:

```
program = ['print', '123', '+', 'xy', ';']
```

An even better representation includes additional information to
indicate the type of text that got matched.  For example:

```
program = [('PRINT', 'print'), ('INTEGER', '123'), ('PLUS', '+'),
           ('NAME', 'xy'), ('SEMI', ';') ]
```

Recognizing patterns and breaking up the input text in this way is the
role of a tokenizer.  It is usually the first step of compilation.

## Your Task

Your task is to write the tokenizer for Wabbit.  The first step is to
define an object that represents a `Token`.  A token has both a type
and a value. For example:

```
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f'Token({self.type}, {self.value})'

    def __eq__(self, other):
        return type(self) == type(other) and vars(self) == vars(other)
```

Next, you need to write a function that turns text strings into a
sequence of tokens.  For example:

```
>>> tokenize('print 123 + xy;')
[ Token('PRINT', print), Token('INTEGER', 123), Token('PLUS', '+'),
  Token('NAME', 'xy'), Token('SEMI', ';')]
>>>
```

You should also write a function that can tokenize an entire file
given a filename.  For example:

```
>>> tokenize_file("program.wb")
[ Token('PRINT', print), Token('INTEGER', 123), Token('PLUS', '+'),
  Token('NAME', 'xy'), Token('SEMI', ';')]
>>>
```

This may be the first part of the project where you can write more
meaningful tests. In fact, this would probably be a pretty good idea.

## The Wabbit Specification

The following specification lists all of the tokens that are used by
Wabbit:

```
Reserved Keywords:
    CONST   : 'const'
    VAR     : 'var'  
    PRINT   : 'print'
    BREAK   : 'break'
    CONTINUE: 'continue'
    IF      : 'if'
    ELSE    : 'else'
    WHILE   : 'while'
    FUNC    : 'func'
    RETURN  : 'return'
    TRUE    : 'true'
    FALSE   : 'false'

Identifiers/Names:
    NAME    : Text starting with a letter or '_', followed by any number
               number of letters, digits, or underscores.
               Examples:  'abc' 'ABC' 'abc123' '_abc' 'a_b_c'

Literals:
    INTEGER :  123
    FLOAT   : 1.234
    CHAR    : 'a'     (a single character - byte)
              '\n'    (newline)

Symbols and Operators:
    PLUS     : '+'
    MINUS    : '-'
    TIMES    : '*'
    DIVIDE   : '/'
    LT       : '<'
    LE       : '<='
    GT       : '>'
    GE       : '>='
    EQ       : '=='
    NE       : '!='
    LAND     : '&&'     (logical and, not bitwise)
    LOR      : '||'     (logical or, not bitwise)
    LNOT     : '!'      (logical not, not bitwise)
    ASSIGN   : '='
    SEMI     : ';'
    LPAREN   : '('
    RPAREN   : ')'
    LBRACE   : '{'
    RBRACE   : '}'
    COMMA    : ','

Comments:  To be ignored
    //             Skips the rest of the line
    /* ... */      Skips a block (no nesting allowed)
```

## Tips

A tokenizer works by scanning the text left-to-right, matching textual
patterns as it goes.

All of the literal symbols and operators can be matched by substring
matching--maybe even just using a lookup table.

More complex tokens such as names and numbers may require more complex
matching involving loops.  For example, to match a number, you would
first check that the current character is a digit. You would then read
all digits that immediately follow until a non-digit character is
encounterted.   You could use regular-expression parsing for this,
but frankly, that's probably overkill.  

Special keywords such as `if`, `else`, `print`, and `while` can be
matched as a special case of names. For example, you would match a
generic name first and then check to see if matches a keyword.  Like
most other programming languages, special keywords in Wabbit can not
be used for other purposes.  For example, you can't name a variable
`if`.

For simplicity, whitespace and comments should be ignored (skipped) by
the tokenizer. It is true that certain kinds of programming tools such
as code formatters might want to know about such things.  However,
that's something that can be added later if you need it.

Don't confuse tokenizing with parsing.  A tokenizer is NOT concerned
with any part of program correctness or correct syntax.  It is merely
taking the input text and breaking it into tokens for later analysis.

## Testing

To test your tokenizer, you might be able to write some 
asserts.

```
assert tokenize("+ - * /") == [ Token('PLUS', '+'), Token('MINUS','-'),
                                Token('TIMES', '*'), Token('DIVIDE', '/') ]
```

The main focus of your testing should be verifying that every possible
token that can appear in a Wabbit program is properly matched.
