import unittest

from victor.core import Victor


class CommandTest(unittest.TestCase):
    def test_victor_constructor(self):
        from victor import VictorCommand, app_context

        app = Victor()
        command = VictorCommand(app_context, app=app)

        assert command.app == app
        assert command.app_context == app_context

    def test_victor_from_object(self):
        from victor import VictorCommand, app_context

        app = Victor()
        command = VictorCommand(app_context)
        command.from_object(app)

        assert command.app == app
        assert command.app_context == app_context

    def test_victor_from_path(self):
        from victor import VictorCommand, app_context
        from victor.testing import dummy_app
        import gevent

        command = VictorCommand(app_context)
        command.from_path('victor.testing.dummy_app')

        assert dummy_app == command.app
        assert command.app_context == app_context

    # def test_victor_run_wf(self):
    #     from victor import VictorCommand, app_context

    #     app = Victor()
    #     command = VictorCommand(app_context, app=app)
    #     command.run()
