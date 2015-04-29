import os

from fabric.api import require, execute, task, local, run, env
from fabric.contrib.project import rsync_project

from core import stage
from deployer.fabric.project import get_project_shared_cache_for_version


__all__ = ['push', 'pull', 'sync', 'all']


#
# Task
#


@task
def push(branch='master'):
    """Push docker service image to docker registry"""
    require('environment', provided_by=[stage])

    # execute(checkout_local_repo, branch=branch)
    local('docker push {registry}/{path}:{version}'.format(
        registry=env['docker']['docker_registry'],
        path=os.path.join('%(application_docker_repository)s' % env['application'],
                          '%(application_name)s' % env['application']),
        version=branch))


@task
def pull(branch='master'):
    """Pull docker service image from docker registry on remote"""
    require('environment', provided_by=[stage])

    # execute(checkout_local_repo, branch=branch)
    run('docker pull {registry}/{path}:{version}'.format(
        registry=env['docker']['docker_registry'],
        path=os.path.join('%(application_docker_repository)s' % env['application'],
                          '%(application_name)s' % env['application']),
        version=branch))


@task
def sync(branch='master'):
    """Synchronize local shared configuration with remote"""
    require('environment', provided_by=[stage])

    rsync_project(
        env['application']['application_shared_path'],
        local_dir='%s/' % get_project_shared_cache_for_version(env, branch),
        delete=True,
        extra_opts='--checksum')


@task(name="*")
def all(branch='master'):
    """Perform all publish sub-tasks at once"""
    require('environment', provided_by=[stage])

    execute(push, branch=branch)
    execute(pull, branch=branch)