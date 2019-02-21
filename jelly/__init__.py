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
    def __encode__(self, encoder):
        """
        should return a json-serializable object
        """
       
        if hasattr(self, "__jellygetstate__"):
            state = self.__jellygetstate__(encoder)
        else:
            state = dict(self.__dict__)

        state_encoded = encoder.encode(state)

        body = {
                "class": qualified_class_name(self), 
                "state": state_encoded,
                }
        dct = {"JELLY": body}

        # debug
        #json.dumps(dct)

        return dct

class Encoder:
    def encode(self, obj):
        """
        should return a json-serializable object
        """

        if hasattr(obj, "__encode__"):
            return obj.__encode__(self)

        if isinstance(obj, dict):
            return dict((k, self.encode(v)) for k, v in obj.items())

        if isinstance(obj, list):
            return list(self.encode(v) for v in obj)

        if isinstance(obj, (int, float, bool, str)): return obj

        if obj is None: return obj

        raise TypeError()

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

class Decoder:
    def decode(self, obj):
        """
        obj: json-serializable object
        
        return an object
        """
        if isinstance(obj, dict):
            if "JELLY" in obj.keys():
                return decode_jelly_object(obj)
    
            def _():
                for k, v in obj.items():
                    y = self.decode(v)
                    print(repr(k), repr(v), repr(y))
                    yield k, y

            return dict(_())
    
        if isinstance(obj, list):
            return list(decode(v) for v in obj)
    
        return obj   

    async def adecode(self, obj):
        """
        obj: json-serializable object
        
        return an object
        """
        if isinstance(obj, dict):
            if "JELLY" in obj.keys():
                return decode_jelly_object(obj)
    
            async def _():
                for k, v in obj.items():
                    y = await self.adecode(v)
                    print(repr(k), repr(v), repr(y))
                    yield k, y

            return dict([e async for e in _()])
    
        if isinstance(obj, list):

            async def _():
                for v in obj:
                    yield await self.adecode(v)

            return [e async for e in _()]
    
        return obj   

def decode(obj):
    return Decoder().decode(obj)

def encode(obj):
    return Encoder().encode(obj)

def dumps(obj):
    return json.dumps(encode(obj))

def loads(s):
    return decode(json.loads(s))








