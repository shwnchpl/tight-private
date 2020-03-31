###############################################################################
#  __main__.py - Tight Buffer compiler entry point.
#
#  Copyright 2020 Shawn M. Chapla
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
###############################################################################


import antlr4
from ._gen.TightLexer import TightLexer
from ._gen.TightParser import TightParser


def main():
    test1 = '''        &foo; ; &  fooo;
    5 bytes; 10 bytes be;
    &foo bits;
    10;'''

    test2 = '!(5 < 6) || 4'
    test3 = '[ sint : 5 bytes be ]; [uint : 5 bytes: &foo];'
    test4 = '[sint::5];'

    test5 = '''
    packet P2_generic : P2(&subtype == 3) {
        always timestamp    [ uint: 4 bytes be ];
        always version      [ uint: 2 bits ];
        always _padding     [ _ : 6 bits]; // pad to align to next byte

        variable speed {
            case(&version < 1) | v1: 0 | {
                always speed    [ uint : 2 bytes be ];
            }
            case(&version < 2) | v2: 1 | {
                always speed    [ uint : 3 bytes be ];
            }
            otherwise | cur: 2 | {
                always speed    [ uint : 4 bytes be ];
            }
        }

        optional metadata when(&version > 3) {
            always distance [ uint : 4 bytes be ];
            always end_time [ uint : 4 bytes be ];
        }
    }'''

    inp = antlr4.InputStream(test5)
    lexer = TightLexer(inp)

    stream = antlr4.CommonTokenStream(lexer)
    parser = TightParser(stream)
    tree = parser.module()

    print(tree.toStringTree(TightParser.ruleNames))


if __name__ == '__main__':
    main()
