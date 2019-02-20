import json
import pytest
import jelly

def test_0():

    class Foo:
        def __encode__(self, encode):
            return "hello"

    foo = Foo()

    jelly.dumps(foo)

def test_1():
    # the __encode__ method of an object must return something that is json serializable

    class Bar: pass

    class Foo:
        def __encode__(self, encode):
            return Bar()

    foo = Foo()

    with pytest.raises(TypeError) as excinfo:
        jelly.dumps(foo)




