import pprint

from fabric.state import env
from fabric.decorators import task
from fabric.operations import require

from deployer.fabric.tasks import stage
from deployer.fabric import defaults as DEFAULTS


__all__ = ['deployer', 'full']


@task
def deployer(branch='master'):
    """Show deployer environment settings"""
    require('environment', provided_by=[stage])

    for section in DEFAULTS.BASE_CONFIG_PARSER_SECTIONS:
        print('# %s' % section)
        for key, val in env[section].items():
            print('  - %s = %s' % (key, val))


@task
def full(branch='master'):
    """Show full environment settings (deployer together with Fabric)"""
    require('environment', provided_by=[stage])

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(env)