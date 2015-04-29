import os

from fabric.api import require, cd, task, run, env
from fabric.context_managers import shell_env

from ..core import stage
from deployer.fabric.application import get_application_maintenance_tasks_commands


__all__ = ['do']


@task()
def do(task_name=None):
    """Execute maintenance task on remote"""
    require('environment', provided_by=[stage])

    tasks_commands = get_application_maintenance_tasks_commands(env)

    if tasks_commands is {} or tasks_commands is None:
        exit('No prepare command found for stage:%s' % env.environment)
    elif task_name is None and type(tasks_commands) is str:
        with cd(env['application']['application_shared_path']), shell_env(COMPOSE_PROJECT_NAME='%(application_name)s' % env['application']):
            run(env['application']['application_maintenance_tasks_command'])
    elif type(tasks_commands) is dict and task_name in tasks_commands:
        with cd(env['application']['application_shared_path']), shell_env(COMPOSE_PROJECT_NAME='%(application_name)s' % env['application']):
            run(tasks_commands[task_name])
    else:
        message = "Unable to execute task command named `%s`.\n" \
                  "Please use one of the followings:" % task_name
        for name in tasks_commands.keys():
            message += '\n - %s' % name
        exit(message)