
class Field(object):
    pass


class CharField(Field):
    pass


class Transform(object):
    def __init__(self):
        self._setup_fields()

    def __call__(self):
        pass

    def push_async(self):
        pass

    def push(self):
        pass

    def _setup_fields(self):
        self._fields = {}

        for a in dir(self):
            v = getattr(self, a)
            if isinstance(v, Field):
                self._fields[a] = v

        self._reset_fields()

    def _reset_fields(self):
        for f in self.get_fields():
            setattr(self, f, None)

    def get_fields(self):
        return self._fields

    def get_field(self, name):
        return self._fields[name]
