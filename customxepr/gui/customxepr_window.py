# -*- coding: utf-8 -*-
"""
@author: Sam Schott  (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.

"""
import os
import platform
import logging
from PyQt5 import QtWidgets, uic

from customxepr.gui.manager_window import ManagerApp


_root = os.path.dirname(os.path.realpath(__file__))
logger = logging.getLogger(__name__)


# ======================================================================================
# Subclass of JobStatusApp exposing certain CustomXepr settings
# ======================================================================================

# noinspection PyArgumentList
class GridLayoutShortcuts(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)
        layout_file = "customxepr_panel.ui"
        uic.loadUi(os.path.join(_root, layout_file), self)

        if platform.system() == "Darwin":
            self.layout.setContentsMargins(20, 0, 20, 0)
        else:
            self.layout.setContentsMargins(20, 15, 20, 10)


class CustomXeprGuiApp(ManagerApp):

    """
    Subclass of :class:`ManagerApp` which adds controls for select CustomXepr settings.

    :param: :class:`main.CustomXepr` instance.
    """

    def __init__(self, customxepr):
        ManagerApp.__init__(self, customxepr.manager)
        self.customxepr = customxepr

        self.gridLayoutShortcuts = GridLayoutShortcuts()
        self.tabJobs.layout().addWidget(self.gridLayoutShortcuts)

        # get temperature control settings
        self.gridLayoutShortcuts.lineEditT_tolerance.setValue(
            self.customxepr.temperature_tolerance
        )
        self.gridLayoutShortcuts.lineEditT_settling.setValue(
            self.customxepr.temp_wait_time
        )
        self.gridLayoutShortcuts.lineEditT_tolerance.setMinimum(0)
        self.gridLayoutShortcuts.lineEditT_settling.setMinimum(0)

        # connect quick settings
        self.gridLayoutShortcuts.qValueButton.clicked.connect(self.on_qvalue_clicked)
        self.gridLayoutShortcuts.tuneButton.clicked.connect(self.on_tune_clicked)
        self.gridLayoutShortcuts.lineEditT_tolerance.valueChanged.connect(
            self.set_temperature_tolerance
        )
        self.gridLayoutShortcuts.lineEditT_settling.valueChanged.connect(
            self.set_t_settling
        )

    # ==================================================================================
    # Button callbacks
    # ==================================================================================

    def on_tune_clicked(self):
        """
        Schedules a tuning job if the ESR is connected.
        """

        if self.job_queue.has_queued():
            logger.info("Tuning job added to the job queue.")

        self.customxepr.customtune()

    def on_qvalue_clicked(self):
        """
        Schedules a Q-Value readout if the ESR is connected.
        """

        if self.job_queue.has_queued():
            logger.info("Q-Value readout added to the job queue.")

        self.customxepr.getQValueCalc()

    # ==================================================================================
    # Callbacks and functions for CustomXepr settings adjustments
    # ==================================================================================

    def set_temperature_tolerance(self, value):
        self.customxepr.temperature_tolerance = value

    def set_t_settling(self, value):
        self.customxepr.temp_wait_time = value
