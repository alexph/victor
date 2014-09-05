from victor.logger import logger


class BaseTransport(object):
    def __init__(self, wf, queue):
        logger.info('%s started' % self.__class__.__name__)

        self.wf = wf
        self.queue = queue

    def send(self, msg):
        raise NotImplementedError()

    def recv(self, msg):
        raise NotImplementedError()


class MemoryTransport(BaseTransport):
    def send(self, msg):
        logger.info('MemoryTransport sending message')
        self.recv(msg)

    def recv(self, msg):
        logger.info('MemoryTransport receiving message')
        self.queue.put(msg)


class Worker(object):
    def __init__(self, wf, transport):
        self.wf = wf
        self.transport = transport
