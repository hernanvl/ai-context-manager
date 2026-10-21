"""Loads settings from the .env file in the project root."""
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")


def _require(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing {name} in .env")
    return value


SUPABASE_URL = _require("SUPABASE_URL")
SUPABASE_SERVICE_KEY = _require("SUPABASE_SERVICE_KEY")
GROQ_API_KEY = _require("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
COMPRESSION_THRESHOLD_TOKENS = int(os.getenv("COMPRESSION_THRESHOLD_TOKENS", "6000"))

# How many recent messages are sent to the LLM as short-term memory
RECENT_MESSAGES = 20

SYSTEM_PROMPT = (
    "You are a context-preserving AI assistant. Your task is to maintain project "
    "continuity across conversations. Use the provided project context when relevant, "
    "and answer clearly and concisely."
)
