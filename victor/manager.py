from collections import defaultdict


class Context(object):
    in_process = False
    children = 4
    workflows = []
    components = []


class WorkflowManager(object):
    workflows = {}
    components = defaultdict(dict)

    def register(self, wf, tf):
        wf_name = wf.get_name()
        tf_name = tf.get_name()
        self.workflows[wf_name] = wf
        self.components[wf_name][tf_name] = tf
