from collections import defaultdict

from multiprocessing import Queue, Process, Pool

import logging
import time


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class ProcessProxy(object):
    def __init__(self, tf):
        self.tf = tf
        self.pool = Pool()

    def push_data(self, queue, data):
        self.tf.push_data(data)
        output = self.tf.output
        queue.put_nowait({'from': self.tf.get_name(), 'data': output})
        return output

        # def async(tf, q, data):
        #     tf.push_data(data)
        #     output = self.tf.output
        #     q.put_nowait({'from': self.tf.get_name(), 'data': output})
        #     return output

        # self.pool.apply_async(async, (self.tf, queue, data))


class WorkflowManager(object):
    def run(self, input_iter):
        pass


class MPWorkflowManager(WorkflowManager):
    def run(self, input_iter):
        r = Process(target=self._read, args=(input_iter, self.queue,))
        w = Process(target=self._worker, args=(self.queue,))

        r.daemon = True
        # w.daemon = True

        r.start()
        w.start()

        r.join()
        w.join()

    def _read(self, input_iter, q):
        while True:
            for x in input_iter():
                if x is not None:
                    q.put_nowait({'from': 'root', 'data': x})

                    if x == '__quit__':
                        return
            time.sleep(5)

    def _worker(self, q):
        while True:
            if not q.empty():
                x = q.get()

                if x['data'] == '__quit__':
                    return
                else:
                    for next in self.get_outputs(x['from']):
                        push = self.get_transformer(next).push_data
                        push(q, x['data'])


class Workflow(object):
    _transformers = {}
    _flow_map = {}

    manager = None

    def __init__(self, manager=None):
        self._transformers = {}
        self._flow_map = defaultdict(list)

        if manager is None:
            manager = WorkflowManager()

        self.manager = manager

    def register_transformer(self, cls, proxy=None):
        if proxy is None:
            proxy = ProcessProxy
        self._transformers[cls.get_name()] = proxy(cls)

    def connect(self, output_name, input_name):
        if output_name is None:
            output_name = 'root'
        self._flow_map[output_name].append(input_name)

    def get_transformer(self, name):
        return self._transformers[name]

    def get_outputs(self, input_name):
        return self._flow_map[input_name]

    def get_flow_map(self):
        return self._flow_map

    def run(self, input_iter):
        pass
