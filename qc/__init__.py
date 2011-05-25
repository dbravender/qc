# Copyright (c) 2009-2011, Dan Bravender <dan.bravender@gmail.com>

import random
import os
from functools import partial

def integers(low=0, high=100):
    '''Endlessly yields random integers between (inclusively) low and high.
       Yields low then high first to test boundary conditions.
    '''
    yield low
    yield high
    while True:
        yield random.randint(low, high)

def lists(items=integers(), size=(0, 100)):
    '''Endlessly yields random lists varying in size between size[0]
       and size[1]. Yields a list of the low size and the high size 
       first to test boundary conditions.
    '''
    yield [items.next() for _ in xrange(size[0])]
    yield [items.next() for _ in xrange(size[1])]
    while True:
        yield [items.next() for _ in xrange(random.randint(size[0], size[1]))]

def key_value_generator(keys=integers(), values=integers()):
    while True:
        yield [keys.next(), values.next()]

def dicts(key_values=key_value_generator(), size=(0, 100)):
    while True:
        x = {}
        for _ in xrange(random.randint(size[0], size[1])):
            item, value = key_values.next()
            while item in x:
                item, value = key_values.next()
            x.update({item: value})
        yield x

def unicodes(size=(0, 100), minunicode=0, maxunicode=255):
    for r in (size[0], size[1]):
        yield u''.join(unichr(random.randint(minunicode, maxunicode)) \
                       for _ in xrange(r))
    while True:
        yield u''.join(unichr(random.randint(minunicode, maxunicode)) \
                       for _ in xrange(random.randint(size[0], size[1])))


characters = partial(unicodes, size=(1, 1))

def forall(tries=100, **kwargs):
    def wrap(f):
        def wrapped(**inkwargs):
            for _ in xrange(tries):
                random_kwargs = (dict((name, gen.next())
                                 for (name, gen) in kwargs.iteritems()))
                if forall.verbose or os.environ.has_key('QC_VERBOSE'):
                    from pprint import pprint
                    pprint(random_kwargs)
                random_kwargs.update(**inkwargs)
                f(**random_kwargs)
        wrapped.__name__ = f.__name__
        return wrapped
    return wrap
forall.verbose = False # if enabled will print out the random test cases

__all__ = ['integers', 'lists', 'unicodes', 'characters', 'forall']
