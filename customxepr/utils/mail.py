#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 20:19:41 2016

@author: Sam Schott (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.

"""
from __future__ import division, absolute_import, unicode_literals
import smtplib
from email.utils import formatdate


class EmailSender(object):
    """ Logging handler which sends out emails."""

    def __init__(self, fromaddr, mailhost, displayname=None, port=None,
                 username=None, password=None, standby=False):
        self.fromaddr = fromaddr
        if displayname is not None:
            self.displayname = '%s <%s>' % (displayname, fromaddr)
        else:
            self.displayname = fromaddr

        self.mailhost = mailhost
        if port:
            self.port = port
        else:
            self.port = 25
        self.username = username
        self.password = password

        self.standby = standby

        if self.standby:
            self.smtp = smtplib.SMTP(self.mailhost, self.port)
            if self.username:
                self.smtp.starttls()
                self.smtp.ehlo()
                self.smtp.login(self.username, self.password)

    def __del__(self):
        """
        Quit mail server when instance is deleted.

        This gets called when the instance is garbage-collected, even for
        instances where __init__ failed with an exception. We therefore need to
        insure that attributes have been created.
        """

        if hasattr(self, 's') and hasattr(self, 'standby'):
            if not self.standby:
                self.smtp.quit()

    def create_email(self, toaddrs, subject, body):
        """Compose email form main body, subject and email addresses."""

        msg = u"""From: {0}\r\nTo: {1}\r\nSubject: {2}\r\nDate: {3}\r\n\r\n{4}""".format(
                self.displayname, ",".join(toaddrs), subject, formatdate(), body
                )

        return msg

    def sendmail(self, toaddrs, subject, body):

        msg = self.create_email(toaddrs, subject, body)

        if not self.standby:
            self.smtp = smtplib.SMTP(self.mailhost, self.port)
            if self.username:
                self.smtp.starttls()
                self.smtp.ehlo()
                self.smtp.login(self.username, self.password)

        self.smtp.sendmail(self.fromaddr, toaddrs, msg.encode('utf-8'))

        if not self.standby:
            self.smtp.quit()
