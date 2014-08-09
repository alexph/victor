from nose.tools import raises

import unittest

from victor.exceptions import FieldRequiredError
from victor.transform import Transformer
from victor.vector import StringField, Vector


class TransformerTestCase(unittest.TestCase):
    def test_transformer_name(self):
        """
        Test that a transformer can return its class name so
        that it can be named in workflows.

        """
        class NamedTransformer(Transformer):
            input_vector = Vector()
            output_vector = Vector()

        tf = NamedTransformer()

        assert tf.get_name() == 'NamedTransformer',\
            'Transformer does not know its own name'

    @raises(AssertionError)
    def test_transformer_input_cls(self):
        """
        Test missing input vector throws exception.

        """
        class InputTransformer(Transformer):
            pass

        InputTransformer()

    @raises(AssertionError)
    def test_transformer_output_cls(self):
        """
        Test missing input vector throws exception.

        """
        class OutputTransformer(Transformer):
            pass

        OutputTransformer()

    def test_transform_hook(self):
        """
        Test transformer transform_"field" hook methods work and return values.

        """
        class HookTransformer(Transformer):
            input_vector = Vector()
            output_vector = Vector()

            def transform_count(self, value, data):
                return value + 1

        data = {
            'count': 1
        }

        tf = HookTransformer()
        tf.push_data(data)

        output = tf.output

        assert output['count'] == 2, 'Transformer did not increment count'

    def test_transform_input(self):
        class TrackVector(Vector):
            remote_addr = StringField()

        class InputTransformer(Transformer):
            input_vector = TrackVector()
            output_vector = Vector()

            def transform_remote_addr(self, value, data):
                geo = {
                    'city': 'Someplace',
                    'country': 'Somewhere'
                }

                data.update(geo)

                return value

        data = {
            'remote_addr': 'some ip'
        }

        tf = InputTransformer()
        tf.push_data(data)

        output = tf.output

        assert 'city' in output,  'City field not in output'
        assert 'country' in output, 'Country field not in output'
        assert 'remote_addr' in output, 'Remote addr not in output'

    @raises(FieldRequiredError)
    def test_ouput_missing_field(self):
        """
        Test output validation fires with data that has already passed
        through input.

        """
        class OutputVector(Vector):
            name = StringField(required=True)

        class NameTransformer(Transformer):
            input_vector = Vector()
            output_vector = OutputVector()

        tf = NameTransformer()
        tf.push_data({})

    @raises(FieldRequiredError)
    def test_input_missing_field(self):
        """
        Test that input does notice a missing field.

        """
        class InputVector(Vector):
            name = StringField(required=True)

        class NameTransformer(Transformer):
            input_vector = InputVector()
            output_vector = Vector()

        tf = NameTransformer()
        tf.push_data({})
