# SmartNotes CLI

Мінімальний консольний застосунок для керування нотатками в рамках лабораторної роботи №4.

## Можливості

- Додавання нотаток із тегами
- Перегляд усіх нотаток або фільтр за тегом
- Пошук за ключовими словами
- Видалення нотаток

## Встановлення

```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows PowerShell
pip install -r requirements.txt  # якщо зʼявляться залежності
```

## Використання

### CLI

```bash
python -m smartnotes.app add --title "Звіт" --body "Оновити лаб4" --tags uni urgent
python -m smartnotes.app list
python -m smartnotes.app search "звіт"
python -m smartnotes.app delete <note_id>
```

Дані зберігаються у файлі `data/notes.json`, який створюється автоматично.

### Графічний інтерфейс (Tkinter)

```bash
python -m smartnotes.gui
```

Особливості GUI:
- фільтрація за тегом через випадаючий список;
- миттєвий пошук за ключовим словом;
- додавання, редагування та видалення нотаток в одній формі;
- попередній перегляд і копіювання тексту в буфер обміну;
- оновлений кольоровий стиль на базі Tkinter.

## Експорт звітів у PDF

1. Встанови Playwright і двигун Chromium:
   ```bash
   pip install playwright
   playwright install chromium
   ```
2. Запусти скрипт:
   ```bash
   python convert_reports.py
   ```
   Він відкриє кожен `lab*_report.html` у headless-браузері та збереже `lab*_report.pdf` поруч.

## Kanban & Code Review

- Kanban-дошка: GitHub Projects → `SmartNotes Roadmap`.
- Кожна картка зв'язана з відповідною гілкою/PR (див. звіт у `lab4_report.html`).
- Зображення канбану можна відтворити скриптом:
  ```bash
  python scripts/generate_kanban.py
  ```
  Файл буде збережено як `screenshots/kanban_board.png`.

## Change Log

Останні оновлення описані у файлі `CHANGELOG.md` та дублюються в історії Git.

