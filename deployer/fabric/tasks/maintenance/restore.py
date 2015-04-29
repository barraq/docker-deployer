import os

from fabric.api import task, env, cd, put, run, abort, local
from fabric.context_managers import shell_env
from fabric.contrib.files import exists
from fabric.operations import require

from ..core import stage


__all__ = ['run_restore', 'upload']


#
# Task
#


@task(name="run")
def run_restore():
    """Run restore script on remote"""
    require('environment', provided_by=[stage])

    if not os.path.exists('%(project_restore_path)s' % env['project']):
        abort('No %(project_restore_path)s directory found !' % env['project'])

    restore_file = '%(application_tmp_path)s/%(application_restore_filename)s' % env['application']

    if not exists(restore_file):
        abort('No %s file found on remote !' % restore_file)

    with cd('%(application_shared_path)s' % env['application']), shell_env(
            COMPOSE_PROJECT_NAME='%(application_name)s' % env['application']):
        run('cp %(application_tmp_path)s/%(application_restore_filename)s %(application_backup_volume_path)s/' % env['application'])
        run('%(application_maintenance_restore_command)s' % env['application'])


@task
def upload(filename=None):
    """Download backup file locally"""
    """Run backup script on remote"""
    require('environment', provided_by=[stage])

    if not os.path.exists('%(project_restore_path)s' % env['project']):
        abort('No %(project_restore_path)s directory found !' % env['project'])

    upload_file = '%s/%s' % (env['project']['project_restore_path'],
                             filename or env['application']['application_restore_filename'])

    if not os.path.exists(upload_file):
        abort('No backup file found named %s' % upload_file)

    put(upload_file, '%(application_tmp_path)s/%(application_restore_filename)s' % env['application'])