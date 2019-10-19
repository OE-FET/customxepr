# -*- coding: utf-8 -*-
#
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
# (see spyder/__init__.py for details)

"""
CustomXepr configuration options

Note: Leave this file free of Qt related imports, so that it can be used to
quickly load a user config file
"""
import getpass

# local imports
from customxepr.config.user import UserConfig

PACKAGE_NAME = 'CustomXepr'
SUBFOLDER = '.%s' % PACKAGE_NAME


# =============================================================================
#  Defaults
# =============================================================================
DEFAULTS = [
            ('Window',
             {
              'x': 0,
              'y': 0,
              'width': 1024,
              'height': 650,
              'auto_plot_results': True
              }),
            ('CustomXepr',
             {
              'notify_address': [getpass.getuser() + '@cam.ac.uk', ],
              'email_handler_level': 30,
              'temp_wait_time': 120,
              'temperature_tolerance': 0.1
              }),
            ('SMTP',
             {
              'mailhost': 'smtp.office365.com',
              'port': 587,
              'fromaddr': 'customxepr@outlook.com',
              'credentials': ('customxepr@outlook.com', 'user@xepr'),
              'secure': None,
             }),
            ('Version',
             {'old_version': 'v2.2.1',
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
CONF_VERSION = '6.1.0'

# Main configuration instance
try:
    CONF = UserConfig('CustomXepr', defaults=DEFAULTS, load=True,
                      version=CONF_VERSION, subfolder=SUBFOLDER, backup=True,
                      raw_mode=True)
except Exception:
    CONF = UserConfig('CustomXepr', defaults=DEFAULTS, load=False,
                      version=CONF_VERSION, subfolder=SUBFOLDER, backup=True,
                      raw_mode=True)
