# coding: utf-8
import os
from concrete_mailer.preparers import prepare_email
from concrete_mailer.utils import get_connection
from smtplib import SMTPException
import logging


logger = logging.getLogger('concrete-mailer')


class EmailSenderClient:
    def __init__(self, **kwargs):
        self.email_host = kwargs.get(
            'email_host', os.environ.get('EMAIL_HOST', '')
        )
        self.email_port = kwargs.get(
            'email_port', os.environ.get('EMAIL_PORT', '')
        )
        self.email_host_user = kwargs.get(
            'email_host_user', os.environ.get('EMAIL_HOST_USER', '')
        )
        self.email_host_password = kwargs.get(
            'email_host_password', os.environ.get('EMAIL_HOST_PASSWORD', '')
        )
        self.use_tls = kwargs.get(
            'use_tls', os.environ.get('SMTP_USE_TLS') == '1'
        )

    def send(
        self,
        context,
        template,
        title,
        dests,
        sender_name,
        sender_email,
        reply_to=None,
        attachments=None,
    ):
        try:
            connection = get_connection(
                host=self.email_host,
                port=self.email_port,
                user=self.email_host_user,
                password=self.email_host_password,
                use_tls=self.use_tls,
            )
        except SMTPException as e:
            logger.info('Failed to establish connection: {}'.format(e))
            return False
        email = prepare_email(
            context=context,
            css='',
            html=template,
            title=title,
            sender='{sender_name} <{sender_email}>'.format(
                sender_name=sender_name, sender_email=sender_email
            ),
            recipients=dests,
            reply_to=reply_to,
            smtp_connection=connection,
            attachments=attachments,
        )
        try:
            return email.send()
        except Exception as e:
            logger.info('Failed to send email: {}'.format(e))
            return False
