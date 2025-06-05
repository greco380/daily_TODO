from __future__ import annotations

from typing import List, Dict

import openai


PROMPT = (
    "Summarize and prioritize the following tasks and meetings for today."
    " Return the summary in natural language, highlighting the most important"
    " items first."
)


def summarize(data: List[Dict], api_key: str) -> str:
    """Send aggregated items to OpenAI API for summarization."""
    openai.api_key = api_key
    text = "\n".join(f"- {item['title']} ({item['due']})" for item in data)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": text},
        ],
    )
    return response["choices"][0]["message"]["content"].strip()
