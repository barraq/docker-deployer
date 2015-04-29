"""
Global configuration
"""
import configparser

from .fabric import defaults as DEFAULTS

config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())

for section in DEFAULTS.BASE_CONFIG_PARSER_SECTIONS:
    config.add_section(section)