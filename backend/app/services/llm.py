"""Thin wrapper around the Groq chat API."""
from groq import Groq

from app.config import GROQ_API_KEY, GROQ_MODEL

_client = Groq(api_key=GROQ_API_KEY)


def chat_completion(messages: list[dict], temperature: float = 0.4) -> str:
    response = _client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content or ""
