import random
import types
import os
from functools import partial

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

__all__ = ['integers', 'lists', 'unicodes', 'characters', 'forall']
