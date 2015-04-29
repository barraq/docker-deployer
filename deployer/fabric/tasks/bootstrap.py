import os
import re

from fabric.api import execute, env, task
from fabric.contrib.console import confirm
from fabric.contrib.files import exists
from fabric.context_managers import hide, settings
from fabric.operations import require, run, local, sudo

from deployer.fabric.tasks.core import stage
from deployer.fabric.tasks.git import clone_local_repo, checkout_local_repo
from deployer.fabric.utils import exit
from deployer.fabric.application import get_application_mount_volumes

__all__ = ['all', 'local', 'remote']


#
# Helper Commands
#


__APPLICATION_PATHS_RE = re.compile('^application_(?P<name>[\w-]+)_path')


def remove_remote_directories():
    """Removes initial directories on remote"""

    for key in filter(__APPLICATION_PATHS_RE.match, env['application'].keys()):
        path = env['application'][key]
        if exists(path):
            sudo('rm -rf %s' % path)


def create_remote_directories():
    """Creates initial directories on remote"""

    execute(remove_remote_directories)

    all_paths = ''

    # create base directories
    for path in filter(__APPLICATION_PATHS_RE.match, env['application'].keys()):
        all_paths += '%s ' % env['application'][path]
        run('mkdir -p %s' % env['application'][path])

    # create volume directories
    for volume in get_application_mount_volumes(env):
        run('mkdir -p %s' % os.path.join('%(application_mount_path)s' % env['application'], volume))

    # set ownership
    run('chmod -R g=u %s' % all_paths)
    run('chown -R {user}:{group} {paths}'.format(user=env['user'], group=env['group'], paths=all_paths))


#
# Tasks
#


@task
def local(branch='master'):
    """Bootstraps deployment locally"""
    require('environment', provided_by=[stage])

    execute(clone_local_repo)
    execute(checkout_local_repo, branch=branch)


@task
def remote():
    """Bootstraps deployment remotely"""
    require('environment', provided_by=[stage])

    if (not exists('%(application_path)s' % env['application']) or
            confirm('\n%(application_path)s already exists. Do you want to continue?' % env['application'],
                    default=False)):
        with settings(hide('stdout', 'stderr')):
            execute(create_remote_directories)
    else:
        exit('\nAborting.')


@task(name="*")
def all(branch='master'):
    """Perform all bootstrap sub-tasks at once"""
    require('environment', provided_by=[stage])

    execute(local, branch=branch)
    execute(remote)
