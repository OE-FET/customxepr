from __future__ import division, absolute_import, unicode_literals
import os
on_rtd = os.environ.get('READTHEDOCS') == 'True'
if not on_rtd:
    from customxepr.startup import run
from customxepr.main import CustomXepr
from customxepr.xepr_dataset import XeprData, XeprParam
from customxepr.manager import queued_exec