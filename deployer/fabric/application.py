"""
Module providing easy API for working with applications.
"""

import re
from deployer.fabric import defaults as DEFAULTS


def get_application_maintenance_tasks_commands(context):
    """Return available maintenance task commands.

    Returns the command as string if `application_maintenance_tasks_command` is defined,
    otherwise a dictionary of { 'name': 'command' }
    """
    if 'application_maintenance_tasks_command' in context['application']:
        return context['application']['application_maintenance_tasks_command']
    else:
        commands = {}
        cmd_re = re.compile('^application_maintenance_tasks_(?P<name>[\w-]+)_command')
        for key in filter(cmd_re.match, context['application'].keys()):
            commands[cmd_re.match(key).group('name')] = context['application'][key]
        return commands


def get_application_mount_volumes(context):
    if 'application_extra_volumes' in context['application']:
        return [v.strip() for v in context['application']['application_extra_volumes'].split(',')] + DEFAULTS.BASE_SERVICE_MOUNT_VOLUMES
    else:
        return DEFAULTS.BASE_SERVICE_MOUNT_VOLUMES