from victor.logger import logger

from gevent.queue import Queue
from gevent.pool import Pool
import gevent

import multiprocessing
import time


class Worker(object):
    def __init__(self, wf):
        self.wf = wf

    def work(self):
        pass


class Scheduler(object):
    def __init__(self, app_context, iter_func):
        logger.info('Scheduler started %s' % self.__class__.__name__)
        self.app_context = app_context
        self.iter_func = iter_func

    def import_worker(self, iter_func):
        raise NotImplementedError()

    def start(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()


class GEventScheduler(Scheduler):
    def __init__(self, app_context, iter_func):
        super(GEventScheduler, self).__init__(app_context, iter_func)

        self.pool = Pool(self.app_context.children)
        self.queue = Queue()
        self.children = []

    def import_worker(self, iter_func):
        logger.info('Reading connection')

        while True:
            for x in iter_func():
                self.queue.put(x)

    def start(self):
        self.children = [
            gevent.spawn(self.import_worker, self.iter_func)
        ]
        gevent.joinall(self.children)

    def stop(self):
        self.queue.put('__stopall__')
        gevent.killall(self.children)


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

        while True:
            for x in import_func():
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
