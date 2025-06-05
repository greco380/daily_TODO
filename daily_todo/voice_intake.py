from __future__ import annotations

import io
import logging
from typing import List

import openai

logger = logging.getLogger(__name__)


def transcribe_audio(audio_bytes: bytes, api_key: str) -> str:
    """Transcribe audio using OpenAI Whisper API."""
    openai.api_key = api_key
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = "audio.wav"
    try:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript["text"]
    except Exception as exc:
        logger.error("Transcription failed: %s", exc)
        return ""


def extract_tasks(transcription: str, api_key: str) -> List[str]:
    """Extract actionable tasks using OpenAI."""
    prompt = (
        "From this transcription, extract a list of actionable tasks the speaker "
        "implied they want to or have to do today. Return only a bullet list."
    )
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": transcription},
        ],
    )
    text = response["choices"][0]["message"]["content"].strip()
    return [line.strip("- ") for line in text.splitlines() if line.strip()]
