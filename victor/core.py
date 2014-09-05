from victor.scheduler import MultiProcessWorkerStrategy


class Victor(object):
    def __init__(self):
        self.workflows = []
        self.scheduler = None
        self.import_func = None

    def set_import(self, functor):
        self.import_func = functor

    def register(self, wf):
        self.workflows.append(wf)

    def run(self, app_context):
        # self.scheduler = Scheduler(app_context)

        # try:
        #     self.scheduler.start()
        # except KeyboardInterrupt:
        #     self.scheduler.stop()
        assert self.import_func is not None, 'App Import cannot be None'

        strategy = MultiProcessWorkerStrategy(self.import_func, app_context)
        strategy.start()
