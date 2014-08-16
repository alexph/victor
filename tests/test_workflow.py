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

        class CaptureTransformer(DummyTransformer):
            captured_data = []

            def on_output(self, data):
                CaptureTransformer.captured_data.append(data)

        wf = Workflow()

        wf.register_transformer(DummyTransformer())
        wf.register_transformer(OtherTransformer())
        wf.register_transformer(CaptureTransformer())

        wf.connect(None, 'DummyTransformer')
        wf.connect('DummyTransformer', 'OtherTransformer')
        wf.connect('OtherTransformer', 'CaptureTransformer')

        assert wf.get_outputs('root') == ['DummyTransformer'],\
            'DummyTransformer not in root outputs'
        assert wf.get_outputs('DummyTransformer') == ['OtherTransformer'],\
            'OtherTransformer not in DummyTransformer outputs'
        assert wf.get_outputs('OtherTransformer') == ['CaptureTransformer'],\
            'CaptureTransformer not in OtherTransformer outputs'

        def test_iter():
            for x in range(0, 10):
                yield {'count': x}

        wf.run(test_iter)

        assert len(CaptureTransformer.captured_data) == 10,\
            'Workflow should pass through all 10 items'
