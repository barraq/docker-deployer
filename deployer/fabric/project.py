"""
Module providing easy API for working with project.
"""

import os


def get_project_shared_cache_for_version(context, version):
    return os.path.join(
        context['project']['project_cache_path'],
        context['project']['project_shared_dir'],
        version)