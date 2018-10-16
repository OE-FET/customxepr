# -*- coding: utf-8 -*-
#
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
# (see spyder/__init__.py for details)

"""
MercuryGUI configuration options

Note: Leave this file free of Qt related imports, so that it can be used to
quickly load a user config file.

To add:
* More feed settings, such as refresh rate, etc?
"""
import getpass

# Local import
from config.user import UserConfig

PACKAGE_NAME = 'MercuryGUI'
SUBFOLDER = '.%s' % PACKAGE_NAME


# =============================================================================
#  Defaults
# =============================================================================
DEFAULTS = [
            ('Connection',
             {
              'MERCURY_ADDRESS': 'TCPIP0::172.20.91.43::7020::SOCKET',
              }),
            (
             'MercuryFeed',
             {
              'temperature_module': 0,
              'gasflow_module': 0,
              'heater_module': 0
              }),
            ]


# =============================================================================
# Config instance
# =============================================================================
# IMPORTANT NOTES:
# 1. If you want to *change* the default value of a current option, you need to
#    do a MINOR update in config version, e.g. from 3.0.0 to 3.1.0
# 2. If you want to *remove* options that are no longer needed in our codebase,
#    or if you want to *rename* options, then you need to do a MAJOR update in
#    version, e.g. from 3.0.0 to 4.0.0
# 3. You don't need to touch this value if you're just adding a new option
CONF_VERSION = '1.0.0'

# Main configuration instance
try:
    CONF = UserConfig('CustomXepr', defaults=DEFAULTS, load=True,
                      version=CONF_VERSION, subfolder=SUBFOLDER, backup=True,
                      raw_mode=True)
except Exception:
    CONF = UserConfig('CustomXepr', defaults=DEFAULTS, load=False,
                      version=CONF_VERSION, subfolder=SUBFOLDER, backup=True,
                      raw_mode=True)
