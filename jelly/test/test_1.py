import json
import pytest
import jelly


class Foo(jelly.Serializable):
    def __jellygetstate__(self, encode):
        return {"a": "hello"}

class Bar(jelly.Serializable):
    def __init__(self):
        self.a = "hello"

def test_2():

    foo = Foo()

    s = jelly.dumps(foo)

    assert s == json.dumps({"JELLY": {"class": "test_1.Foo", "state": {"a": "hello"}}})

def test_3():


    foo = Foo()

    s = jelly.dumps(foo)

    assert s == json.dumps({"JELLY": {"class": "test_1.Foo", "state": {"a": "hello"}}})

    obj = jelly.loads(s)

    assert isinstance(obj, Foo)

    assert obj.a == "hello"

def test_4():


    foo = Bar()

    s = jelly.dumps(foo)

    assert s == json.dumps({"JELLY": {"class": "test_1.Bar", "state": {"a": "hello"}}})

    obj = jelly.loads(s)

    assert isinstance(obj, Bar)

    assert obj.a == "hello"





