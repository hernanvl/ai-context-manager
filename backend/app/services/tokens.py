"""Cheap token estimate (~4 characters per token) - good enough for triggers."""


def count_tokens(text: str) -> int:
    return max(1, len(text) // 4)
