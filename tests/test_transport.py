import unittest


from victor.pipeline import Message
from victor.workflow import Workflow
from Queue import Queue


class TestTransport(unittest.TestCase):
    def test_memory_transport(self):
        from victor.transport import MemoryTransport
        
        queue = Queue()
        wf = Workflow()
        tp = MemoryTransport(wf, queue, None)

        msg = Message()

        tp.send(msg)

        assert queue.get() == msg, 'Message did not loop back to queue'
