from victor.pipeline import LocalPipeline
# from victor import workflow_manager

from collections import defaultdict


class Workflow(object):
    transformers = {}
    flow_map = {}
    transport = None

    def __init__(self, transport=None):
        self.transformers = {}
        self.flow_map = defaultdict(list)

    def register_transformer(self, tf):
        self.transformers[tf.get_name()] = tf

    def connect(self, output_name, input_name):
        if output_name is None:
            output_name = 'root'
        self.flow_map[output_name].append(input_name)

    def get_transformers(self):
        return self.transformers

    def get_transformer(self, name):
        return self.transformers[name]

    def get_outputs(self, input_name):
        return self.flow_map[input_name]

    def get_flow_map(self):
        """
        Get dictionary map of all transformer objects and
        the instances that they push to.

        """
        return self.flow_map

    def run(self, iter_generator, cls=LocalPipeline):
        """
        Run this workflow in a given pipeline. This factory
        method Will pass reference of the workflow on to a 
        pipeline and start iterating.

        """
        runner = cls(self)
        runner.start(iter_generator)
        return runner
