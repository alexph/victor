from nose.tools import raises

import unittest

from victor.exceptions import (
    FieldValidationException,
    FieldTypeConversionError,
    FieldRequiredError,
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
    def test_vector_name(self):
        """
        Test vector object has a name which is required for creating
        workflows.

        """
        class NamedVector(Vector):
            pass

        vector = NamedVector()
        assert vector.get_name() == 'NamedVector', 'Vector does not know its own name'

    def test_field_setup(self):
        """
        Test Vector objects will correctly build their fields from
        attributes and that values can be stored and retrieved.

        """
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
        """
        Test that the ListField constructor will halt if its
        sub-field parameter is not a valid Field or subclass.

        """
        ListField(int)

    def test_list_field_data(self):
        """
        Test that a list field can be passed an iterable and
        retain it's value without exception. When the ListField
        has strict enabled an exception will be raised. 

        """
        field = ListField(CharField(), strict=True)

        data = ('test',)

        field.set_data(data)

        assert field.data == data, 'Data given to ListField does not match'

    @raises(FieldValidationException)
    def test_list_field_bad_type(self):
        """
        Test that an exception is raised when a ListField is given
        an iterable object with an incorrect item type. With strict
        enabled exceptions will be raised.

        """
        field = ListField(StringField(strict=True), strict=True)

        data = ({},)

        field.set_data(data)

    def test_field_type_cast(self):
        """
        Test basic fields can cast value to type and revert to
        a set value.
        """
        field_str = StringField()
        field_str.set_data(10)

        assert isinstance(field_str.data, str),\
            'Data should have been cast to a string'

        field_int = IntField()
        field_int.set_data('hello')

        assert isinstance(field_int.data, int),\
            'Data should have been cast to an integer'
        assert field_int.data == 0

        field_float = FloatField()
        field_float.set_data('hello')

        assert isinstance(field_float.data, float),\
            'Data should have been cast to an integer'
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
        """
        Test that passing a string to an FloatField in non strict mode
        will try to cast to int and should yield an error when
        missing value is bad.

        """
        field_float = FloatField(missing_value=False)
        field_float.set_data('hello')

    @raises(VectorInputTypeError)
    def test_vector_bad_input(self):
        """
        Test that a vector will throw an exception when data is not a 
        dictionary.

        """
        vector = Vector()
        vector('bad input')

    @raises(FieldRequiredError)
    def test_vector_missing_fields(self):
        """
        Test a vector object with a field set to require will throw
        an exception when the input is missing.

        """
        class RequiredVector(Vector):
            name = StringField(required=True)

        vector = RequiredVector()
        data = {}
        vector(data)

    def test_vector_input_mapping(self):
        """
        Test that vector will accept input and map values to attributes.

        """
        vector = Vector()
        data = {
            'name': 'Bob',
            'age': 30
        }
        vector(data)

        assert hasattr(vector, 'name'), 'Name field not mapped on vector'
        assert hasattr(vector, 'age'), 'Age field not mapped on vector'
        assert vector.name == 'Bob', 'Name field not set'
        assert vector.age == 30, 'Age field not set'

    @raises(FieldTypeConversionError)
    def test_vector_nested_validation(self):
        """
        Test vector nested field validation when a value cannot be
        cast and the missing_value is disabled.

        """
        class DummyVector(Vector):
            number = IntField(missing_value=False)

        vector = DummyVector()
        data = {
            'number': 'not a number'
        }
        vector(data)
