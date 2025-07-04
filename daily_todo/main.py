from __future__ import annotations

import logging

from . import config
from .integrations.google_calendar import get_today_events
from .integrations.trello import get_tasks_due_today as trello_tasks
from .integrations.asana import get_tasks_due_today as asana_tasks
from .aggregator import aggregate
from .llm import summarize
from .email_formatter import format_email
from .email_dispatch import send_email

DEFAULT_SUBJECT = "Daily Summary"

logger = logging.getLogger(__name__)


def run_daily_summary(cfg: config.UserConfig):
    items = []
    if cfg.google_credentials_path:
        items.append(get_today_events(cfg.google_credentials_path))
    if cfg.trello_api_key and cfg.trello_token:
        items.append(trello_tasks(cfg.trello_api_key, cfg.trello_token))
    if cfg.asana_access_token:
        items.append(asana_tasks(cfg.asana_access_token))

    merged = aggregate(items)
    summary = summarize(merged, cfg.openai_api_key)
    email_body = format_email(summary, merged)
    logger.info("Generated email:\n%s", email_body)
    subject = DEFAULT_SUBJECT
    try:
        send_email(cfg.email, subject, email_body)
    except Exception:
        logger.exception("Error sending email")


if __name__ == "__main__":
    cfg = config.load_config()
    run_daily_summary(cfg)
