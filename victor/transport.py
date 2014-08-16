class Context(object):
    pass


class BaseTransport(object):
    def __init__(self, wf, queue):
        self.wf = wf
        self.queue = queue

    def send(self, msg):
        raise NotImplementedError()

    def recv(self, msg):
        raise NotImplementedError()


class MemoryTransport(BaseTransport):
    def send(self, msg):
        self.recv(msg)

    def recv(self, msg):
        self.queue.put(msg)


class Worker(object):
    def __init__(self, wf, transport):
        self.wf = wf
        self.transport = transport
