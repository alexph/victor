from victor.command import parser as args, Victor
from victor.managers import WorkflowManager
from victor.workflow import Workflow


__all__ = ['Victor', 'args', 'workflow_manager', 'Workflow']


workflow_manager = WorkflowManager()
