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
from typing import Union


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
        old_scope = self._scope

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
                    # Set scope to parent scope for the purposes of
                    # resolving this condition expression.
                    self._scope = parent.scope
                    cond = model.Condition(self.visit(cond_ctx))

        p = model.Packet(str(ctx.IDENT(0)), parent=parent, cond=cond)

        # Set current scope to packet scope.
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

    def visitCond_exp(
            self,
            ctx: CstParser.Cond_expContext) -> model.Condition.Expr:
        val = ctx.value()
        exp0 = ctx.cond_exp(0)
        exp1 = ctx.cond_exp(1)
        cond_rel = ctx.cond_relation()
        cond_conj = ctx.cond_conjunction()

        if cond_conj is not None:
            return model.Condition.Conjunction(
                self.visit(exp0),
                self.visit(exp1),
                op=self.visit(cond_conj))
        elif cond_rel is not None:
            return model.Condition.Relation(
                self.visit(exp0),
                self.visit(exp1),
                op=self.visit(cond_rel))
        elif exp0 is not None:
            res = self.visit(exp0)
            if ctx.LOGIC_NOT() is not None:
                return model.Condition.Negation(res)
            else:
                return res
        elif val is not None:
            return model.Condition.Value(
                self.visit(val))

        # TODO: [SHAWN] raise some kind of error.
        return None

    def visitCond_relation(
            self,
            ctx: CstParser.Cond_relationContext
            ) -> model.Condition.Relation.Op:
        if ctx.EQ() is not None:
            return model.Condition.Relation.Op.EQ
        elif ctx.GT() is not None:
            return model.Condition.Relation.Op.GT
        elif ctx.GTE() is not None:
            return model.Condition.Relation.Op.GTE
        elif ctx.LT() is not None:
            return model.Condition.Relation.Op.LT
        elif ctx.LTE() is not None:
            return model.Condition.Relation.Op.LTE
        elif ctx.NOT_EQ() is not None:
            return model.Condition.Relation.Op.NOT_EQ

        # TODO: [SHAWN] raise some kind of error.
        return None

    def visitCond_conjunction(
            self,
            ctx: CstParser.Cond_conjunctionContext
            ) -> model.Condition.Conjunction.Op:
        if ctx.LOGIC_AND() is not None:
            return Condition.Conjunction.Op.AND
        elif ctx.LOGIC_OR() is not None:
            return Condition.Conjunction.Op.OR

        # TODO: [SHAWN] raise some kind of error.
        return None

    def visitAlways_statement(
            self,
            ctx: CstParser.Always_statementContext
            ) -> model.Always:
        ident = ctx.IDENT().getText()
        data = self.visit(ctx.field_desc())

        return model.Always(ident, data)

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

    def visitCase_tag(self, ctx: CstParser.Case_tagContext):
        pass

    def visitOtherwise_statement(
            self,
            ctx: CstParser.Otherwise_statementContext):
        pass

    def visitField_desc(
            self,
            ctx: CstParser.Field_descContext
            ) -> model.Data:
        st = self.visit(ctx.scalar_type())

        count = None
        val = None

        count_ctx = ctx.count()
        val_ctx = ctx.value()

        if count_ctx is not None:
            count = self.visit(ctx.count())

        if val_ctx is not None:
            val = self.visit(ctx.value())

        if count is None and val is None:
            # FIXME: Handle this error correctly.
            raise RuntimeError('change me')

        if val is not None:
            return model.Data(st, width=count)

        return model.Data(st, width=count, count=val)

    def visitScalar_type(
            self,
            ctx: CstParser.Scalar_typeContext
            ) -> model.Data.Type:
        if ctx.IGNORE() is not None:
            return model.Data.Type.IGNORE
        elif ctx.SINT() is not None:
            return model.Data.Type.SINT
        elif ctx.UINT() is not None:
            return model.Data.Type.UINT

        # TODO: Raise some kind of error.
        return None

    def visitCount(self, ctx: CstParser.CountContext) -> model.Data.Width:
        val = self.visit(ctx.value())
        units = self.visit(ctx.units())

        return model.Data.Width(val, units)

    def visitValue(self, ctx: CstParser.ValueContext) -> model.ValueT:
        lit = ctx.LITERAL()
        r = ctx.resolvable()

        if lit is not None:
            return int(lit.getText())

        return self.visit(r)

    def visitResolvable(
            self,
            ctx: CstParser.ResolvableContext
            ) -> model.ValueT:
        if ctx is not None and self._scope is not None:
            ident = ctx.IDENT().getText()
            for s in self._scope.lineage():
                if (ident in s.fields and
                        isinstance(s.fields[ident], model.Always)):
                    return ident

        # TODO: [SHAWN] raise some kind of error.
        return None

    def visitUnits(self, ctx: CstParser.UnitsContext) -> model.Data.Unit:
        if ctx.BITS() is not None:
            return model.Data.Unit.BITS
        elif ctx.BYTES() is not None:
            if ctx.LE() is not None:
                return model.Data.Unit.BYTES_LE
            else:
                return model.Data.Unit.BYTES_BE

        # TODO: [SHAWN] raise some kind of error.
        return None


def build_ast(tree: CstRoot) -> AstRoot:
    builder = AstBuilder()
    return builder.visit(tree)
