from __future__ import annotations

import smtplib
from email.message import EmailMessage
import logging

from .config import EmailSettings

logger = logging.getLogger(__name__)


def send_email(settings: EmailSettings, subject: str, body: str):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.username
    msg["To"] = settings.recipient
    msg.set_content(body)

    try:
        with smtplib.SMTP(settings.smtp_server, settings.smtp_port) as server:
            server.starttls()
            if settings.username:
                server.login(settings.username, settings.password)
            server.send_message(msg)
        logger.info("Email sent to %s", settings.recipient)
    except Exception as exc:
        logger.error("Failed to send email: %s", exc)
