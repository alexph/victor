import unittest

from victor.core import Victor


class CommandTest(unittest.TestCase):
    def test_victor_cstr(self):
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
        from victor.examples.twitter import app

        command = VictorCommand(app_context)
        command.from_path('victor.examples.twitter.app')

        assert app == command.app
        assert command.app_context == app_context

    # def test_victor_run_wf(self):
    #     from victor import VictorCommand, app_context

    #     app = Victor()
    #     command = VictorCommand(app_context, app=app)
    #     command.run()
