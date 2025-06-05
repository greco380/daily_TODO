from __future__ import annotations

import time
import logging
from typing import Callable

import schedule

logger = logging.getLogger(__name__)


def schedule_daily(time_str: str, job: Callable[[], None]):
    """Schedule a job to run daily at time_str."""
    schedule.every().day.at(time_str).do(job)
    logger.info("Scheduled daily job at %s", time_str)


def run_pending():
    """Run pending scheduled jobs."""
    while True:
        schedule.run_pending()
        time.sleep(1)
