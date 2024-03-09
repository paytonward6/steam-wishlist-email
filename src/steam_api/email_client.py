from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Self
import logging
import smtplib


from .settings import Settings


class EmailClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.to_addresses = self.settings.to_addresses

        self.smtp = self.configure_smtp()

        self.smtp.login(self.settings.email_address, self.settings.email_password)

    @staticmethod
    def configure_smtp():
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()
        smtp.starttls()

        return smtp

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.smtp.__exit__(*_)

    def send_message(self, subject: str, text: str, subtype: str = "plain"):
        def _msg():
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg.attach(MIMEText(text, subtype))

            return msg

        self.smtp.sendmail(
            from_addr=self.settings.email_address,
            to_addrs=self.to_addresses,
            msg=_msg().as_string()
        )
