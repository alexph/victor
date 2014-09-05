from victor.command import parser as args, VictorCommand
from victor.core import Victor
from victor.manager import Context, WorkflowManager
from victor.workflow import Workflow

import gevent.monkey

gevent.monkey.patch_all()


__all__ = ['Victor', 'args', 'workflow_manager', 'Workflow', 'app_context',\
           'VictorCommand']


workflow_manager = WorkflowManager()

app_context = Context()
