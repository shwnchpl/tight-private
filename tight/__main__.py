#!/usr/bin/env python3

import antlr4
from ._gen.TightLexer import TightLexer
from ._gen.TightParser import TightParser


def main():
    test1 = '''        &foo; ; &  fooo;
    5 bytes; 10 bytes be;
    &foo bits;
    10;'''

    test2 = '!(5 < 6) || 4';

    inp = antlr4.InputStream(test2)
    lexer = TightLexer(inp)

    stream = antlr4.CommonTokenStream(lexer)
    parser = TightParser(stream)
    tree = parser.module()

    print(tree.toStringTree(TightParser.ruleNames))


if __name__ == '__main__':
    main()
