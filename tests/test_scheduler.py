import unittest
import mock


class SchedulerTestCase(unittest.TestCase):
    def test_scheduler_proxy(self):
        from victor import app_context
        from victor.scheduler import Scheduler, SchedulerProxy

        it = []
        SchedulerMock = mock.NonCallableMock(Scheduler)

        proxy = SchedulerProxy(app_context, it, Scheduler)
        proxy.scheduler = SchedulerMock
        proxy.start()

        SchedulerMock.start.assert_called_once_with()


    def test_gevent_scheduler(self):
        from victor import app_context
        from victor.scheduler import GEventScheduler
        from victor.workflow import Workflow
        from victor.transform import PassiveTransformer

        import gevent

        wf = Workflow()

        wf.register_transformer(PassiveTransformer('tf1'))
        wf.register_transformer(PassiveTransformer('tf2'))
        wf.register_transformer(PassiveTransformer('tf3'))

        app_context.workflows.append(wf)

        def it():
            for i in range(10):
                yield i

        with gevent.Timeout(1, False):
            scheduler = GEventScheduler(app_context, it)
            scheduler.start()

        assert scheduler.queue.qsize() > 0, 'Queue did not fill'
