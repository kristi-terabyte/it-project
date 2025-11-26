"""
Command-line interface for SmartNotes.
"""

from __future__ import annotations

import argparse
from textwrap import dedent

from .storage import NoteStorage


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="smartnotes",
        description="Мінімальний CLI для створення та пошуку нотаток.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=dedent(
            """\
            Приклади:
              python -m smartnotes.app add --title "Лаба" --body "Завершити звіт" --tags uni urgent
              python -m smartnotes.app list --tag uni
              python -m smartnotes.app search "звіт"
              python -m smartnotes.app delete <id>
            """
        ),
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Створити нову нотатку")
    add_parser.add_argument("--title", required=True)
    add_parser.add_argument("--body", required=True)
    add_parser.add_argument("--tags", nargs="*", default=[])

    list_parser = subparsers.add_parser("list", help="Вивести всі нотатки")
    list_parser.add_argument("--tag", help="Фільтр за тегом")

    search_parser = subparsers.add_parser("search", help="Пошук за ключовим словом")
    search_parser.add_argument("keyword")

    delete_parser = subparsers.add_parser("delete", help="Видалити нотатку за ID")
    delete_parser.add_argument("note_id")

    return parser


def render_notes(notes):
    if not notes:
        print("Нотаток не знайдено.")
        return
    for note in notes:
        header = f"[{note.id}] {note.title} ({', '.join(note.tags) or 'без тегів'})"
        print(header)
        print("-" * len(header))
        print(note.body)
        print(f"Створено: {note.created_at}")
        print()


def main() -> None:
    storage = NoteStorage()
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "add":
        note = storage.add_note(args.title, args.body, args.tags)
        print(f"✅ Створено нотатку {note.id}")
    elif args.command == "list":
        render_notes(storage.list_notes(tag=args.tag))
    elif args.command == "search":
        render_notes(storage.search(args.keyword))
    elif args.command == "delete":
        if storage.delete(args.note_id):
            print("🗑️  Нотатку видалено.")
        else:
            print("⚠️  Нотатку не знайдено.")


if __name__ == "__main__":
    main()

