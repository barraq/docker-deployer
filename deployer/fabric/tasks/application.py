import os

from fabric.api import require, cd, task, run, env
from fabric.context_managers import shell_env

from deployer.fabric.tasks.core import stage


__all__ = ['run_command', 'up', 'ps', 'start', 'stop']


#
# Task
#


@task
def up():
    """Create and start service on remote"""
    require('environment', provided_by=[stage])

    with cd(env['application']['application_shared_path']), shell_env(
            COMPOSE_PROJECT_NAME='%(application_name)s' % env['application']):
        run(env['application']['application_up_command'])


@task
def ps():
    """Get service status"""
    require('environment', provided_by=[stage])

    with cd(env['application']['application_shared_path']), shell_env(
            COMPOSE_PROJECT_NAME='%(application_name)s' % env['application']):
        run(env['application']['application_ps_command'])


@task(name='run')
def run_command(service=None, command=None):
    """Run a one-off command on remote"""
    require('environment', provided_by=[stage])

    if service is None or command is None:
        exit("Please provide a service name and a command to run")

    with cd(env['application']['application_shared_path']), shell_env(
            COMPOSE_PROJECT_NAME='%(application_name)s' % env['application']):
        run(env['application']['application_run_command'] % {
            'service': service,
            'command': command})


@task
def start(service=None):
    """Start a service on remote"""
    require('environment', provided_by=[stage])

    with cd(env['application']['application_shared_path']), shell_env(
            COMPOSE_PROJECT_NAME='%(application_name)s' % env['application']):
        if service:
            run(env['application']['application_start_service_command'] % service)
        else:
            run(env['application']['application_start_command'])


@task
def stop(service=None):
    """Stop service on remote"""
    require('environment', provided_by=[stage])

    with cd(env['application']['application_shared_path']), shell_env(
            COMPOSE_PROJECT_NAME='%(application_name)s' % env['application']):
        if service:
            run(env['application']['application_stop_service_command'] % service)
        else:
            run(env['application']['application_stop_command'])