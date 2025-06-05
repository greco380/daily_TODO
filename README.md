# Daily TODO

Utilities to collect tasks and calendar events from multiple services, summarize
with OpenAI, and send a daily email summary. This repository contains sample
modules for integrating with Google Calendar, Trello, and Asana, aggregating
results, summarizing with the OpenAI API, and formatting the output for email
delivery.

## Running the scheduler

1. Install dependencies with `pip install -r requirements.txt`.
2. Create a `config.yml` file containing your credentials and desired
   `delivery_time`.
3. Start the scheduler:

   ```bash
   python run_scheduler.py
   ```

The process loads your configuration, schedules `run_daily_summary` for the
specified delivery time, and keeps running to execute pending jobs each day.
