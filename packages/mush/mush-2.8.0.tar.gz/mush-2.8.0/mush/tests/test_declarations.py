from functools import partial
from unittest import TestCase
from mock import Mock
from testfixtures import compare, generator, ShouldRaise
from mush.markers import missing
from mush.declarations import (
    requires, optional, returns,
    returns_mapping, returns_sequence, returns_result_type,
    how, item, attr, nothing,
    extract_declarations
)


def check_extract(obj, expected_rq, expected_rt):
    rq, rt = extract_declarations(obj, None, None)
    compare(rq, expected=expected_rq, strict=True)
    compare(rt, expected=expected_rt, strict=True)


class Type1(object): pass
class Type2(object): pass
class Type3(object): pass
class Type4(object): pass


class TestRequires(TestCase):

    def test_empty(self):
        r = requires()
        compare(repr(r), 'requires()')
        compare(generator(), r)

    def test_types(self):
        r = requires(Type1, Type2, x=Type3, y=Type4)
        compare(repr(r), 'requires(Type1, Type2, x=Type3, y=Type4)')
        compare({
            (None, Type1),
            (None, Type2),
            ('x', Type3),
            ('y', Type4),
        }, set(r))

    def test_strings(self):
        r = requires('1', '2', x='3', y='4')
        compare(repr(r), "requires('1', '2', x='3', y='4')")
        compare({
            (None, '1'),
            (None, '2'),
            ('x', '3'),
            ('y', '4'),
        }, set(r))

    def test_tuple_arg(self):
        with ShouldRaise(TypeError("('1', '2') is not a type or label")):
            requires(('1', '2'))

    def test_tuple_kw(self):
        with ShouldRaise(TypeError("('1', '2') is not a type or label")):
            requires(foo=('1', '2'))

    def test_decorator_paranoid(self):
        @requires(Type1)
        def foo():
            return 'bar'

        compare(set(foo.__mush_requires__), {(None, Type1)})
        compare(foo(), 'bar')


class TestItem(TestCase):

    def test_single(self):
        h = item(Type1, 'foo')
        compare(repr(h), "Type1['foo']")
        compare(h.process(dict(foo=1)), 1)

    def test_multiple(self):
        h = item(Type1, 'foo', 'bar')
        compare(repr(h), "Type1['foo']['bar']")
        compare(h.process(dict(foo=dict(bar=1))), 1)

    def test_missing_obj(self):
        h = item(Type1, 'foo', 'bar')
        with ShouldRaise(TypeError):
            h.process(object())

    def test_missing_key(self):
        h = item(Type1, 'foo', 'bar')
        compare(h.process({}), missing)

    def test_passed_missing(self):
        h = item(Type1, 'foo', 'bar')
        compare(h.process(missing), missing)

    def test_bad_type(self):
        with ShouldRaise(TypeError):
            item([], 'foo', 'bar')


class TestHow(TestCase):

    def test_process_on_base(self):
        compare(how('foo').process('bar'), missing)


class TestAttr(TestCase):

    def test_single(self):
        h = attr(Type1, 'foo')
        compare(repr(h), "Type1.foo")
        m = Mock()
        compare(h.process(m), m.foo)

    def test_multiple(self):
        h = attr(Type1, 'foo', 'bar')
        compare(repr(h), "Type1.foo.bar")
        m = Mock()
        compare(h.process(m), m.foo.bar)

    def test_missing(self):
        h = attr(Type1, 'foo', 'bar')
        compare(h.process(object()), missing)

    def test_passed_missing(self):
        h = attr(Type1, 'foo', 'bar')
        compare(h.process(missing), missing)


class TestOptional(TestCase):

    def test_type(self):
        compare(repr(optional(Type1)), "optional(Type1)")

    def test_string(self):
        compare(repr(optional('1')), "optional('1')")

    def test_present(self):
        compare(optional(Type1).process(1), 1)

    def test_missing(self):
        compare(optional(Type1).process(missing), nothing)


class TestReturns(TestCase):

    def test_type(self):
        r = returns(Type1)
        compare(repr(r), 'returns(Type1)')
        compare(dict(r.process('foo')), {Type1: 'foo'})

    def test_string(self):
        r = returns('bar')
        compare(repr(r), "returns('bar')")
        compare(dict(r.process('foo')), {'bar': 'foo'})

    def test_sequence(self):
        r = returns(Type1, 'bar')
        compare(repr(r), "returns(Type1, 'bar')")
        compare(dict(r.process(('foo', 'baz'))),
                {Type1: 'foo', 'bar': 'baz'})

    def test_decorator(self):
        @returns(Type1)
        def foo():
            return 'foo'
        r = foo.__mush_returns__
        compare(repr(r), 'returns(Type1)')
        compare(dict(r.process(foo())), {Type1: 'foo'})

    def test_bad_type(self):
        with ShouldRaise(TypeError(
            '[] is not a type or label'
        )):
            @returns([])
            def foo(): pass

class TestReturnsMapping(TestCase):

    def test_it(self):
        @returns_mapping()
        def foo():
            return {Type1: 'foo', 'bar': 'baz'}
        r = foo.__mush_returns__
        compare(repr(r), 'returns_mapping()')
        compare(dict(r.process(foo())),
                {Type1: 'foo', 'bar': 'baz'})


class TestReturnsSequence(TestCase):

    def test_it(self):
        t1 = Type1()
        t2 = Type2()
        @returns_sequence()
        def foo():
            return t1, t2
        r = foo.__mush_returns__
        compare(repr(r), 'returns_sequence()')
        compare(dict(r.process(foo())),
                {Type1: t1, Type2: t2})


class TestReturnsResultType(TestCase):

    def test_basic(self):
        @returns_result_type()
        def foo():
            return 'foo'
        r = foo.__mush_returns__
        compare(repr(r), 'returns_result_type()')
        compare(dict(r.process(foo())), {str: 'foo'})

    def test_old_style_class(self):
        class Type: pass
        obj = Type()
        r = returns_result_type()
        compare(dict(r.process(obj)), {Type: obj})

    def test_returns_nothing(self):
        def foo():
            pass
        r = returns_result_type()
        compare(dict(r.process(foo())), {})


class TestExtractDeclarations(object):

    def test_default_requirements_for_function(self):
        def foo(a, b=None): pass
        check_extract(foo,
                      expected_rq=requires('a', optional('b')),
                      expected_rt=None)

    def test_default_requirements_for_class(self):
        class MyClass(object):
            def __init__(self, a, b=None): pass
        check_extract(MyClass,
                      expected_rq=requires('a', optional('b')),
                      expected_rt=None)

    def test_extract_from_partial(self):
        def foo(x, y, z, a=None): pass
        p = partial(foo, 1, y=2)
        check_extract(
            p,
            expected_rq=requires(z='z', a=optional('a'), y=optional('y')),
            expected_rt=None
        )

    def test_extract_from_partial_default_not_in_partial(self):
        def foo(a=None): pass
        p = partial(foo)
        check_extract(
            p,
            expected_rq=requires(optional('a')),
            expected_rt=None
        )

    def test_extract_from_partial_default_in_partial_arg(self):
        def foo(a=None): pass
        p = partial(foo, 1)
        check_extract(
            p,
            # since a is already bound by the partial:
            expected_rq=None,
            expected_rt=None
        )

    def test_extract_from_partial_default_in_partial_kw(self):
        def foo(a=None): pass
        p = partial(foo, a=1)
        check_extract(
            p,
            expected_rq=requires(a=optional('a')),
            expected_rt=None
        )

    def test_extract_from_partial_required_in_partial_arg(self):
        def foo(a): pass
        p = partial(foo, 1)
        check_extract(
            p,
            # since a is already bound by the partial:
            expected_rq=None,
            expected_rt=None
        )

    def test_extract_from_partial_required_in_partial_kw(self):
        def foo(a): pass
        p = partial(foo, a=1)
        check_extract(
            p,
            expected_rq=requires(a=optional('a')),
            expected_rt=None
        )

    def test_extract_from_partial_plus_one_default_not_in_partial(self):
        def foo(b, a=None): pass
        p = partial(foo)
        check_extract(
            p,
            expected_rq=requires('b', optional('a')),
            expected_rt=None
        )

    def test_extract_from_partial_plus_one_required_in_partial_arg(self):
        def foo(b, a): pass
        p = partial(foo, 1)
        check_extract(
            p,
            # since b is already bound:
            expected_rq=requires('a'),
            expected_rt=None
        )

    def test_extract_from_partial_plus_one_required_in_partial_kw(self):
        def foo(b, a): pass
        p = partial(foo, a=1)
        check_extract(
            p,
            expected_rq=requires('b', a=optional('a')),
            expected_rt=None
        )
