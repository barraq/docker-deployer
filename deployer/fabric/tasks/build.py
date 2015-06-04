import os

from fabric.api import require, execute, lcd, task, local, env

from core import stage
from git import checkout_local_repo
from deployer.fabric.project import get_project_shared_cache_for_version
from deployer.fabric.files import copy_template


__all__ = ['all', 'local', 'remote']


#
# Helper Commands
#


def process_shared(version='master'):
    """Process shared files for given `version` and copy them to cache"""
    local('rm -rf %s' % get_project_shared_cache_for_version(env, version))
    for root, dirs, files in os.walk(env['project']['project_shared_path']):
        rel_root = os.path.relpath(root, env['project']['project_shared_path'])
        if rel_root == os.curdir:
            rel_root = ''

        # setup context for template
        context = env.copy()
        context.update({
            'branch': version
        })

        for dir in dirs:
            local('mkdir -p %s/%s' % (
                get_project_shared_cache_for_version(env, version),
                os.path.join(rel_root, dir)))

        for file in files:
            src = '%s/%s' % (root, file)
            dest = '%s/%s' % (get_project_shared_cache_for_version(env, version), os.path.join(rel_root, file))
            if file.endswith('.tpl'):
                copy_template(src, dest[:-4], context=context)
                os.chmod(dest[:-4], os.stat(src).st_mode)
            else:
                local('cp %s %s' % (src, dest))


#
# Task
#


@task
def build(branch='master'):
    """Build service image and shared data for a given `branch` (default: master)"""
    require('environment', provided_by=[stage])

    execute(checkout_local_repo, branch=branch)
    execute(process_shared, version=branch)
    with lcd(os.path.join(env['project']['project_repo_path'],
                          os.path.dirname(env['application']['application_dockerfile']))):
        local('docker build -t {registry}/{path}:{version} .'.format(
            registry=env['docker']['docker_registry'],
            path=os.path.join(env['application']['application_docker_repository'],
                              env['application']['application_name']),
            version=branch))
