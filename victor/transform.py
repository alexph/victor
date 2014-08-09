from victor.vector import Vector

class Transformer(object):
    input_vector = None
    output_vector = None
    data = None

    def __init__(self):
        assert isinstance(self.input_vector, Vector),\
            'input_vector is not a Vector class instance'
        assert isinstance(self.output_vector, Vector),\
            'input_vector is not a Vector class instance'

    def get_name(self):
        return self.__class__.__name__

    def push_data(self, input_data):
        pass

    def _pass_input_vector(self, input_data):
        self.input_vector(input_data)

    def _run_field_hook(self, key, value):
        attr_name = 'transform_%s' % key

        if hasattr(self, attr_name):
            functor = getattr(self, attr_name)
            return functor(value, self.data)
