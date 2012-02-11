from qc import integers, floats, unicodes, characters, lists, tuples, dicts, objects, forall

@forall(tries=10, i=integers())
def test_integers(i):
    assert type(i) == int
    assert i >= 0 and i <= 100

@forall(tries=10, l=lists(items=integers()))
def test_a_int_list(l):
    assert type(l) == list

@forall(tries=10, l=tuples(items=integers()))
def test_a_int_tuple(l):
    assert type(l) == tuple

@forall(tries=10, i=floats())
def test_floats(i):
    assert type(i) == float
    assert i >= 0.0 and i <= 100.0

@forall(tries=10, l=lists(items=floats()))
def test_a_float_list(l):
    assert type(l) == list
    for x in l:
        assert type(x) == float

@forall(tries=10, ul=lists(items=unicodes()))
def test_unicodes_list(ul):
    assert type(ul) == list
    if len(ul):
        assert type(ul[0]) == str

@forall(tries=10, l=lists(items=integers(), size=(10, 50)))
def test_lists_size(l):
    assert len(l) <= 50 and len(l) >= 10

@forall(tries=10, l=tuples(items=integers(), size=(10, 50)))
def test_tuples_size(l):
    assert len(l) <= 50 and len(l) >= 10

@forall(tries=10, u=unicodes())
def test_unicodes(u):
    assert type(u) == str

@forall(tries=10, u=unicodes(size=(1,1)))
def test_unicodes_size(u):
    assert len(u) == 1

def random_int_str_tuple():
    i = integers()
    u = unicodes()
    while True:
        yield (next(i), next(u))

@forall(tries=10, l=lists(items=random_int_str_tuple()))
def test_a_tupled_list(l):
    for x in l:
        assert type(x[0]) == int and type(x[1]) == str

@forall(tries=10, x=integers(), y=integers())
def test_addition_commutative(x, y):
    assert x + y == y + x

@forall(tries=10, l=lists())
def test_reverse_reverse(l):
    assert list(reversed(list(reversed(l)))) == l

@forall(tries=10, c=characters())
def test_characters(c):
    assert len(c) == 1

def kv_str_integers():
    u = unicodes()
    i = integers()
    while True:
        yield (next(u), next(i))

@forall(tries=10, d=dicts(key_values=kv_str_integers()))
def test_dicts(d):
    for x, y in d.items():
        assert type(x) == str
        assert type(y) == int

def kv_unicodes_lists():
    u = unicodes()
    l = lists()
    while True:
        yield (next(u), next(l))

@forall(tries=10, d=dicts(key_values=kv_unicodes_lists(), size=(2, 2)))
def test_dicts_size(d):
    assert len(d) == 2
    for x, y in d.items():
        assert type(x) == str
        assert type(y) == list

@forall(tries=10, i=integers(low=0, high=10))
def each_integer_from_0_to_10(i, target_low, target_high):
    assert i >= target_low and i<= target_high

def test_qc_partials():
    each_integer_from_0_to_10(target_low=0, target_high=10)


class TestClass(object):
    def __init__(self, arg):
        self.arg_from_init = arg

@forall(tries=10, obj=objects(TestClass, {'an_int': integers(), 'a_float': floats()}, unicodes()))
def test_objects(obj):
    assert type(obj) == TestClass
    assert type(obj.an_int) == int
    assert type(obj.a_float) == float
    assert type(obj.arg_from_init) == str

