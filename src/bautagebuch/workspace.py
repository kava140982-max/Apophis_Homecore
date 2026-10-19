"""KaVa Workspace Core: one local place for structured personal work."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from .core import validate_text, redact
from .secure_store import SecureStore

ALLOWED_KINDS = {"note", "task", "file_ref", "calendar", "message", "contact", "ai_result"}

class WorkspaceService:
    def __init__(self, vault: SecureStore): self.vault = vault
    def add_item(self, kind: str, title: str, content: dict[str, Any], actor: str = "local-user") -> str:
        if kind not in ALLOWED_KINDS: raise ValueError("unsupported workspace item kind")
        validate_text(title, field="title")
        if not isinstance(content, dict) or len(content) > 100: raise ValueError("content must be an object with <=100 fields")
        safe = {k: redact(str(v)) if isinstance(v, str) else v for k, v in content.items()}
        return self.vault.append("workspace.item", actor, {"kind": kind, "title": title, "content": safe, "created_at": datetime.now(timezone.utc).isoformat()})
    def list_items(self, kind: str | None = None) -> list[dict[str, Any]]:
        rows = [r for r in self.vault.records() if r["kind"] == "workspace.item"]
        return [r for r in rows if kind is None or r["payload"].get("kind") == kind]
    def verify(self) -> bool: return self.vault.verify()
