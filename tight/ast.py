from collections import OrderedDict
from enum import Enum
from typing import Generator, Union


class PacketRedefError(Exception):
    pass


class FieldRedefError(Exception):
    pass


class VariantRedefError(Exception):
    pass


class Module:
    def __init__(self) -> None:
        self._packets = OrderedDict()

    def __repr__(self) -> str:
        return 'Module({!r})'.format(self._packets)

    def append_packet(self, p: 'Packet') -> None:
        if p in self._packets:
            raise PacketRedefError
        self._packets[p] = None


class Packet:
    def __init__(self, ident: str, parent: 'Packet' = None) -> None:
        self.ident = ident
        self.parent = parent
        self.children = OrderedDict()

        if parent is not None:
            self.scope = Scope(parent=parent.scope)
        else:
            self.scope = Scope()

    def __eq__(self, other: 'Packet') -> bool:
        return self.ident == other.ident

    def __hash__(self) -> int:
        return hash(self.ident)

    def __repr__(self) -> str:
        return 'Packet(\'{}\', parent={}, {!r})'.format(
            self.ident,
            self.parent.ident if self.parent is not None else None,
            self.scope)

    def append_field(self, f: 'Field') -> None:
        self.scope.append_field(f)

    def append_child(self, p: 'Packet', cond: 'Condition' = None) -> None:
        self.children[p] = cond


class Scope:
    ScopeGenerator = Generator['Scope', None, None]

    def __init__(self, parent: 'Scope' = None) -> None:
        self._parent = parent
        self.fields = OrderedDict()

    def __repr__(self) -> str:
        return 'Scope({!r})'.format(self.fields)

    def _lineage(self) -> ScopeGenerator:
        inst = self
        while inst is not None:
            yield inst
            inst = inst._parent

    def append_field(self, f: 'Field') -> None:
        for p in self._lineage():
            if f in p.fields:
                raise FieldRedefError
        self.fields[f] = None


class Condition:
    class Expr:
        pass

    class Value(Expr):
        def __init__(self, val: Union[int, str]) -> None:
            self.val = val

        def __repr__(self) -> str:
            return 'Value({})'.format(self.val)

        def __str__(self) -> str:
            return str(self.val)

    class Negation(Expr):
        def __init__(self, expr: 'Expr') -> None:
            self.expr = expr

        def __repr__(self) -> str:
            return 'Negation({!r})'.format(self.expr)

        def __str__(self) -> str:
            return '!{}'.format(self.expr)

    class Relation(Expr):
        class Op(Enum):
            EQ = 0
            GT = 1
            GTE = 2
            LT = 3
            LTE = 4
            NOT_EQ = 5

        def __init__(self, left: 'Expr', right: 'Expr', op: Op) -> None:
            self.left = left
            self.right = right
            self.op = op

        def __repr__(self) -> str:
            return 'Relation({!r}, {!r}, op={!r})'.format(
                self.left,
                self.right,
                self.op)

        def __str__(self) -> str:
            op_to_str = {
                Condition.Relation.Op.EQ: '==',
                Condition.Relation.Op.GT: '>',
                Condition.Relation.Op.GTE: '>=',
                Condition.Relation.Op.LT: '<',
                Condition.Relation.Op.LTE: '<=',
                Condition.Relation.Op.NOT_EQ: '!='
            }

            return '({} {} {})'.format(
                self.left, op_to_str[self.op], self.right)

    class Conjunction(Expr):
        class Op(Enum):
            AND = 0
            OR = 1

        def __init__(
                self, left: 'Expr', right: 'Expr', op: Op) -> None:
            self.left = left
            self.right = right
            self.op = op

        def __repr__(self) -> str:
            return 'Conjunction({!r}, {!r}, op={!r})'.format(
                self.left,
                self.right,
                self.op)

        def __str__(self) -> str:
            op_to_str = {
                Condition.Conjunction.Op.AND: '&&',
                Condition.Conjunction.Op.OR: '||',
            }

            return '({} {} {})'.format(
                self.left, op_to_str[self.op], self.right)

    def __init__(self, root: Expr) -> None:
        self.root = root

    def __repr__(self) -> str:
        return 'Condition({!r})'.format(self.root)

    def __str__(self) -> str:
        return str(self.root)


class Field:
    def __init__(self, ident: str) -> None:
        self.ident = ident

    def __eq__(self, other: 'Field') -> bool:
        return self.ident == other.ident

    def __hash__(self) -> int:
        return hash(self.ident)

    def __repr__(self) -> str:
        return 'Field(\'{}\')'.format(self.ident)


class Always(Field):
    def __init__(self, ident: str, data: 'Data') -> None:
        super().__init__(ident)
        self.data = data

    def __repr__(self) -> str:
        return 'Always(\'{}\', {!r})'.format(self.ident, self.data)


class Optional(Field):
    def __init__(self, ident: str, parent: Scope, cond: Condition) -> None:
        super().__init__(ident)
        self.scope = Scope(parent=parent)
        self.cond = cond

    def __repr__(self) -> str:
        return 'Optional(\'{}\', {!r}, {!r})'.format(
            self.ident,
            self.cond,
            self.scope)

    def append_field(self, f: Field) -> None:
        self.scope.append_field(f)


class Variable(Field):
    class Variant:
        class Tag:
            def __init__(self, label: str, val: int) -> None:
                self.label = label
                self.val = val

            def __repr__(self) -> str:
                return 'Tag({}, {})'.format(self.label, self.val)

        def __init__(self, parent: Scope, tag: Tag) -> None:
            self.scope = Scope(parent=parent)
            self.tag = tag

        def __repr__(self) -> str:
            return 'Variant({!r}, {!r})'.format(self.tag, self.scope)

        def append_field(self, f: Field) -> None:
            self.scope.append_field(f)

    def __init__(self, ident: str) -> None:
        super().__init__(ident)
        self._variants = OrderedDict()
        self._labels = set()
        self._vals = set()

    def __repr__(self) -> str:
        return 'Variable(\'{}\', {!r})'.format(self.ident, self._variants)

    def append_variant(self, variant: Variant, cond: Condition = None) -> None:
        if cond is None and None in self._variants:
            # Should never happen.
            raise VariantRedefError('multiple otherwise variants')

        if cond in self._variants:
            # Should never happen.
            raise VariantRedefError('variant redefined')

        if variant.tag.label in self._labels:
            raise VariantRedefError(
                'tag redefined - {}'.format(variant.tag.label))

        if variant.tag.val in self._vals:
            raise VariantRedefError('val reused - {}'.format(variant.tag.val))

        self._labels.add(variant.tag.label)
        self._vals.add(variant.tag.val)
        self._variants[cond] = variant


class Data:
    class Type(Enum):
        IGNORE = 0
        SINT = 1
        UINT = 2

    class Unit(Enum):
        BITS = 0
        BYTES = 1

    class Width:
        def __init__(self, count: int, unit: 'Unit') -> None:
            self.count = count
            self.unit = unit

        def __repr__(self) -> str:
            return 'Width({}, {!r})'.format(self.count, self.unit)

    def __init__(
            self, type_: Type, *, width: Width = None, count: int = 1) -> None:
        self.type_ = type_
        self.count = count

        if width is None:
            self.width = Data.Width(1, Data.Unit.BYTES)
        else:
            self.width = width

    def __repr__(self) -> str:
        return 'Data({!r}, {!r}, {})'.format(
            self.type_,
            self.width,
            self.count)
