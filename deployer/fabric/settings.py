"""
Module providing easy API for working with settings.
"""

import os
import configparser

from deployer.configmanager import config
from deployer.fabric import defaults as DEFAULTS
from deployer.fabric.application import get_application_mount_volumes


def get_settings(stage, env, extra={}):
    """Return settings for a given `stage` and `extra` arguments"""

    # load predefined deployer environment settings
    config.read(os.path.join(DEFAULTS.DEPLOYER_LIB_ROOT, 'config', 'env', 'defaults.cfg'))

    # load shared environment settings if any
    try:
        if config.has_option('deployer', 'shared_env_dir'):
            for name in ['defaults', stage]:
                config_file = os.path.join(config.get('deployer', 'shared_env_dir'), '%s.cfg' % name)
                if os.path.exists(config_file):
                    config.read(config_file)
    except configparser.Error:
        pass

    project_root = __get_application_project_root(env)

    # load service environment settings
    for name in ['defaults', stage]:
        config_file = os.path.join(project_root, DEFAULTS.BASE_SERVICE_ENV_CONFIG_DIR, '%s.cfg' % name)
        if os.path.exists(config_file):
            config.read(config_file)

    settings = {}

    # build up settings from configuration files
    for section in config.sections():
        if section == 'fabric':
            settings.update(dict(config.items(section)))
        else:
            settings[section] = {}
            for key, val in config.items(section):
                settings[section][key] = val

    # extend settings
    __extend_settings(settings, env)

    return settings


def __extend_settings(settings, env):
    """Extend settings with additional properties"""
    project_root = __get_application_project_root(env)

    # set non-overridable properties
    settings['project']['project_root'] = project_root

    # define project paths
    for item in ['project_repo', 'project_cache', 'project_shared', 'project_backup', 'project_restore']:
        settings['project']['%s_path' % item] = os.path.join(project_root, settings['project']['%s_dir' % item])

    # define service_mount paths
    for volume in get_application_mount_volumes(settings):
        settings['application']['application_%s_volume_path' % volume] = os.path.join(settings['application']['application_mount_path'], volume)


def __get_application_project_root(context):
    """Return application project root from a given `context"""
    return os.path.dirname(context['real_fabfile'])


























