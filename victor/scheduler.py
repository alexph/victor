from victor.injestion import ReaderBase
from victor.logger import logger
# from victor.pipeline import GEventPipeline
# from victor.transport import GEventQueueTransport

from gevent.queue import Queue, JoinableQueue
# from gevent.pool import Pool
import gevent

from collections import defaultdict

import copy
import multiprocessing
import time


# class Worker(object):
#     def __init__(self, wf):
#         self.wf = wf

#     def work(self):
#         pass


class Scheduler(object):
    """
    The Scheduler will read input from the worker queue and
    move messages on to Pipeline workers. Workers are created
    from each separate component of a workflow multiplied by the
    app_context multiplier setting.

    Messages are continually looped. When output is created
    they move back to the queue to wait for their next step.

    """
    def __init__(self, app_context, iter_func):
        logger.info('Scheduler started %s' % self.__class__.__name__)
        self.app_context = app_context
        self.iter_func = iter_func

        self.setup_components()

    def import_worker(self, iter_func):
        raise NotImplementedError()

    def start(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()

    def setup_components(self):
        pass

    def create_pipelines(self):
        pl = self.app_context.pipeline_class()


class GEventScheduler(Scheduler):
    def __init__(self, app_context, iter_func):
        # self.pool = Pool(self.app_context.children)
        self.queue = Queue()
        self.children = []
        self.shutdown = False
        self.queues = {}
        self.pipelines = {}

        super(GEventScheduler, self).__init__(app_context, iter_func)

        print self.queues
        print self.pipelines

    def import_worker(self, iter_func):
        logger.info('Reading connection')
        while True:
            for x in iter_func():
                self.queue.put(x)
                gevent.sleep(0)

    def setup_components(self):
        for wf in self.app_context.workflows:
            for name, tf in wf.get_transformers().items():
                local_queue = Queue()
                self.queues[name] = local_queue
                transport = self.app_context.transport_class(wf, local_queue,\
                    self.queue)
                self.pipelines[name] = self.app_context.pipeline_class(\
                    wf, tf=tf, transport=transport)

    # def setup_components(self):
    #     components = defaultdict(list)

    #     for wf in self.app_context.workflows:
    #         for name, tf in wf.get_transformers().iteritems():
    #             for index_id in range(0, self.app_context.multiplier):
    #                 components[name].append(self.\
    #                     create_component_worker(index_id, tf))

    #     self.components = components

    # def create_component_worker(self, index_id, tf):
    #     logger.debug('Creating component %s #%d' % (tf.get_name(), index_id))

    #     tf_copy = copy.copy(tf)

    #     def feed_tf(tf_copy, queue):
    #         while True:
    #             if not queue.empty():
    #                 message = queue.get()
    #                 tf.push_data(message)

    #     return feed_tf

    def start(self):
        self.children = [
            gevent.spawn(self.import_worker, self.iter_func)
        ]
        gevent.joinall(self.children)

    def stop(self):
        gevent.killall(self.children, timeout=2)


class SchedulerProxy(object):
    def __init__(self, app_context, iter_func, scheduler_class):
        self.scheduler = scheduler_class(app_context, iter_func)

    def start(self):
        self.scheduler.start()

    def stop(self):
        self.scheduler.stop()


class MultiProcessWorkerStrategy(object):
    def __init__(self, import_func, app_context, num_processes=8):
        self.import_func = import_func
        self.app_context = app_context
        self.in_queue = multiprocessing.Queue()
        self.out_queue = multiprocessing.Queue()
        self.num_processes = num_processes
        self.workers = []

    def start(self):
        im = multiprocessing.Process(
            target=self.import_loop,
            args=(self.import_func, self.in_queue))

        self.workers.append(im)

        for i in range(self.num_processes):
            p = multiprocessing.Process(
                target=self.worker,
                args=(i, self.in_queue, self.out_queue))
            self.workers.append(p)
            p.start()

        im.start()

        for w in self.workers:
            w.join()

    def import_loop(self, import_func, in_queue):
        logger.debug('Import loop starting')

        if isinstance(import_func, ReaderBase):
            functor = import_func.read
        else:
            functor = import_func

        while True:
            for x in functor():
                in_queue.put_nowait(x)
                time.sleep(0)

            time.sleep(0)

    def worker(self, worker_id, in_queue, out_queue):
        logger.debug('Launching scheduler in %s' % worker_id)

        def iter_func():
            while not in_queue.empty():
                logger.debug('Worker #%d getting task' % worker_id)
                task = in_queue.get()
                yield task

        scheduler = SchedulerProxy(
            self.app_context,
            iter_func,
            GEventScheduler
        )

        scheduler.start()
