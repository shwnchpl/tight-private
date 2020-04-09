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

        for p_ctx in ctx.packet():
            p = self.visit(p_ctx)
            self._packets[p.ident] = p
            try:
                mod.append_packet(p)
            except model.PacketRedefError:
                ctx.parser.notifyErrorListeners(
                    'Packet redefinition error: {}'.format(p.ident),
                    p_ctx.IDENT(0).symbol)

        return mod

    def visitPacket(self, ctx: CstParser.PacketContext) -> model.Packet:
        parent = None
        cond = None

        parent_ident = ctx.IDENT(1)
        if parent_ident is not None:
            try:
                parent = self._packets[str(parent_ident)]
            except KeyError:
                ctx.parser.notifyErrorListeners(
                    'No such packet: {}'.format(parent_ident),
                    parent_ident.symbol)
            else:
                cond_ctx = ctx.cond_exp()
                if cond_ctx is not None:
                    cond = self.visit(cond_ctx)

        p = model.Packet(str(ctx.IDENT(0)), parent=parent, cond=cond)

        # Set current scope to packet scope.
        old_scope = self._scope
        self._scope = p.scope

        # Visit each statement in the packet, adding to packet.
        for stmt in ctx.def_block().statement():
            f = self.visit(stmt)
            if f is not None:
                try:
                    p.append_field(f)
                except model.FieldRedefError:
                    bad_tok = None
                    ident_stmt = (
                        stmt.optional_statement() or
                        stmt.always_statement() or
                        stmt.empty_statement())
                    if ident_stmt is not None:
                        bad_tok = ident_stmt.IDENT().symbol
                    else:
                        empty_stmt = stmt.empty_statement()
                        if empty_stmt is not None:
                            bad_tok = empty_stmt.SEMI().symbol

                    ctx.parser.notifyErrorListeners(
                        'Field redefinition error: {}'.format(f.ident),
                        bad_tok)

        # Restore old scope.
        self._scope = old_scope

        return p

    def visitCond_exp(self, ctx: CstParser.Cond_expContext):
        pass

    def visitCond_relation(self, ctx: CstParser.Cond_relationContext):
        pass

    def visitCond_conjunction(self, ctx: CstParser.Cond_conjunctionContext):
        pass

    def visit_statement(self, ctx: CstParser.StatementContext):
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
