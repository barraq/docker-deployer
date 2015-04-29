from .. import utils

from fabric.api import task, env
from deployer.fabric.settings import get_settings


@task
def stage(name, new_settings={}):
    """Set working environment: staging, production.

    Usage:

        fab env:production deploy
        fab env:staging deploy
    """
    env.update(get_settings(name, env, new_settings))
    env.environment = name