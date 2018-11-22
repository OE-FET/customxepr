#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 20:19:41 2016

@author: Sam Schott (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.

"""
from __future__ import division, absolute_import, unicode_literals
import logging.handlers
import smtplib
import string
from email.utils import formatdate
from email.message import Message


class TlsSMTPHandler(logging.handlers.SMTPHandler):
    """
    Logging handler which sends out emails.
    Extemnds SMTPHandler from logging package with TLS support.
    """

    def emit(self, record):
        """
        Emit a record.

        Format the record and send it to the specified addressees.
        """
        try:
            port = self.mailport
            if not port:
                port = smtplib.SMTP_PORT
            smtp = smtplib.SMTP(self.mailhost, port)
            log_msg = self.format(record)
            msg = u'From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s' % (
                            self.fromaddr, string.join(self.toaddrs, ","),
                            self.getSubject(record), formatdate(), log_msg
                            )
            if self.username:
                smtp.starttls()
                smtp.ehlo()
                smtp.login(self.username, self.password)
            smtp.sendmail(self.fromaddr, self.toaddrs, msg.encode('utf-8'))
            smtp.quit()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            pass


class EmailSender(object):
    """ Logging handler which sends out emails."""

    def __init__(self, fromaddr, mailhost, port=None, username=None, password=None, standby=False):
        self.fromaddr = fromaddr
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
                self.smtpstarttls()
                self.smtpehlo()
                self.smtplogin(self.username, self.password)

    def __del__(self):
        """
        Quit mailserver when instance is deleted.

        This gets called when the instance is garbage-collected, even for instances where __init__
        failed with an exception. We therefore need to insure that attributes have been created.
        """

        if hasattr(self, 's') and hasattr(self, 'standby'):
            if not self.standby:
                self.smtp.quit()

    def create_email(self, toaddrs, subject, body):
        """Compose email form main body, subject and email addresses."""

        msg = u'From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s' % (
                self.fromaddr, string.join(toaddrs, ","),
                subject, formatdate(), body
                )

        return msg

    def sendmail(self, toaddrs, subject, body):

        msg = self.create_email(toaddrs, subject, body)

        if not self.standby:
            self.smtp = smtplib.SMTP(self.mailhost, self.port)
            if self.username:
                self.smtpstarttls()
                self.smtpehlo()
                self.smtplogin(self.username, self.password)

        self.smtp.sendmail(self.fromaddr, toaddrs, msg.encode('utf-8'))

        if not self.standby:
            self.smtpquit()
