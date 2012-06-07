# Copyright (c) 2009-2011, Dan Bravender <dan.bravender@gmail.com>

import random
import os
import functools
from copy import deepcopy


def integers(low=0, high=100):
    '''Endlessly yields random integers between (inclusively) low and high.
       Yields low then high first to test boundary conditions.
    '''
    yield low
    yield high
    while True:
        yield random.randint(low, high)


def floats(low=0.0, high=100.0):
    '''Endlessly yields random floats between (inclusively) low and high.
       Yields low then high first to test boundary conditions.
    '''
    yield low
    yield high
    while True:
        yield random.uniform(low, high)


def lists(items=integers(), size=(0, 100)):
    '''Endlessly yields random lists varying in size between size[0]
       and size[1]. Yields a list of the low size and the high size
       first to test boundary conditions.
    '''
    yield [next(items) for _ in range(size[0])]
    yield [next(items) for _ in range(size[1])]
    while True:
        yield [next(items) for _ in range(random.randint(size[0], size[1]))]


def tuples(items=integers(), size=(0, 100)):
    '''Endlessly yields random tuples varying in size between size[0]
       and size[1]. Yields a tuple of the low size and the high size
       first to test boundary conditions.
    '''
    yield tuple([next(items) for _ in range(size[0])])
    yield tuple([next(items) for _ in range(size[1])])
    while True:
        yield tuple([next(items)
            for _ in range(random.randint(size[0], size[1]))])


def key_value_generator(keys=integers(), values=integers()):
    while True:
        yield [next(keys), next(values)]


def dicts(key_values=key_value_generator(), size=(0, 100)):
    while True:
        x = {}
        for _ in range(random.randint(size[0], size[1])):
            item, value = next(key_values)
            while item in x:
                item, value = next(key_values)
            x.update({item: value})
        yield x


def unicodes(size=(0, 100), minunicode=0, maxunicode=255):
    for r in (size[0], size[1]):
        yield ''.join(chr(random.randint(minunicode, maxunicode))
            for _ in range(r))
    while True:
        yield ''.join(chr(random.randint(minunicode, maxunicode))
            for _ in range(random.randint(size[0], size[1])))


characters = functools.partial(unicodes, size=(1, 1))


def objects(_object_class, _fields={}, *init_args, **init_kwargs):
    ''' Endlessly yields objects of given class, with fields specified
        by given dictionary. Uses given constructor arguments while creating
        each object.
    '''
    while True:
        ctor_args = [next(arg) for arg in init_args]
        ctor_kwargs = (dict((k, next(v)) for k, v in init_kwargs.items()))
        obj = _object_class(*ctor_args, **ctor_kwargs)
        for k, v in _fields.items():
            setattr(obj, k, next(v))
        yield obj


def forall(tries=100, **kwargs):
    def wrap(f):
        @functools.wraps(f)
        def wrapped(*inargs, **inkwargs):
            for _ in range(tries):
                random_kwargs = (dict((name, next(gen))
                                 for (name, gen) in kwargs.items()))
                if forall.verbose or 'QC_VERBOSE' in os.environ:
                    from pprint import pprint
                    pprint(random_kwargs)
                random_kwargs.update(**inkwargs)
                f(*inargs, **random_kwargs)
        return wrapped
    return wrap
forall.verbose = False  # if enabled will print out the random test cases


default_annotation_checks = {
    int: integers,
    float: floats,
    list: lists,
    tuple: tuples,
    dict: dicts,
    str: unicodes,
    object: objects,
}


def check_annotations(f, annotation_checks=None, tries=100):
    '''
    Check Python 3 annotations
    '''
    if annotation_checks is None:
        annotation_checks = default_annotation_checks
    inputs = deepcopy(f.__annotations__)
    output = inputs.pop('return', None)
    args = {arg: annotation_checks[typ]() for arg, typ in inputs.items()}
    for _ in range(tries):
        test_args = {arg: next(iterator) for arg, iterator in args.items()}
        response_type = type(f(**test_args))
        assert response_type == output, (
            'Was expecting %s to return %r but got %r with '
            'these arguments: %r' % (
                f.__name__, output, response_type, test_args))


__all__ = [
    'integers', 'floats', 'lists', 'tuples', 'unicodes', 'characters',
    'objects', 'forall']
