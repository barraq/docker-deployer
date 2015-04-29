import os

from fabric.operations import local
from fabric.contrib.console import confirm
from fabric.api import lcd, env, execute

from ..utils import exit


def clone_local_repo():
    """Clones the Git repository"""
    if (not os.path.exists('{project[project_repo_path]}'.format(**env)) or confirm(
            '\n{project[project_repo_path]} already exists. Do you want to continue?'.format(**env), default=False)):
        local('rm -rf {project[project_repo_path]}'.format(**env))
        local('git clone {application[repo_url]} {project[project_repo_path]}'.format(**env))
    else:
        exit('\nAborting.')


def checkout_local_repo(branch='master'):
    """Updates the Git repository and checks out the specified branch"""
    if not os.path.exists('{project[project_repo_path]}'.format(**env)):
        execute(clone_local_repo)
    with lcd(env['project']['project_repo_path']):
        local('git fetch')
        local('git checkout %s' % branch)
    local('chmod -R go=u,go-w {project[project_repo_path]}'.format(**env))