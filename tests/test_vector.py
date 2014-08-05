from nose.tools import raises

import unittest

from victor.exceptions import (
    FieldValidationException,
    FieldTypeConversionError,
    VectorInputTypeError
)

from victor.vector import (
    Vector,
    CharField,
    StringField,
    ListField,
    IntField,
    FloatField
)


class VectorTestCase(unittest.TestCase):
    def test_field_setup(self):
        class DummyVector(Vector):
            field_str = CharField()

        vector = DummyVector()

        assert 'field_str' in vector.get_fields()
        assert getattr(vector, 'field_str') is None
        assert isinstance(vector.get_field('field_str'), CharField)

        vector.field_str = 'dummy'

        assert vector.field_str == 'dummy'

    @raises(AssertionError)
    def test_list_field_type(self):
        ListField(int)

    def test_list_field_data(self):
    	field = ListField(CharField(), strict=True)

        data = ('test',)

        field.set_data(data)

        assert field.data == data, 'Data given to ListField does not match'

    @raises(FieldValidationException)
    def test_list_field_bad_type(self):
        field = ListField(StringField(strict=True), strict=True)

        data = ({},)

        field.set_data(data)

    def test_field_type_cast(self):
        field_str = StringField()
        field_str.set_data(10)

        assert isinstance(field_str.data, str), 'Data should have been cast to a string'

        field_int = IntField()
        field_int.set_data('hello')

        assert isinstance(field_int.data, int), 'Data should have been cast to an integer'
        assert field_int.data == 0

        field_float = FloatField()
        field_float.set_data('hello')

        assert isinstance(field_float.data, float), 'Data should have been cast to an integer'
        assert field_float.data == 0

    @raises(FieldTypeConversionError)
    def test_int_field_bad_cast(self):
        #
        # Trying to pass a string to an IntField in non strict mode
        # will try to cast to int and should yield an error when 
        # missing value is bad.
        field_int = IntField(missing_value=False)
        field_int.set_data('hello')

    @raises(FieldTypeConversionError)
    def test_float_field_bad_cast(self):
        #
        # Trying to pass a string to an IntField in non strict mode
        # will try to cast to int and should yield an error when 
        # missing value is bad.
        field_float = FloatField(missing_value=False)
        field_float.set_data('hello')

    @raises(VectorInputTypeError)
    def test_vector_bad_input(self):
        vector = Vector()
        vector('bad input')

    def test_vector_required_fields(self):
        class RequiredVector(Vector):
            name = StringField(required=True)
            age = IntField(required=True)

        vector = RequiredVector()

        data = {}

        vector(data)
