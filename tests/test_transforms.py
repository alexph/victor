import unittest

from victor.transform import Transform, CharField


class TransformsTestCase(unittest.TestCase):
    def test_field_setup(self):
        class FieldTransform(Transform):
            field_str = CharField()

        transform_obj = FieldTransform()

        assert 'field_str' in transform_obj.get_fields()
        assert getattr(transform_obj, 'field_str') is None
        assert isinstance(transform_obj.get_field('field_str'), CharField)
