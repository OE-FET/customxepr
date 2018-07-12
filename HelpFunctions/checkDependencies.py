#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 12:38:00 2018

@author: samschott
"""

from pkgutil import iter_modules

def check_dependencies(filePath):
    exit_code = 0
    modules = set(x[1] for x in iter_modules())
    with open(filePath, 'rb') as f:
        for line in f:
            requirement = line.rstrip()
            if not requirement in modules:
                print('Error: Could not find module ' + requirement + '. ' +
                      'Please install to run CustomXepr.')
                exit_code +=1
    
    return exit_code