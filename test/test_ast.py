from tight.ast import *

import unittest


# Unit tests
class AstTests(unittest.TestCase):
    def test_condition(self):
        v1 = Condition.Value('foo')
        v2 = Condition.Value(3)
        v3 = Condition.Value('bar')
        v4 = Condition.Value(20)
        v5 = Condition.Value('bas')

        c1 = Condition.Relation(v1, v2, Condition.Relation.Op.LT)
        c2 = Condition.Relation(v3, v4, Condition.Relation.Op.GT)

        n1 = Condition.Negation(v5)

        cj1 = Condition.Conjunction(c1, c2, Condition.Conjunction.Op.AND)
        cj2 = Condition.Conjunction(cj1, n1, Condition.Conjunction.Op.OR)

        cond = Condition(root=cj2)

        # Not a great way to test this, so lets just make sure the repr
        # and str are what we expect.
        self.assertEqual(
            repr(cond),
            'Condition(Conjunction(Conjunction(Relation('
            'Value(foo), Value(3), op=<Op.LT: 3>), Relation('
            'Value(bar), Value(20), op=<Op.GT: 1>), op=<Op.AND: 0>), '
            'Negation(Value(bas)), op=<Op.OR: 1>))')
        self.assertEqual(str(cond), '(((foo < 3) && (bar > 20)) || !bas)')

    def test_module(self):
        m = Module()

        m.append_packet(Packet('foo'))
        with self.assertRaises(PacketRedefError):
            m.append_packet(Packet('foo'))

        # Make sure this doesn't raise an exception.
        _ = repr(m)

    def test_optional(self):
        s1 = Scope()
        data = Data(Data.Type.UINT, count=8)
        field1 = Always('foo', data)

        cond = Condition(Condition.Value(1))
        opt = Optional('bar', s1, cond)

        s1.append_field(field1)
        with self.assertRaises(FieldRedefError):
            opt.append_field(Always('foo', data))

        s1.append_field(opt)

        with self.assertRaises(FieldRedefError):
            opt.append_field(Always('bar', data))

        opt.append_field(Always('bas', data))

        # Make sure this doesn't raise an exception.
        _ = repr(opt)

    def test_packet(self):
        p1 = Packet('foo')
        p2 = Packet('bar', parent=p1)

        data = Data(Data.Type.UINT, count=8)
        field1 = Always('foo', data)
        p1.append_field(field1)

        with self.assertRaises(FieldRedefError):
            p2.append_field(field1)

        # Make sure this doesn't raise an exception.
        _ = repr(p2)

    def test_scope(self):
        s1 = Scope()
        data = Data(Data.Type.UINT, count=8)
        field1 = Always('foo', data)
        field2 = Always('foo', data)

        s1.append_field(field1)
        with self.assertRaises(FieldRedefError):
            s1.append_field(field2)

        self.assertEqual(len(s1.fields), 1)

        s2 = Scope(parent=s1)
        with self.assertRaises(FieldRedefError):
            s2.append_field(field2)

        field3 = Always('bar', data)

        s2.append_field(field3)
        with self.assertRaises(FieldRedefError):
            s2.append_field(field3)

        # This _is_ allowed. If we're appending to s1
        # again it means that s2 is closed.
        s1.append_field(field3)
        self.assertEqual(len(s1.fields), 2)

        # Make sure this doesn't raise an exception.
        _ = repr(s2)

    def test_variable(self):
        s1 = Scope()
        data = Data(Data.Type.UINT, count=8)
        field1 = Always('foo', data)
        s1.append_field(field1)

        c1 = Condition(Condition.Value(1))
        c2 = Condition(Condition.Value(2))
        c3 = Condition(Condition.Value(3))

        v1 = Variable.Variant(s1, Variable.Variant.Tag('FOO', 0))
        v2 = Variable.Variant(s1, Variable.Variant.Tag('BAR', 1))
        v3 = Variable.Variant(s1, Variable.Variant.Tag('BAS', 2))
        v4 = Variable.Variant(s1, Variable.Variant.Tag('BAXX', 3))
        v5 = Variable.Variant(s1, Variable.Variant.Tag('BAS', 4))
        v6 = Variable.Variant(s1, Variable.Variant.Tag('QUUX', 2))

        with self.assertRaises(FieldRedefError):
            v1.append_field(Always('foo', data))

        v1.append_field(Always('bar', data))

        var = Variable('bas')
        var.append_variant(v1, c1)
        var.append_variant(v2, c2)
        var.append_variant(v3)

        with self.assertRaises(VariantRedefError):
            var.append_variant(v4)

        with self.assertRaises(VariantRedefError):
            var.append_variant(v4, c2)

        with self.assertRaises(VariantRedefError):
            var.append_variant(v5, c3)

        with self.assertRaises(VariantRedefError):
            var.append_variant(v6, c3)

        # Make sure this doesn't raise an exception.
        _ = repr(var)
