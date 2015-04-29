import os

from fabric.api import task, env, cd, get, run, execute, local
from fabric.context_managers import shell_env
from fabric.operations import require

from ..core import stage


__all__ = ['run_backup', 'download']


#
# Task
#


@task(name="run")
def run_backup():
    """Run backup script on remote"""
    require('environment', provided_by=[stage])

    if not os.path.exists(env['project']['project_backup_path']):
        local('mkdir %(project_backup_path)s' % env['project'])
    with cd('%(application_shared_path)s' % env['application']), shell_env(
            COMPOSE_PROJECT_NAME='%(application_name)s' % env['application']):
        run('%(application_maintenance_backup_command)s' % env['application'])
    with cd('%(application_tmp_path)s' % env['application']):
        run('install --owner {user} {src} {dest}'.format(
            user=env['user'],
            src='%(application_backup_volume_path)s/%(application_backup_filename)s' % env['application'],
            dest='%(application_tmp_path)s/' % env['application']))

    execute(download)


@task
def download():
    """Download backup file locally"""
    """Run backup script on remote"""
    require('environment', provided_by=[stage])

    get('%(application_tmp_path)s/%(application_backup_filename)s' % env['application'],
        '%(project_backup_path)s' % env['project'])