# system imports
from __future__ import absolute_import
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

        # This application will also act on the shell user namespace
        self.namespace = self.ipkernel.shell.user_ns

    def send_to_namespace(self, dictionary):
        """
        Pushes variables from dictionary to kernel name space. Replaces
        variables if they already exists.
        """
        self.namespace.update(dictionary)

    def new_qt_console(self, style=''):
        """start a new qtconsole connected to our kernel"""
        return connect_qtconsole(self.ipkernel.abs_connection_file,
                                 profile=self.ipkernel.profile,
                                 argv=['--gui-completion', 'droplist',
                                       '--style', style,
                                       '--JupyterWidget.banner=""'])

    def cleanup_consoles(self):
        for c in self.consoles:
            c.kill()
