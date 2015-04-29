import os

DEPLOYER_LIB_ROOT = os.path.dirname(os.path.dirname(__file__))

BASE_CONFIG_PARSER_SECTIONS = ['deployer', 'application', 'project', 'docker']
BASE_SERVICE_MOUNT_VOLUMES = ['backup']
BASE_SERVICE_ENV_CONFIG_DIR = os.path.join('config', 'env')
