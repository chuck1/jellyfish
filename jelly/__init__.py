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
        """
        should return a json-serializable object
        """
       
        if hasattr(self, "__jellygetstate__"):
            state = self.__jellygetstate__(encode)
        else:
            state = dict(self.__dict__)

        state_encoded = encode(state)

        body = {
                "class": qualified_class_name(self), 
                "state": state_encoded,
                }
        dct = {"JELLY": body}

        # debug
        #json.dumps(dct)

        return dct

class Encoder(json.JSONEncoder):
    def default(self, obj):
        """
        should return a json-serializable object
        """

        if hasattr(obj, "__encode__"):
            return obj.__encode__(self.default)

        if isinstance(obj, dict):
            return dict((k, self.default(v)) for k, v in obj.items())

        if isinstance(obj, list):
            return list(self.default(v) for v in obj)

        if isinstance(obj, (int, float, bool, str)): return obj

        # let default implementation raise error
        return super().default(obj)

def decode_jelly_object(dct):
    dct = dct["JELLY"]
    split = dct["class"].split(".")
    m = __import__(".".join(split[:-1]), globals(), locals(), [split[-1]])
    print(m)
    print(dir(m))
    cls = getattr(m, split[-1])
    obj = cls.__new__(cls)

    state_encoded = dct["state"]
    state = decode(state_encoded)

    if hasattr(obj, "__jellysetstate__"):
        obj.__jellysetstate__(state)
    else:
        obj.__dict__.update(state)

    return obj

class Decoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.object_hook)

    def object_hook(self, dct):
        print(dct)

        if "JELLY" in dct.keys():
            return decode_jelly_object(dct)

        return dct

def decode(obj):
    """
    obj: json-serializable object
    
    return an object
    """
    if isinstance(obj, dict):
        if "JELLY" in obj.keys():
            return decode_jelly_object(obj)

        return dict((k, decode(v)) for k, v in obj.items())

    if isinstance(obj, list):
        return list(decode(v) for v in obj)

    return obj   

def encode(obj):
    return Encoder().default(obj)

def dumps(obj):
    return json.dumps(obj, cls=Encoder)

def loads(s):
    return json.loads(s, cls=Decoder)    








