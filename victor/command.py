from victor.logger import logger

import argparse
import importlib
import multiprocessing


try:
    default_workers = multiprocessing.cpu_count()
except NotImplementedError:
    default_workers = 2
    logger.info('CPU count not available, default is %d' % default_workers)


parser = argparse.ArgumentParser(description='Victor command runner')
sub_parsers = parser.add_subparsers(help='sub-command help')

#
# Command for starting workflow process
parser_run = sub_parsers.add_parser('run')
parser_run.add_argument('module', help='Start Workflow from object path')
parser_run.add_argument('-w', help='Start Workflow from object path', default=default_workers)

#
# 
# parser_spawn = sub_parsers.add_parser('spawn')
# parser_spawn.add_argument('<module>', help='Start Workflow component from object path')


class VictorCommand(object):
    def __init__(self, app_context, app=None):
        logger.info('Victor says hello')

        self.app_context = app_context
        self.app = app

    def from_object(self, app):
        logger.info('App from object')
        self.app = app

    def from_path(self, module_path):
        logger.info('App from path')

        parts = module_path.split('.')
        obj_name = parts[-1]
        import_path = '.'.join(parts[:-1])
        module = importlib.import_module(import_path)
        self.app = module.__dict__[obj_name]

    def run(self):
        self.app.run(self.app_context)
