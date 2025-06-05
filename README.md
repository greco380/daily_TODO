# Daily TODO

Utilities to collect tasks and calendar events from multiple services, summarize
with OpenAI, and send a daily email summary. This repository contains sample
modules for integrating with Google Calendar, Trello, and Asana, aggregating
results, summarizing with the OpenAI API, and formatting the output for email
delivery.

## Configuration

1. Copy `config.example.yml` to `config.yml` in the project root.
2. Edit the copied file and fill in your service credentials, API keys and
   preferred delivery time.

API keys such as `openai_api_key`, `trello_api_key`, and `asana_access_token`
should be kept secret. Store them in environment variables or a secrets manager
and reference them in `config.yml` if desired.
