#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 19:30:53 2018

@author: samschott
"""
import os.path as osp
import pygments
import shutil


direct = osp.dirname(osp.realpath(__file__))


def install_dark_style():
    """Installs customxeprdark style to pygments style folder."""
    # find pygments path
    pygments_path = osp.dirname(pygments.__file__)
    style_path = osp.join(pygments_path, 'styles')

    # find current path
    source_path = osp.join(direct, 'customxeprdark.py')

    # copy customxeprdark.py to style_path
    shutil.copy2(source_path, style_path)


def get_dark_style():
    """
    Tries to get customxeprdark pygments sytle. if this fails, it tries to
    install the customxeprdark style in the current pygments folder.
    If this fails, it falls back to the 'native' pygments style.
    """
    try:
        pygments.styles.get_style_by_name('customxeprdark')
        console_style = 'customxeprdark'
    except pygments.util.ClassNotFound:
        try:
            install_dark_style()
            console_style = 'customxeprdark'
        except:
            console_style = 'native'

    return console_style
