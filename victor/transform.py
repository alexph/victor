from victor.vector import Vector

class Transformer(object):
    input_vector = None
    output_vector = None

    # _input_data = {}
    # _data = None
    # _output_data = {}

    def __init__(self):
        assert isinstance(self.input_vector, Vector),\
            'input_vector is not a Vector class instance'
        assert isinstance(self.output_vector, Vector),\
            'output_vector is not a Vector class instance'

        self._input_data = {}
        self._data = {}
        self._output_data = {}

    def get_name(self):
        return self.__class__.__name__

    def push_data(self, input_data):
        self.on_input(input_data)

        #
        # Pass through input vector
        self._pass_input_vector(input_data)

        #
        # Post validation input data
        self._data = self.input_vector.data.copy()

        #
        # Post data hook
        self.on_post_input(self._data)
        
        #
        # Run through transformer
        for k, v in self._data.copy().iteritems():
            self._data[k] = self._run_field_hook(k, v)

        #
        # Pass through output vector
        self._pass_output_vector(self._data)

        output_data = self.output_vector.data.copy()

        self.on_output(output_data)

        #
        # Get output data
        self._output_data = output_data

    def _pass_input_vector(self, input_data):
        self.input_vector(input_data)

    def _pass_output_vector(self, data):
        self.output_vector(data)

    def _run_field_hook(self, key, value):
        attr_name = 'transform_%s' % key

        if hasattr(self, attr_name):
            functor = getattr(self, attr_name)
            return functor(value, self._data)
        return value

    def on_input(self, data):
        pass

    def on_post_input(self, data):
        pass

    def on_output(self, data):
        pass

    @property
    def output(self):
        return self._output_data
