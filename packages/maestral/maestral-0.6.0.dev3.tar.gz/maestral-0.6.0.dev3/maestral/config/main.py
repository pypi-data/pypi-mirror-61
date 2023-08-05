# -*- coding: utf-8 -*-
#
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
# (see spyder/__init__.py for details)

"""
Maestral configuration options

Note: The 'account' section is used for internal purposes only to store some
basic information on the user account between connections. The 'internal'
section saves cursors and time-stamps for the last synced Dropbox state and
local state, respectively. Resetting those to the default values will trigger
a full download on the next startup.
"""

import os
import copy
from .user import UserConfig
from .base import get_conf_path


PACKAGE_NAME = os.getenv('MAESTRAL_CONFIG', 'maestral')
SUBFOLDER = 'maestral'


# =============================================================================
#  Defaults
# =============================================================================

DEFAULTS = [
    ('main',  # main settings regarding folder locations etc
     {
         'path': '',  # dropbox folder location (parent folder)
         'default_dir_name': 'Dropbox ({})',  # default dropbox folder name
         'excluded_folders': [],  # folders excluded from sync
         'excluded_files': [],  # files excluded from sync, currently not supported
     }
     ),
    ('account',  # info on linked Dropbox account, periodically updated from servers
     {
         'account_id': '',
         'email': '',
         'display_name': '',
         'abbreviated_name': '',
         'type': '',
         'usage': '',
         'usage_type': '',
     }
     ),
    ('app',  # app settings
     {
         'notification_level': 15,  # desktop notifications for file changes
         'log_level': 20,  # log level for file log, defaults to INFO
         'update_notification_last': 0.0,  # last notification about updates
         'update_notification_interval': 60*60*24*7,  # interval to check for updates, sec
         'latest_release': '0.0.0',  # latest available release
         'analytics': False,  # automatically report crashes and errors with bugsnag
     }
     ),
    ('internal',  # saved sync state
     {
         'cursor': '',  # remote cursor: represents last state synced from Dropbox
         'lastsync': 0.0,  # local cursor: time-stamp of last upload
         'recent_changes': [],  # cached list of recent changes to display in GUI
     }
     ),
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
CONF_VERSION = '10.0.0'


class MaestralConfig:
    """Singleton config instance for Maestral"""

    _instances = {}

    def __new__(cls, config_name):
        """
        Create new instance for a new config name, otherwise return existing instance.
        """

        if config_name in cls._instances:
            return cls._instances[config_name]
        else:
            defaults = copy.deepcopy(DEFAULTS)
            # set default dir name according to config
            for sec, options in defaults:
                if sec == 'main':
                    options['default_dir_name'] = f'Dropbox ({config_name.title()})'

            path = get_conf_path('maestral', create=True)
            try:
                conf = UserConfig(
                    path, config_name, defaults=defaults, version=CONF_VERSION, load=True,
                    backup=True, raw_mode=True, remove_obsolete=True
                )
            except OSError:
                conf = UserConfig(
                    path, config_name, defaults=defaults, version=CONF_VERSION, load=False,
                    backup=True, raw_mode=True, remove_obsolete=True
                )

            conf._name = config_name

            cls._instances[config_name] = conf
            return conf
