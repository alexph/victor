import unittest


from victor.transform import Transformer
from victor.workflow import Workflow
from victor.vector import Vector


class CaptureTransformer(Transformer):
    input_vector = Vector()
    output_vector = Vector()

    captured_data = []

    def on_output(self, data):
        CaptureTransformer.captured_data.append(data)


class TestPipeline(unittest.TestCase):
    def test_local_pipeline(self):
        from victor.pipeline import LocalPipeline
        
        wf = Workflow()
        tf = CaptureTransformer()
        wf.register_transformer(tf)
        wf.connect(None, 'CaptureTransformer')

        pl = LocalPipeline(wf)

        data = [{'nothing': 0}, {'nothing': 1}, {'nothing': 2},\
                {'nothing': 3}, {'nothing': 4}]

        pl.start(lambda: data)

        assert data == tf.captured_data, 'Data in not matching data out'
