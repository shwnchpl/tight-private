###############################################################################
#  model.py - Tight Buffer abstract syntax tree builder.
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


from . import AstRoot, model
from ..cst import CstParser, CstRoot, CstVisitor


class AstBuilder(CstVisitor):
    def __init__(self):
        super().__init__()
        self._packets = {}
        self._scope = None

    def visitModule(self, ctx: CstParser.ModuleContext) -> AstRoot:
        mod = model.Module()

        # Visit each packet, building it.

        # Add to packets dict and module.

        return mod

    def visitPacket(self, ctx: CstParser.PacketContext) -> model.Packet:
        # Create packet. We'll run into an issue here if our parent
        # isn't around.

        # Set current scope to packet scope.
        # old_scope = self._scope

        # Visit each statement in the packet, adding to packet.

        # Restore old scope.
        # self._scope = old_scope

        pass

    def visitCond_exp(self, ctx: CstParser.Cond_expContext):
        pass

    def visitCond_relation(self, ctx: CstParser.Cond_relationContext):
        pass

    def visitCond_conjunction(self, ctx: CstParser.Cond_conjunctionContext):
        pass

    def visitDef_block(self, ctx: CstParser.Def_blockContext):
        pass

    def visitAlways_statement(self, ctx: CstParser.Always_statementContext):
        pass

    def visitOptional_statement(
            self,
            ctx: CstParser.Optional_statementContext):
        pass

    def visitVariable_statement(
            self,
            ctx: CstParser.Variable_statementContext):
        pass

    def visitCase_block(self, ctx: CstParser.Case_blockContext):
        pass

    def visitCase_statement(self, ctx: CstParser.Case_statementContext):
        pass

    def visitCase_tag(self, ctx: CstParser.Case_tagContext):
        pass

    def visitOtherwise_statement(
            self,
            ctx: CstParser.Otherwise_statementContext):
        pass

    def visitField_desc(self, ctx: CstParser.Field_descContext):
        pass

    def visitScalar_type(self, ctx: CstParser.Scalar_typeContext):
        pass

    def visitCount(self, ctx: CstParser.CountContext):
        pass

    def visitValue(self, ctx: CstParser.ValueContext):
        pass

    def visitResolvable(self, ctx: CstParser.ResolvableContext):
        pass

    def visitUnits(self, ctx: CstParser.UnitsContext):
        pass


def build_ast(tree: CstRoot) -> AstRoot:
    builder = AstBuilder()
    return builder.visit(tree)
