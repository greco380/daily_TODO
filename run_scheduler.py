import logging

from daily_todo import config, scheduler
from daily_todo.main import run_daily_summary


logging.basicConfig(level=logging.INFO)


def main() -> None:
    cfg = config.load_config()
    scheduler.schedule_daily(cfg.delivery_time, lambda: run_daily_summary(cfg))
    scheduler.run_pending()


if __name__ == "__main__":
    main()
