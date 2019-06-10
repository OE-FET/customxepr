# -*- coding: utf-8 -*-
"""
@author: Sam Schott  (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.

"""
from __future__ import division, absolute_import, unicode_literals
import os
from enum import Enum


class SupportedImplementation(Enum):
    notify_send = 'notify-send'
    osascript = 'osascript'


class Notipy(object):
    """Send native OS notifications to user.

    Relies on AppleScript on macOS and notify-send on linux, otherwise
    falls back to stdout."""

    enabled = True

    def __init__(self):
        self.implementation = self.__get_available_implementation()

    def send(self, message, title="CustomXepr"):
        if self.enabled:
            self.__send_message(message, title)
        else:
            pass

    def __send_message(self, message, title=""):
        if self.implementation == SupportedImplementation.osascript:
            os.system("osascript -e 'display notification \"{}\" with title \"{}\"'".format(
                message, title))
        elif self.implementation == SupportedImplementation.notify_send:
            os.system('notify-send "{}" "{}"'.format(title, message))
        else:
            print('{}: {}'.format(title, message))

    @staticmethod
    def __command_exists(command):
        return any(
            os.access(os.path.join(path, command), os.X_OK)
            for path in os.environ["PATH"].split(os.pathsep)
        )

    def __get_available_implementation(self):
        if self.__command_exists('osascript'):
            return SupportedImplementation.osascript
        elif self.__command_exists('notify-send'):
            return SupportedImplementation.notify_send
        return None
