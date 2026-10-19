"""Small, local-only command line for KaVa Workspace Free."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from .secure_store import SecureStore
from .workspace import WorkspaceService

ALLOWED = {"note", "task", "file_ref"}

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="kava-free", description="Lokale Notizen, Aufgaben und Dateiverweise")
    parser.add_argument("--store", type=Path, default=Path("data/kava-free.bin"))
    parser.add_argument("--key", type=Path, default=Path("private/kava-free.key"))
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add", help="Notiz, Aufgabe oder Dateiverweis speichern")
    add.add_argument("kind", choices=sorted(ALLOWED)); add.add_argument("title"); add.add_argument("text")
    sub.add_parser("list", help="Gespeicherte Einträge anzeigen")
    sub.add_parser("check", help="Verschlüsselten Speicher prüfen")
    args = parser.parse_args(argv)
    vault = SecureStore(args.store, SecureStore.load_or_create_key(args.key))
    service = WorkspaceService(vault)
    if args.command == "add":
        print("Eintrag gespeichert:", service.add_item(args.kind, args.title, {"text": args.text}))
    elif args.command == "list":
        for row in service.list_items():
            payload = row["payload"]
            if payload.get("kind") in ALLOWED:
                print(f"- {payload['kind']}: {payload['title']} — {payload.get('content', {}).get('text', '')}")
    else:
        print("Speicherprüfung erfolgreich." if service.verify() else "Speicherprüfung fehlgeschlagen.")
        return 0 if service.verify() else 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
