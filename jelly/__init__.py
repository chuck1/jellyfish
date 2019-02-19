import json

def qualified_class_name(o):
    # o.__module__ + "." + o.__class__.__qualname__ is an example in
    # this context of H.L. Mencken's "neat, plausible, and wrong."
    # Python makes no guarantees as to whether the __module__ special
    # attribute is defined, so we take a more circumspect approach.
    # Alas, the module name is explicitly excluded from __qualname__
    # in Python 3.

    module = o.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return o.__class__.__name__    # Avoid reporting __builtin__
    else:
        return module + '.' + o.__class__.__name__

class Serializable:
    def __encode__(self, encode):
        if hasattr(self, "__jellygetstate__"):
            state = self.__jellygetstate__(encode)
        else:
            state = dict(self.__dict__)

        body = {
                "class": qualified_class_name(self), 
                "state": state,
                }
        dct = {"JELLY": body}
        return dct

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "__encode__"):
            return obj.__encode__(self.default)
        return super().default(obj)


class Decoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.object_hook)

    def object_hook(self, dct):
        print(dct)

        if "JELLY" in dct.keys():
            dct = dct["JELLY"]
            split = dct["class"].split(".")
            m = __import__(".".join(split[:-1]))
            print(m)
            print(dir(m))
            cls = getattr(m, split[-1])
            obj = cls.__new__(cls)
            if hasattr(obj, "__jellysetstate__"):
                obj.__jellysetstate__(dct["state"])
            else:
                obj.__dict__.update(dct["state"])
            return obj

        return dct

def dumps(obj):
    return json.dumps(obj, cls=Encoder)

def loads(s):
    return json.loads(s, cls=Decoder)    

