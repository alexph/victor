import unittest


from victor.vector import Vector
from victor.transform import Transformer
from victor.workflow import Workflow


class TestWorkflow(unittest.TestCase):
    def test_workflow(self):
        class DummyTransformer(Transformer):
            input_vector = Vector()
            output_vector = Vector()

        class OtherTransformer(DummyTransformer):
            pass

        wf = Workflow()

        wf.register_transformer(DummyTransformer())
        wf.register_transformer(OtherTransformer())

        wf.connect(None, 'DummyTransformer')
        wf.connect('DummyTransformer', 'OtherTransformer')

        assert wf.get_outputs('root') == ['DummyTransformer'],\
            'DummyTransformer not in root outputs'
        assert wf.get_outputs('DummyTransformer') == ['OtherTransformer'],\
            'OtherTransformer not in DummyTransformer outputs'

        def test_iter():
            for x in range(0, 10):
                yield {'count': x}

            yield '__quit__'

        wf.run(test_iter)
