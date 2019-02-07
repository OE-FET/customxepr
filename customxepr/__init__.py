from __future__ import division, absolute_import
import os
on_rtd = os.environ.get('READTHEDOCS') == 'True'
if not on_rtd:
    from customxepr.startup import run
from customxepr.main import CustomXepr
from customxepr.main import queued_exec