#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 16:59:21 2018

@author: SamSchott
"""
import os
import subprocess


def ping(ipAddress, ms_timeout=20):
    """
    Ping command for UNIX based systems. Millisecond timeout will only work
    if fping is installed. Returns True if IP address is reachable within
    timeout.
    """
    # check if fping is installed, otherwise use ping
    if os.system('which fping 2>&1 >/dev/null') == 0:
        command = 'fping'
        options = '-c 1 -t %i' % round(ms_timeout)
    else:
        sec_timeout = max(1, ms_timeout/1000)
        command = 'ping'
        options = '-c 1 -t %i ' % int(sec_timeout)

    return subprocess.call([command, options, ipAddress]) == 0
