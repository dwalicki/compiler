# tokenizer.py
#
# I encourage you to follow along with some coding to follow.  I'll paste this in the chat.
# This is a stand-alone file.  No dependencies on prior work.

code = '''var x int = 1;
var fact int = 1;
var result float = 15.553;
/* This is a while loop */
while x < 11 {
    fact = fact * x;
    x = x + 1;
    print fact;
}
'''


class Token:
    """A single character in a programming language."""

    def __init__(self, toktype, value, lineno):
        """Initialize a Token."""
        self.toktype = toktype
        self.value = value
        self.lineno = lineno

    def __repr__(self):
        """Return a representation of the token."""
        return f'Token({self.toktype}, {self.value}, {self.lineno})'


# Example:
tok1 = Token(toktype='INTEGER', value='1234', lineno=5)
tok2 = Token(toktype='NAME', value='fact', lineno=6)
tok3 = Token(toktype='PLUS', value='+', lineno=14)


# Make a table of valid literals
literals = {
    '=': 'ASSIGN',
    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'MULTIPLY',
    '/': 'DIVIDE',
    '<': 'LT',
    '>': 'GT',
    ';': 'SEMI',
    '{': 'LBRACE',
    '}': 'RBRACE',
    # Add more characters...
}

keywords = {
    'if': 'IF',
    'while': 'WHILE',
    'func': 'FUNC',
    'var': 'VAR'
}


def tokenize(source) -> list[Token]:
    """Parse source string into list of tokens."""
    tokens = []
    n = 0
    lineno = 1
    while n < len(source):
        if source[n] == '\n':
            lineno += 1
            n += 1
            continue

        elif source[n].isspace():
            n += 1
            continue

        # Recognize name
        if source[n].isalpha():
            start = n
            while n < len(source) and source[n].isalpha():
                n += 1

            name = source[start:n]
            if name in keywords:
                tokens.append(Token(keywords[name], name, lineno))
            else:
                tokens.append(Token('NAME', source[start:n], lineno))

        if source[n].isdigit():
            start = n
            while n < len(source) and source[n].isdigit():
                n += 1
            # Floats
            # TODO check if the float is in range
            if source[n] == '.':
                n += 1
                while n < len(source) and source[n].isdigit():
                    n += 1
                tokens.append(Token('FLOAT', source[start:n], lineno))
                continue
            tokens.append(Token('INTEGER', source[start:n], lineno))

        match source[n:n+2]:
            case '==':
                tokens.append(Token('EQ', '==', lineno))
                n += 2
            case '/*':
                # block comment
                start = n
                while n < len(source):
                    if source[n:n+2] == '*/':
                        break
                    n+= 1
                n += 2
                tokens.append(Token('COMMENT', source[start:n], lineno))
        if source[n] in literals:
            tokens.append(Token(literals[source[n]], source[n], lineno))
            n += 1
        else:
            # Unrecognized input character
            tokens.append(Token('ILLEGAL', source[n], lineno))
            n += 1

    return tokens


if __name__ == '__main__':
    tokens = tokenize(code)
    print(tokens)
