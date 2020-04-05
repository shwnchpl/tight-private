###############################################################################
#  __init__.py - Tight Buffer concrete syntax tree module init file.
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


from .._gen.TightLexer import TightLexer as CstLexer
from .._gen.TightParser import TightParser as CstParser
from .._gen.TightVisitor import TightVisitor as CstVisitor


CstRoot = CstParser.ModuleContext
