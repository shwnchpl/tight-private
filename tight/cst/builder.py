###############################################################################
#  builder.py - Tight Buffer concrete syntax tree builder.
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


from antlr4 import CommonTokenStream, InputStream
from . import CstLexer, CstParser, CstRoot


def build_cst(src: str) -> CstRoot:
    in_stream = InputStream(src)
    lexer = CstLexer(in_stream)
    tok_stream = CommonTokenStream(lexer)
    parser = CstParser(tok_stream)
    return parser.module()
