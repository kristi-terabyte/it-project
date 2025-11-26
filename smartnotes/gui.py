"""
Tkinter-based graphical interface for SmartNotes.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from .storage import Note, NoteStorage


class SmartNotesGUI:
    def __init__(self) -> None:
        self.storage = NoteStorage()
        self.root = tk.Tk()
        self.root.title("SmartNotes")
        self.root.geometry("900x600")

        self.notes: list[Note] = []

        self._build_widgets()
        self._refresh_notes()

    def _build_widgets(self) -> None:
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=2)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # Left panel list
        list_frame = ttk.Frame(self.root, padding=10)
        list_frame.grid(row=0, column=0, sticky="nsew", rowspan=2)
        list_frame.rowconfigure(1, weight=1)
        list_frame.columnconfigure(0, weight=1)

        filter_frame = ttk.Frame(list_frame)
        filter_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        filter_frame.columnconfigure(1, weight=1)

        ttk.Label(filter_frame, text="Тег:").grid(row=0, column=0, padx=(0, 5))
        self.tag_var = tk.StringVar()
        tag_entry = ttk.Entry(filter_frame, textvariable=self.tag_var)
        tag_entry.grid(row=0, column=1, sticky="ew")

        ttk.Label(filter_frame, text="Пошук:").grid(row=1, column=0, padx=(0, 5), pady=(5, 0))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(filter_frame, textvariable=self.search_var)
        search_entry.grid(row=1, column=1, sticky="ew", pady=(5, 0))

        button_frame = ttk.Frame(filter_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=5, sticky="ew")
        ttk.Button(button_frame, text="Оновити", command=self._refresh_notes).pack(side="left", padx=(0, 5))
        ttk.Button(button_frame, text="Очистити", command=self._clear_filters).pack(side="left")

        self.listbox = tk.Listbox(list_frame, height=20)
        self.listbox.grid(row=1, column=0, sticky="nsew")
        self.listbox.bind("<<ListboxSelect>>", lambda _: self._show_selected_note())

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.listbox.configure(yscrollcommand=scrollbar.set)

        # Right panel
        detail_frame = ttk.Frame(self.root, padding=10)
        detail_frame.grid(row=0, column=1, sticky="nsew")
        detail_frame.columnconfigure(1, weight=1)
        detail_frame.rowconfigure(3, weight=1)

        ttk.Label(detail_frame, text="Заголовок").grid(row=0, column=0, sticky="w")
        self.title_var = tk.StringVar()
        title_entry = ttk.Entry(detail_frame, textvariable=self.title_var)
        title_entry.grid(row=0, column=1, sticky="ew", pady=2)

        ttk.Label(detail_frame, text="Теги (через пробіл)").grid(row=1, column=0, sticky="w")
        self.tags_var = tk.StringVar()
        tags_entry = ttk.Entry(detail_frame, textvariable=self.tags_var)
        tags_entry.grid(row=1, column=1, sticky="ew", pady=2)

        ttk.Label(detail_frame, text="Текст нотатки").grid(row=2, column=0, sticky="w")
        self.body_text = tk.Text(detail_frame, wrap="word", height=10)
        self.body_text.grid(row=2, column=1, sticky="nsew", pady=5)

        action_frame = ttk.Frame(detail_frame)
        action_frame.grid(row=4, column=0, columnspan=2, pady=5, sticky="ew")
        ttk.Button(action_frame, text="Додати / Оновити", command=self._create_note).pack(side="left")
        ttk.Button(action_frame, text="Видалити", command=self._delete_note).pack(side="left", padx=5)

        # Preview frame
        preview_frame = ttk.Frame(self.root, padding=10)
        preview_frame.grid(row=1, column=1, sticky="nsew")
        preview_frame.rowconfigure(0, weight=1)
        preview_frame.columnconfigure(0, weight=1)
        ttk.Label(preview_frame, text="Перегляд вибраної нотатки").pack(anchor="w")
        self.preview_text = tk.Text(preview_frame, wrap="word", state="disabled")
        self.preview_text.pack(fill="both", expand=True, pady=5)

    def _clear_filters(self) -> None:
        self.tag_var.set("")
        self.search_var.set("")
        self._refresh_notes()

    def _refresh_notes(self) -> None:
        tag = self.tag_var.get().strip() or None
        keyword = self.search_var.get().strip()
        if keyword:
            notes = self.storage.search(keyword)
        else:
            notes = self.storage.list_notes(tag=tag)
        self.notes = notes
        self.listbox.delete(0, tk.END)
        for note in notes:
            display = f"{note.title}  [{', '.join(note.tags) or 'без тегів'}]"
            self.listbox.insert(tk.END, display)
        self.preview_text.configure(state="normal")
        self.preview_text.delete("1.0", tk.END)
        self.preview_text.configure(state="disabled")

    def _show_selected_note(self) -> None:
        selection = self.listbox.curselection()
        if not selection:
            return
        note = self.notes[selection[0]]
        self.preview_text.configure(state="normal")
        self.preview_text.delete("1.0", tk.END)
        self.preview_text.insert(tk.END, f"{note.title}\n{'=' * len(note.title)}\n")
        self.preview_text.insert(tk.END, f"Теги: {', '.join(note.tags) or 'без тегів'}\n")
        self.preview_text.insert(tk.END, f"Створено: {note.created_at}\n\n")
        self.preview_text.insert(tk.END, note.body)
        self.preview_text.configure(state="disabled")

    def _create_note(self) -> None:
        title = self.title_var.get().strip()
        body = self.body_text.get("1.0", tk.END).strip()
        tags = [tag for tag in self.tags_var.get().split() if tag]

        if not title or not body:
            messagebox.showwarning("Помилка", "Необхідно вказати заголовок і текст.")
            return

        self.storage.add_note(title=title, body=body, tags=tags)
        self.title_var.set("")
        self.body_text.delete("1.0", tk.END)
        self.tags_var.set("")
        self._refresh_notes()
        messagebox.showinfo("Успіх", "Нотатку додано.")

    def _delete_note(self) -> None:
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showinfo("SmartNotes", "Оберіть нотатку для видалення.")
            return
        note = self.notes[selection[0]]
        confirm = messagebox.askyesno("Підтвердження", f"Видалити '{note.title}'?")
        if confirm:
            if self.storage.delete(note.id):
                self._refresh_notes()
                messagebox.showinfo("SmartNotes", "Нотатку видалено.")
            else:
                messagebox.showerror("SmartNotes", "Не вдалося видалити нотатку.")

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    app = SmartNotesGUI()
    app.run()


if __name__ == "__main__":
    main()

