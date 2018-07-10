#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 20:19:41 2016

@author: Sam Schott (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.

"""


def SendEmail(TO='ss2151@cam.ac.uk', FROM='"Sam Schott" <ss2151@cam.ac.uk>',
              HOST='localhost', USER=None, PASS=None, SUBJECT='Test',
              MESSAGE=''):

        try:
            import smtplib
            import string  # for tls add this line
            try:
                from email.utils import formatdate
            except ImportError:
                pass
            port = smtplib.SMTP_PORT
            smtp = smtplib.SMTP(HOST, port)
            msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s" % (
                            FROM, string.join(TO, ","), SUBJECT, formatdate(),
                            MESSAGE)
            if USER:
                smtp.ehlo()  # for tls add this line
                smtp.starttls()  # for tls add this line
                smtp.ehlo()  # for tls add this line
                smtp.login(USER, PASS)
            smtp.sendmail(FROM, TO, msg)
            smtp.quit()
        except (KeyboardInterrupt, SystemExit):
            raise
