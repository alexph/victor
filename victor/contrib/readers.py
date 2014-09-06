from victor.injestion import ReaderBase


class BeanstalkReader(ReaderBase):
    def __init__(self, *args, **kwargs):
        import beanstalkc
        self.beanstalk = beanstalkc.Connection(*args, **kwargs)

    def read(self):
        job = self.beanstalk.reserve()
        yield job.body
        job.delete()
