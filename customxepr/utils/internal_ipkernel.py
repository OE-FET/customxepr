# -*- coding: utf-8 -*-
"""
@author: Sam Schott  (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.

"""

# system imports
from __future__ import absolute_import, print_function
from ipykernel.connect import connect_qtconsole
from ipykernel.kernelapp import IPKernelApp


def create_ip_kernel(gui, banner):
    """
    Launch and return an IPython kernel with matplotlib support for the
    desired gui.
    """
    kernel = IPKernelApp.instance()
    kernel.initialize(['python', '-m', 'CustomXeprKernel',
                       '--matplotlib=%s' % gui])
    kernel.shell.banner1 = banner
    return kernel


class InternalIPKernel(object):

    def __init__(self, backend='qt', banner=''):
        # Start IPython kernel
        self.ipkernel = create_ip_kernel(backend, banner)
        self.consoles = []  # To create and track active qt consoles

        # get namespace of kernel
        self.namespace = self.ipkernel.shell.user_ns

    def send_to_namespace(self, dictionary):
        """
        Pushes variables from dictionary to kernel name space. Replaces
        variables if they already exists.
        """
        self.namespace.update(dictionary)

    def new_qt_console(self, style=''):
        """
        Start a new qtconsole connected to our kernel.
        """
        arglist = ['--gui-completion', 'droplist',
                   '--style', style,
                   '--JupyterWidget.banner=""',
                   '--JupyterWidget.font_family="SF Mono"',
                   ]
        return connect_qtconsole(self.ipkernel.abs_connection_file,
                                 profile=self.ipkernel.profile, argv=arglist)

    def cleanup_consoles(self):
        for c in self.consoles:
            c.kill()
