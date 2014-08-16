from victor.pipeline import LocalPipeline

from collections import defaultdict


class Workflow(object):
    transformers = {}
    flow_map = {}
    transport = None

    def __init__(self, transport=None):
        self.transformers = {}
        self.flow_map = defaultdict(list)

    def register_transformer(self, cls):
        self.transformers[cls.get_name()] = cls

    def connect(self, output_name, input_name):
        if output_name is None:
            output_name = 'root'
        self.flow_map[output_name].append(input_name)

    def get_transformer(self, name):
        return self.transformers[name]

    def get_outputs(self, input_name):
        return self.flow_map[input_name]

    def get_flow_map(self):
        return self.flow_map

    def run(self, iter_generator, cls=LocalPipeline):
        runner = cls(self)
        runner.start(iter_generator)
        return runner
