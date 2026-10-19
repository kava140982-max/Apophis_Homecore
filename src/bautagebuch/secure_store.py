"""Encrypted-at-rest append-only local store.

Requires the optional `cryptography` package. It fails closed when unavailable.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import secrets
import tempfile
from pathlib import Path
from typing import Any

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
except ImportError:  # pragma: no cover
    AESGCM = None


class SecureStore:
    def __init__(self, path: Path, key: bytes):
        if AESGCM is None:
            raise RuntimeError("cryptography is required for encrypted local persistence")
        if len(key) not in (16, 24, 32):
            raise ValueError("AES-GCM key must be 128, 192 or 256 bits")
        self.path = path
        self.key = key
        self.path.parent.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def load_or_create_key(path: Path) -> bytes:
        if path.exists():
            if path.stat().st_mode & 0o077:
                raise PermissionError("key file permissions must be 0600")
            raw = path.read_bytes()
            if len(raw) != 32:
                raise ValueError("key file must contain exactly 32 bytes")
            return raw
        path.parent.mkdir(parents=True, exist_ok=True)
        raw = secrets.token_bytes(32)
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "wb") as f:
            f.write(raw)
        return raw

    def _read(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"version": 1, "records": [], "chain_head": "0" * 64}
        blob = json.loads(self.path.read_text(encoding="ascii"))
        nonce = base64.b64decode(blob["nonce"])
        ciphertext = base64.b64decode(blob["ciphertext"])
        plain = AESGCM(self.key).decrypt(nonce, ciphertext, b"KaVa-Bautagebuch-v1")
        return json.loads(plain.decode("utf-8"))

    def _write(self, data: dict[str, Any]) -> None:
        plain = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
        nonce = secrets.token_bytes(12)
        ciphertext = AESGCM(self.key).encrypt(nonce, plain, b"KaVa-Bautagebuch-v1")
        payload = {"version": 1, "nonce": base64.b64encode(nonce).decode(), "ciphertext": base64.b64encode(ciphertext).decode()}
        fd, tmp = tempfile.mkstemp(prefix=".secure-store-", dir=self.path.parent)
        try:
            with os.fdopen(fd, "w", encoding="ascii") as f:
                json.dump(payload, f, separators=(",", ":")); f.flush(); os.fsync(f.fileno())
            os.chmod(tmp, 0o600); os.replace(tmp, self.path)
        finally:
            if os.path.exists(tmp): os.unlink(tmp)

    def append(self, kind: str, actor: str, payload: dict[str, Any]) -> str:
        data = self._read()
        payload_json = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        payload_hash = hashlib.sha256(payload_json.encode()).hexdigest()
        previous = data["chain_head"]
        event_hash = hashlib.sha256(f"{previous}|{kind}|{actor}|{payload_hash}".encode()).hexdigest()
        record = {"id": secrets.token_hex(16), "kind": kind, "actor": actor, "payload": payload, "payload_hash": payload_hash, "prev_hash": previous, "event_hash": event_hash}
        data["records"].append(record); data["chain_head"] = event_hash
        self._write(data)
        return record["id"]

    def records(self) -> list[dict[str, Any]]:
        return self._read()["records"]

    def verify(self) -> bool:
        data = self._read(); previous = "0" * 64
        for record in data["records"]:
            payload_json = json.dumps(record["payload"], ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            ph = hashlib.sha256(payload_json.encode()).hexdigest()
            expected = hashlib.sha256(f"{previous}|{record['kind']}|{record['actor']}|{ph}".encode()).hexdigest()
            if record["prev_hash"] != previous or record["payload_hash"] != ph or record["event_hash"] != expected:
                return False
            previous = expected
        return previous == data["chain_head"]
