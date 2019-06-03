# -*- coding: utf-8 -*-
"""
@author: Sam Schott  (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.

"""
from __future__ import division, absolute_import, unicode_literals
import sys
import smtplib

PY2 = sys.version[0] == '2'

if not PY2:  # in Python 3
    from email.message import EmailMessage
    from email.utils import localtime
    basestring = str
else:  # in Python 2
    from email.mime.text import MIMEText
    from email.utils import formatdate


class EmailSender(object):
    """
    Class to send plain text email notifications.

    Initialize the instance with the from address. To specify a non-standard SMTP port,
    use the (host, port) tuple format for the mailhost argument. To specify authentication
    credentials, supply a (username, password) tuple for the credentials argument. To
    specify the use of a secure protocol (TLS), pass in a tuple for the secure argument.
    This will only be used when authentication credentials are supplied. The tuple will be
    either an empty tuple, or a single-value tuple with the name of a keyfile, or a
    2-value tuple with the names of the keyfile and certificate file. (This tuple is
    passed to the `starttls` method).
    """

    def __init__(self, mailhost, fromaddr, credentials=None, secure=None):
        if isinstance(mailhost, (list, tuple)):
            self.mailhost, self.mailport = mailhost
        else:
            self.mailhost, self.mailport = mailhost, None
        if isinstance(credentials, (list, tuple)):
            self.username, self.password = credentials
        else:
            self.username = None
        self.fromaddr = fromaddr
        self.secure = secure

    def sendmail(self, toaddrs, subject, body):

        if isinstance(toaddrs, basestring):
            toaddrs = [toaddrs]

        try:
            if not PY2:
                port = self.mailport
                if not port:
                    port = smtplib.SMTP_PORT
                smtp = smtplib.SMTP(self.mailhost, port)
                msg = EmailMessage()
                msg['From'] = self.fromaddr
                msg['To'] = ','.join(toaddrs)
                msg['Subject'] = subject
                msg['Date'] = localtime()
                msg.set_content(body)
                if self.username:
                    if self.secure is not None:
                        smtp.ehlo()
                        smtp.starttls(*self.secure)
                        smtp.ehlo()
                    smtp.login(self.username, self.password)
                smtp.send_message(msg)
                smtp.quit()
            else:
                port = self.mailport
                if not port:
                    port = smtplib.SMTP_PORT
                smtp = smtplib.SMTP(self.mailhost, port)
                msg = MIMEText(body)
                msg['From'] = self.fromaddr
                msg['To'] = ','.join(toaddrs)
                msg['Subject'] = subject
                msg['Date'] = formatdate()
                if self.username:
                    if self.secure is not None:
                        smtp.ehlo()
                        smtp.starttls(*self.secure)
                        smtp.ehlo()
                    smtp.login(self.username, self.password)
                smtp.sendmail(self.fromaddr, toaddrs, msg.as_string())
                smtp.quit()
        except Exception:
            print('Could not send email.')
