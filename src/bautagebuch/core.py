"""Hilfsfunktionen für die eingeschränkte KaVa Workspace Ausgabe."""
from __future__ import annotations
import re
from typing import Any

MAX_TEXT = 20_000
_SECRET_PATTERNS = (
    re.compile(r"(?i)bearer\s+[A-Za-z0-9._~-]+"),
    re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*[^\s,;]+"),
)

def redact(value: str) -> str:
    for pattern in _SECRET_PATTERNS:
        value = pattern.sub("[REDACTED]", value)
    return value

def validate_text(value: Any, *, field: str = "text") -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a string")
    if len(value) > MAX_TEXT:
        raise ValueError(f"{field} exceeds {MAX_TEXT} characters")
    if "\x00" in value:
        raise ValueError(f"{field} contains NUL")
    return value
