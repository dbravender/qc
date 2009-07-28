import random
import types
import os
from functools import partial

__all__ = ['integers', 'lists', 'unicodes', 'characters', 'forall']

def evaluate(lazy_value):
    while hasattr(lazy_value, '__call__'):
        lazy_value = lazy_value()
    return lazy_value

def integers(low=0, high=100):
    return lambda: random.randint(low, high)

def lists(items=integers, size=(0, 100)):
    return lambda: [evaluate(items) \
                    for _ in xrange(random.randint(size[0], size[1]))]

def dicts(items=integers, values=integers, size=(0, 100)):
    def fun():
        x = {}
        for _ in xrange(random.randint(size[0], size[1])):
            item = evaluate(items)
            while item in x:
                item = evaluate(items)
            x.update({evaluate(items): evaluate(values)})
        return x
    return fun

def unicodes(size=(0, 100), minunicode=0, maxunicode=255):
    return lambda: u''.join(unichr(random.randint(minunicode, maxunicode)) \
                            for _ in xrange(random.randint(size[0], size[1])))

characters = partial(unicodes, size=(1, 1))

def forall(tries=100, **kwargs):
    def wrap(f):
        def wrapped():
            for _ in xrange(tries):
                random_kwargs = (dict((name, evaluate(lazy_value)) \
                                 for (name, lazy_value) in kwargs.iteritems()))
                if forall.verbose or os.environ.has_key('QC_VERBOSE'):
                    from pprint import pprint
                    pprint(random_kwargs)
                f(**random_kwargs)
        wrapped.__name__ = f.__name__
        return wrapped
    return wrap
forall.verbose = False # if enabled will print out the random test cases

@forall(tries=10, i=integers)
def test_integers(i):
    assert type(i) == int
    assert i >= 0 and i <= 100

@forall(tries=10, l=lists(items=integers))
def test_a_int_list(l):
    assert type(l) == list

@forall(tries=10, ul=lists(items=unicodes))
def test_unicodes_list(ul):
    assert type(ul) == list
    if len(ul):
        assert type(ul[0]) == unicode

@forall(tries=10, l=lists(items=integers, size=(10, 50)))
def test_lists_size(l):
    assert len(l) <= 50 and len(l) >= 10

@forall(tries=10, u=unicodes)
def test_unicodes(u):
    assert type(u) == unicode

@forall(tries=10, u=unicodes(size=(1,1)))
def test_unicodes_size(u):
    assert len(u) == 1

def random_int_unicode_tuple():
    return lambda: (evaluate(integers), evaluate(unicodes))

@forall(tries=10, l=lists(items=random_int_unicode_tuple))
def test_a_tupled_list(l):
    for x in l:
        assert type(x[0]) == int and type(x[1]) == unicode

@forall(tries=10, x=integers, y=integers)
def test_addition_associative(x, y):
    assert x + y == y + x

@forall(tries=10, l=lists)
def test_reverse_reverse(l):
    assert list(reversed(list(reversed(l)))) == l

@forall(tries=10, c=characters)
def test_characters(c):
    assert len(c) == 1

@forall(tries=10, d=dicts(items=unicodes, values=integers))
def test_dicts(d):
    for x, y in d.iteritems():
        assert type(x) == unicode
        assert type(y) == int

@forall(tries=10, d=dicts(items=unicodes, values=lists, size=(2, 2)))
def test_dicts_size(d):
    assert len(d) == 2
    for x, y in d.iteritems():
        assert type(x) == unicode
        assert type(y) == list
