import json
import jelly

class Foo(jelly.Serializable):
    def __init__(self):
        self.a = "hello"

class Bar(jelly.Serializable):
    def __init__(self):
        self.a = Foo()


def test_0():

    foo = Foo()

    e = jelly.encode(foo)

    json.dumps(e)

    print(e)

    assert e == {'JELLY': {'class': 'test_encode.Foo', 'state': {'a': 'hello'}}}

def test_1():

    bar = Bar()

    e = jelly.encode(bar)

    json.dumps(e)

    print(e)

    assert e == {'JELLY': {'class': 'test_encode.Bar', 'state': {'a': {'JELLY': {'class': 'test_encode.Foo', 'state': {'a': 'hello'}}}}}}

class ClassC(jelly.Serializable):
    def __init__(self):
        self.a = [Foo()]

def test_2():

    o = ClassC()

    e = jelly.encode(o)

    json.dumps(e)

    print(e)


