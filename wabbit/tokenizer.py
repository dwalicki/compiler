# tokenizer.py


class Token:
    """A single character in a programming language."""

    def __init__(self, toktype, value, lineno, index):
        """Initialize a Token."""
        self.toktype = toktype
        self.value = value
        self.lineno = lineno
        self.index = index

    def __repr__(self):
        """Return a representation of the token."""
        return f"Token({self.toktype}, {self.value}, {self.lineno}, {self.index})"

    def __eq__(self, other):
        return type(self) == type(other) and vars(self) == vars(other)


# Make a table of valid literals
literals = {
    "=": "ASSIGN",
    "==": "EQ",
    "!=": "NE",
    "+": "PLUS",
    "-": "MINUS",
    "*": "MULTIPLY",
    "/": "DIVIDE",
    "<": "LT",
    ">": "GT",
    "<=": "LE",
    ">=": "GE",
    "&&": "LOGAND",
    "||": "LOGOR",
    "!": "LOGNOT",
    ";": "SEMI",
    ",": "COMMA",
    "(": "LPAREN",
    ")": "RPAREN",
    "{": "LBRACE",
    "}": "RBRACE",
}

keywords = {
    "if": "IF",
    "while": "WHILE",
    "func": "FUNC",
    "var": "VAR",
    "break": "BREAK",
    "const": "CONST",
    "continue": "CONTINUE",
    "else": "ELSE",
    "print": "PRINT",
    "return": "RETURN",
    "true": "TRUE",
    "false": "FALSE",
}


def tokenize_file(filename: str) -> list[Token]:
    with open(filename) as file:
        source = file.read()
        return tokenize(source)


def tokenize(source) -> list[Token]:
    """Parse source string into list of tokens."""
    tokens = []
    n = 0
    lineno = 1
    while n < len(source):
        if source[n] == "\n":
            lineno += 1
            n += 1
            continue

        elif source[n].isspace():
            n += 1
            continue

        # Comments before anything else besides spaces
        elif source[n : n + 2] == "/*":
            start = n
            end = source.find("*/", start)
            if end > 0:
                n = end + 2
                lineno += source[start:end].count("\n")
                continue
            else:
                tokens.append(Token("UNTERMCOMMENT", source[start:], lineno, start))
        elif source[n : n + 2] == "//":
            end = source.find("\n", n)
            if end > 0:
                n = end
            else:
                # corner case of // on last line with no newline terminator
                break
        # Recognize name
        elif source[n].isalpha() or source[n] == "_":
            start = n
            while n < len(source) and (source[n].isalpha() or source[n] == "_"):
                n += 1
            name = source[start:n]
            if name in keywords:
                tokens.append(Token(keywords[name], name, lineno, start))
            else:
                tokens.append(Token("NAME", source[start:n], lineno, start))

        # Recognize number
        elif source[n].isdigit():
            start = n
            while n < len(source) and source[n].isdigit():
                n += 1
            # Floats
            # TODO check if the float is in range
            if n < len(source) and source[n] == ".":
                n += 1
                while n < len(source) and source[n].isdigit():
                    n += 1
                tokens.append(Token("FLOAT", source[start:n], lineno, start))
            else:
                tokens.append(Token("INTEGER", source[start:n], lineno, start))

        # A bare float or just a period
        elif source[n] == ".":
            start = n
            n += 1
            while n < len(source) and source[n].isdigit():
                n += 1
            value = source[start:n]
            if value == ".":
                tokens.append(Token("DOT", value, lineno, start))
            else:
                tokens.append(Token("FLOAT", value, lineno, start))

        elif source[n : n + 2] in literals:
            tokens.append(
                Token(literals[source[n : n + 2]], source[n : n + 2], lineno, n)
            )
            n += 2
        elif source[n] in literals:
            tokens.append(Token(literals[source[n]], source[n], lineno, n))
            n += 1
        else:
            # Unrecognized input character
            tokens.append(Token("ILLEGAL", source[n], lineno, n))
            n += 1

    return tokens


def test_tokens():
    def extract(toks):
        return [(t.toktype, t.value) for t in toks]

    mytokens = extract(tokenize("+ - * /"))

    assert mytokens == [
        ("PLUS", "+"),
        ("MINUS", "-"),
        ("MULTIPLY", "*"),
        ("DIVIDE", "/"),
    ]

    assert (
        tokenize(
            """/* a multiline comment
    on multiple lines is ignored */"""
        )
        == []
    )
    assert tokenize("// a comment is ignored") == []

    assert extract(tokenize("= == != + - * / < > <= >= && || ! ; , ( ) { }")) == [
        ("ASSIGN", "="),
        ("EQ", "=="),
        ("NE", "!="),
        ("PLUS", "+"),
        ("MINUS", "-"),
        ("MULTIPLY", "*"),
        ("DIVIDE", "/"),
        ("LT", "<"),
        ("GT", ">"),
        ("LE", "<="),
        ("GE", ">="),
        ("LOGAND", "&&"),
        ("LOGOR", "||"),
        ("LOGNOT", "!"),
        ("SEMI", ";"),
        ("COMMA", ","),
        ("LPAREN", "("),
        ("RPAREN", ")"),
        ("LBRACE", "{"),
        ("RBRACE", "}"),
    ]

    assert extract(
        tokenize("if while func var break const continue else print return true false")
    ) == [
        ("IF", "if"),
        ("WHILE", "while"),
        ("FUNC", "func"),
        ("VAR", "var"),
        ("BREAK", "break"),
        ("CONST", "const"),
        ("CONTINUE", "continue"),
        ("ELSE", "else"),
        ("PRINT", "print"),
        ("RETURN", "return"),
        ("TRUE", "true"),
        ("FALSE", "false"),
    ]


test_tokens()

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        raise SystemExit("Usage: python tokenizer.py filename")
    for tok in tokenize_file(sys.argv[1]):
        print(tok)
