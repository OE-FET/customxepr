# system imports
from __future__ import unicode_literals, absolute_import
from IPython.lib.kernel import connect_qtconsole
from ipykernel.kernelapp import IPKernelApp


def mpl_kernel(gui, banner):
    """Launch and return an IPython kernel with matplotlib support for the
    desired gui
    """
    kernel = IPKernelApp.instance()
    kernel.initialize(['python', '-m', 'CustomXeprKernel',
                       '--matplotlib=%s' % gui])
    kernel.shell.banner1 = banner
    return kernel


class InternalIPKernel(object):

    def init_ipkernel(self, backend='qt', banner=''):
        # Start IPython kernel with GUI event loop and mpl support
        self.ipkernel = mpl_kernel(backend, banner)
        # To create and track active qt consoles
        self.consoles = []

        # This application will also act on the shell user namespace
        self.namespace = self.ipkernel.shell.user_ns

    def send_to_namespace(self, dictionary, evt=None):
        """Pushed variables from dictionary to kernel name space. Replaces
        variables if they already exists.
        """
        self.namespace.update(dictionary)

    def new_qt_console(self, evt=None, style=''):
        """start a new qtconsole connected to our kernel"""
        return connect_qtconsole(self.ipkernel.abs_connection_file,
                                 profile=self.ipkernel.profile,
                                 argv=['--gui-completion', 'droplist',
                                       '--style', style,
                                       '--JupyterWidget.banner=""'])

    def cleanup_consoles(self, evt=None):
        for c in self.consoles:
            c.kill()
