from victor.exceptions import (
    FieldValidationException,
    FieldTypeConversionError,
    VectorInputTypeError
)


class Field(object):
    required = True
    """Field is required and an exception will be raised if missing"""

    missing_value = None
    """Value to use when field is missing and not required"""

    strict = False
    """Field value must pass validation or an exception will be raised"""

    cast_cls = None

    data = None

    def __init__(self, required=True, missing_value=None, strict=False):
        self.required = required
        self.missing_value = missing_value
        self.strict = strict

    def _validate(self, value):
        return True

    def _cast_type(self, value):
        return self.cast_cls(value)

    def set_data(self, value):
        if self.strict:
            if not self._validate(value):
                raise FieldValidationException('%s does not except this value' % self.__class__.__name__)
        elif self.cast_cls is not None:
            value = self._cast_type(value)

        self.data = value


class CharField(Field):
    pass


class StringField(Field):
    cast_cls = str

    def _validate(self, value):
        if not isinstance(value, (str, unicode)):
            return False

        return True


class IntField(Field):
    cast_cls = int
    _cast_fallback_value = 0

    def __init__(self, *args, **kwargs):
        super(IntField, self).__init__(*args, **kwargs)

        if self.missing_value is None:
            self.missing_value = self._cast_fallback_value

    def _cast_type(self, value):
        try:
            return self.cast_cls(value)
        except ValueError, exc:
            if self.missing_value is False:
                raise FieldTypeConversionError('Could not convert data or use missing_value: %s' % exc)

        return self.missing_value


class FloatField(IntField):
    cast_class = float
    _cast_fallback_value = 0.0


class ListField(Field):
    cls = None
    """Field class to represent list items"""

    def __init__(self, cls, *args, **kwargs):
        assert isinstance(cls, Field), 'cls is not a valid Field instance'

        self.cls = cls

        super(ListField, self).__init__(*args, **kwargs)

    def _validate(self, value):
        if not isinstance(value, (list, tuple)):
            raise FieldValidationException('ListField requires data to be a sequence type')

        for x in value:
            self.cls.set_data(value)

        self.data = value

        return True


class Vector(object):
    def __init__(self):
        self._fields = {}
        self._required = []

        self._setup_fields()

    def __call__(self, data):
        return self.input(data)

    def input(self, data):
        if not isinstance(data, dict):
            raise VectorInputTypeError('Vector input not a dictionary')
        self._validate()

    def _setup_fields(self):
        self._fields = {}

        for a in dir(self):
            v = getattr(self, a)
            if isinstance(v, Field):
                self._fields[a] = v

                if v.required:
                    self._required.append(a)

        self._reset_fields()

    def _reset_fields(self):
        for f in self.get_fields():
            setattr(self, f, None)

    def _validate(self):
        pass

    def get_fields(self):
        return self._fields

    def get_field(self, name):
        return self._fields[name]