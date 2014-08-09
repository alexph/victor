from nose.tools import raises

import unittest

from victor.vector import Vector
from victor.transform import Transformer


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
