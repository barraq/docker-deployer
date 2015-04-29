import os

from fabric.api import lcd, task, local, env
from fabric.contrib.console import confirm


@task
def cache():
    """Clean cache in current project"""
    if confirm('\nRemove all content from $(project_cache_path). Do you want to continue?' % env['project'],
               default=False):
        with lcd(env['project']['project_cache_path']):
            local('rm -rf *')