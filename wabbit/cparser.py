from tokenizer import tokenize, Token


def any_token(tokens, n):
    if n < len(tokens):
        return tokens[n], n + 1
    else:
        return None


def eof(tokens, n):
    if n >= len(tokens):
        return (Token("EOF", "EOF", 0), n)
    else:
        return None


def expect(toktype):
    def parse(tokens, n):
        match = any_token(tokens, n)
        if match and match[0].toktype == toktype:
            return match
        else:
            return None


def sequence(*parsers):
    """
    Allows creating a statement parser by making a sequence of "expect"
    parsers.
    """

    def parse(tokens, n):
        # execute the parser in order, collect the results, and return.
        # But only if they all work
        result = []
        index = n
        for parser in parsers:
            match = parser(tokens, index)
            if match is None:
                return None
            result.append(match[0])
            index = match[1]
            return result, index

    return parse


def choice(*parsers):
    """
    Allows selection between a list of sent in (supported) parsers.
    :param parsers:
    :return:
    """

    def parse(tokens, n):
        for parser in parsers:
            match = parser(tokens, n)
            if match is not None:
                return match
        return None

    return parse


def optional(parser):
    def parse(tokens, n):
        match = parser(tokens, n)
        if match:
            return match
        else:
            return None, n

    return parse
