import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from dataclasses import dataclass
from typing import List, Optional
import sqlite3
import json
from datetime import datetime
import os

# ──────────────────────────────────────────────
# Theme Configuration
# ──────────────────────────────────────────────


class ThemeManager:
    def __init__(self):
        self.current_theme = "light"
        self.themes = {
            "light": {
                "bg": "#f8f9fa",
                "surface": "#ffffff",
                "surface_variant": "#f1f3f4",
                "primary": "#1976d2",
                "primary_variant": "#1565c0",
                "secondary": "#03dac6",
                "text": "#212121",
                "text_secondary": "#757575",
                "accent": "#ff4081",
                "border": "#e0e0e0",
                "hover": "#f5f5f5",
                "success": "#4caf50",
                "warning": "#ff9800",
                "error": "#f44336",
                "shadow": "#00000010",
            },
            "dark": {
                "bg": "#121212",
                "surface": "#1e1e1e",
                "surface_variant": "#2d2d2d",
                "primary": "#64b5f6",
                "primary_variant": "#42a5f5",
                "secondary": "#64ffda",
                "text": "#ffffff",
                "text_secondary": "#b0b0b0",
                "accent": "#ff6090",
                "border": "#404040",
                "hover": "#333333",
                "success": "#81c784",
                "warning": "#ffb74d",
                "error": "#e57373",
                "shadow": "#00000030",
            },
        }

    def get_color(self, color_name):
        return self.themes[self.current_theme][color_name]

    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"


# Global theme manager
theme = ThemeManager()

# ──────────────────────────────────────────────
# Custom Widgets with Modern Styling
# ──────────────────────────────────────────────


class ModernFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(
            bg=theme.get_color("surface"),
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=theme.get_color("border"),
            highlightcolor=theme.get_color("primary"),
        )


class GlassyFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(
            bg=theme.get_color("surface_variant"),
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=theme.get_color("border"),
            highlightcolor=theme.get_color("primary"),
        )


class ModernButton(tk.Button):
    def __init__(self, parent, **kwargs):
        # Extract custom style options
        button_style = kwargs.pop("style", "primary")

        super().__init__(parent, **kwargs)

        if button_style == "primary":
            self.configure(
                bg=theme.get_color("primary"),
                fg="white",
                activebackground=theme.get_color("primary_variant"),
                activeforeground="white",
                relief="flat",
                bd=0,
                font=("Segoe UI", 10, "normal"),
                cursor="hand2",
                padx=20,
                pady=8,
            )
        elif button_style == "secondary":
            self.configure(
                bg=theme.get_color("surface_variant"),
                fg=theme.get_color("text"),
                activebackground=theme.get_color("hover"),
                activeforeground=theme.get_color("text"),
                relief="flat",
                bd=0,
                font=("Segoe UI", 10, "normal"),
                cursor="hand2",
                padx=20,
                pady=8,
            )
        elif button_style == "danger":
            self.configure(
                bg=theme.get_color("error"),
                fg="white",
                activebackground="#d32f2f",
                activeforeground="white",
                relief="flat",
                bd=0,
                font=("Segoe UI", 10, "normal"),
                cursor="hand2",
                padx=20,
                pady=8,
            )

        # Add hover effects
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, event):
        if self["bg"] == theme.get_color("primary"):
            self.configure(bg=theme.get_color("primary_variant"))
        elif self["bg"] == theme.get_color("surface_variant"):
            self.configure(bg=theme.get_color("hover"))

    def _on_leave(self, event):
        if self["bg"] == theme.get_color("primary_variant"):
            self.configure(bg=theme.get_color("primary"))
        elif self["bg"] == theme.get_color("hover"):
            self.configure(bg=theme.get_color("surface_variant"))


class ModernEntry(tk.Entry):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(
            bg=theme.get_color("surface"),
            fg=theme.get_color("text"),
            insertbackground=theme.get_color("primary"),
            relief="flat",
            bd=0,
            highlightthickness=2,
            highlightbackground=theme.get_color("border"),
            highlightcolor=theme.get_color("primary"),
            font=("Segoe UI", 11, "normal"),
            selectbackground=theme.get_color("primary"),
            selectforeground="white",
        )


class ModernText(tk.Text):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(
            bg=theme.get_color("surface"),
            fg=theme.get_color("text"),
            insertbackground=theme.get_color("primary"),
            relief="flat",
            bd=0,
            highlightthickness=2,
            highlightbackground=theme.get_color("border"),
            highlightcolor=theme.get_color("primary"),
            font=("Segoe UI", 11, "normal"),
            selectbackground=theme.get_color("primary"),
            selectforeground="white",
            wrap=tk.WORD,
            padx=15,
            pady=15,
            spacing1=2,
            spacing3=2,
        )


class ModernListbox(tk.Listbox):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(
            bg=theme.get_color("surface"),
            fg=theme.get_color("text"),
            selectbackground=theme.get_color("primary"),
            selectforeground="white",
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=theme.get_color("border"),
            highlightcolor=theme.get_color("primary"),
            font=("Segoe UI", 10, "normal"),
            activestyle="none",
        )


class ModernLabel(tk.Label):
    def __init__(self, parent, style="normal", **kwargs):
        super().__init__(parent, **kwargs)

        if style == "title":
            self.configure(
                bg=theme.get_color("bg"),
                fg=theme.get_color("text"),
                font=("Segoe UI", 16, "bold"),
            )
        elif style == "subtitle":
            self.configure(
                bg=theme.get_color("bg"),
                fg=theme.get_color("text_secondary"),
                font=("Segoe UI", 12, "normal"),
            )
        elif style == "caption":
            self.configure(
                bg=theme.get_color("bg"),
                fg=theme.get_color("text_secondary"),
                font=("Segoe UI", 9, "normal"),
            )
        else:
            self.configure(
                bg=theme.get_color("bg"),
                fg=theme.get_color("text"),
                font=("Segoe UI", 10, "normal"),
            )


# ──────────────────────────────────────────────
# Database Setup (unchanged)
# ──────────────────────────────────────────────

DB_FILE = "notes.db"


def init_database():
    """Initialize SQLite database with required tables."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create notes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL DEFAULT '',
            mode TEXT NOT NULL DEFAULT 'normal',
            category TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create tasks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            note_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            done BOOLEAN DEFAULT 0,
            FOREIGN KEY (note_id) REFERENCES notes (id) ON DELETE CASCADE
        )
    """)

    # Create settings table for theme
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ──────────────────────────────────────────────
# Models (unchanged)
# ──────────────────────────────────────────────


@dataclass
class TaskItem:
    content: str
    done: bool = False
    id: Optional[int] = None


@dataclass
class Note:
    title: str
    content: str = ""
    tasks: List[TaskItem] = None
    mode: str = "normal"  # "normal" or "task"
    category: str = ""
    id: Optional[int] = None
    created_at: Optional[str] = None
    modified_at: Optional[str] = None

    def __post_init__(self):
        if self.tasks is None:
            self.tasks = []


# ──────────────────────────────────────────────
# Database Operations (enhanced with settings)
# ──────────────────────────────────────────────


class NotesDB:
    @staticmethod
    def save_note(note: Note) -> int:
        """Save or update a note. Returns the note ID."""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        now = datetime.now().isoformat()

        if note.id is None:
            # Create new note
            cursor.execute(
                """
                INSERT INTO notes (title, content, mode, category, created_at, modified_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (note.title, note.content, note.mode, note.category, now, now),
            )
            note_id = cursor.lastrowid
            note.id = note_id
        else:
            # Update existing note
            cursor.execute(
                """
                UPDATE notes 
                SET title=?, content=?, mode=?, category=?, modified_at=?
                WHERE id=?
            """,
                (note.title, note.content, note.mode, note.category, now, note.id),
            )
            note_id = note.id

        # Delete existing tasks and re-insert
        cursor.execute("DELETE FROM tasks WHERE note_id=?", (note_id,))

        # Insert tasks
        for task in note.tasks:
            cursor.execute(
                """
                INSERT INTO tasks (note_id, content, done)
                VALUES (?, ?, ?)
            """,
                (note_id, task.content, task.done),
            )

        conn.commit()
        conn.close()
        return note_id

    @staticmethod
    def load_note(note_id: int) -> Optional[Note]:
        """Load a note by ID."""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM notes WHERE id=?", (note_id,))
        row = cursor.fetchone()

        if not row:
            conn.close()
            return None

        note = Note(
            id=row[0],
            title=row[1],
            content=row[2],
            mode=row[3],
            category=row[4],
            created_at=row[5],
            modified_at=row[6],
        )

        # Load tasks
        cursor.execute("SELECT content, done FROM tasks WHERE note_id=?", (note_id,))
        tasks = cursor.fetchall()
        note.tasks = [TaskItem(content=task[0], done=bool(task[1])) for task in tasks]

        conn.close()
        return note

    @staticmethod
    def load_all_notes() -> List[tuple]:
        """Load all notes (id, title, category, modified_at) for the list."""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, title, category, modified_at, mode
            FROM notes 
            ORDER BY modified_at DESC
        """)
        notes = cursor.fetchall()

        conn.close()
        return notes

    @staticmethod
    def delete_note(note_id: int):
        """Delete a note and its tasks."""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM notes WHERE id=?", (note_id,))
        cursor.execute("DELETE FROM tasks WHERE note_id=?", (note_id,))

        conn.commit()
        conn.close()

    @staticmethod
    def search_notes(query: str) -> List[tuple]:
        """Search notes by title or content."""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, title, category, modified_at, mode
            FROM notes 
            WHERE title LIKE ? OR content LIKE ?
            ORDER BY modified_at DESC
        """,
            (f"%{query}%", f"%{query}%"),
        )

        notes = cursor.fetchall()
        conn.close()
        return notes

    @staticmethod
    def get_categories() -> List[str]:
        """Get all unique categories."""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute('SELECT DISTINCT category FROM notes WHERE category != ""')
        categories = [row[0] for row in cursor.fetchall()]

        conn.close()
        return sorted(categories)

    @staticmethod
    def save_setting(key: str, value: str):
        """Save a setting to database."""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO settings (key, value)
            VALUES (?, ?)
        """,
            (key, value),
        )

        conn.commit()
        conn.close()

    @staticmethod
    def load_setting(key: str, default: str = "") -> str:
        """Load a setting from database."""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("SELECT value FROM settings WHERE key=?", (key,))
        row = cursor.fetchone()

        conn.close()
        return row[0] if row else default


# ──────────────────────────────────────────────
# Enhanced Views with Modern Styling
# ──────────────────────────────────────────────


class ModernNoteView(ModernFrame):
    def __init__(self, master, note):
        super().__init__(master)
        self.note = note

        # Create rounded container
        container = GlassyFrame(self)
        container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Text widget with custom styling
        self.text = ModernText(container)

        # Custom scrollbar
        scrollbar = ttk.Scrollbar(
            container, orient=tk.VERTICAL, command=self.text.yview
        )
        self.text.configure(yscrollcommand=scrollbar.set)

        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text.insert("1.0", self.note.content)

    def update_note(self):
        self.note.content = self.text.get("1.0", tk.END).strip()


class ModernTaskView(ModernFrame):
    def __init__(self, master, note):
        super().__init__(master)
        self.note = note
        self.entries = []

        # Main container with glassy effect
        main_container = GlassyFrame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Header
        header = ModernFrame(main_container)
        header.pack(fill=tk.X, padx=15, pady=10)

        title_label = ModernLabel(header, style="subtitle", text="📋 Task List")
        title_label.pack(side=tk.LEFT)

        # Scrollable area for tasks
        canvas = tk.Canvas(
            main_container, bg=theme.get_color("surface"), highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(
            main_container, orient="vertical", command=canvas.yview
        )
        self.scrollable_frame = ModernFrame(canvas)

        self.scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<MouseWheel>", _on_mousewheel)

        self.render_tasks()

    def render_tasks(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.entries = []

        # Add existing tasks with modern styling
        for i, task in enumerate(self.note.tasks):
            task_container = GlassyFrame(self.scrollable_frame)
            task_container.pack(fill=tk.X, padx=15, pady=5)

            task_frame = ModernFrame(task_container)
            task_frame.pack(fill=tk.X, padx=10, pady=8)

            var = tk.BooleanVar(value=task.done)

            # Custom checkbox styling
            cb = tk.Checkbutton(
                task_frame,
                text=task.content,
                variable=var,
                command=self.update_task_states,
                wraplength=350,
                justify=tk.LEFT,
                bg=theme.get_color("surface"),
                fg="gray" if task.done else theme.get_color("text"),
                selectcolor=theme.get_color("primary"),
                activebackground=theme.get_color("surface"),
                activeforeground=theme.get_color("text"),
                font=("Segoe UI", 10, "overstrike" if task.done else "normal"),
                relief="flat",
                bd=0,
                highlightthickness=0,
            )
            cb.pack(side=tk.LEFT, fill=tk.X, expand=True)

            # Modern delete button
            del_btn = ModernButton(
                task_frame,
                text="×",
                command=lambda idx=i: self.delete_task(idx),
                style="danger",
                width=3,
                font=("Segoe UI", 12, "bold"),
            )
            del_btn.pack(side=tk.RIGHT, padx=5)

            self.entries.append((task, var))

        # Add new task section
        add_container = GlassyFrame(self.scrollable_frame)
        add_container.pack(fill=tk.X, padx=15, pady=10)

        add_frame = ModernFrame(add_container)
        add_frame.pack(fill=tk.X, padx=10, pady=10)

        add_label = ModernLabel(add_frame, text="✨ Add new task:")
        add_label.pack(anchor=tk.W, pady=(0, 5))

        entry_frame = ModernFrame(add_frame)
        entry_frame.pack(fill=tk.X, pady=5)

        self.new_entry = ModernEntry(entry_frame)
        self.new_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.new_entry.bind("<Return>", self.add_task)

        add_btn = ModernButton(
            entry_frame, text="Add", command=self.add_task, style="primary"
        )
        add_btn.pack(side=tk.RIGHT)

    def add_task(self, event=None):
        content = self.new_entry.get().strip()
        if content:
            self.note.tasks.append(TaskItem(content=content))
            self.new_entry.delete(0, tk.END)
            self.render_tasks()

    def delete_task(self, index):
        if 0 <= index < len(self.note.tasks):
            del self.note.tasks[index]
            self.render_tasks()

    def update_task_states(self):
        for task, var in self.entries:
            task.done = var.get()
        self.render_tasks()


# ──────────────────────────────────────────────
# Main Modern Application
# ──────────────────────────────────────────────


class ModernNoteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("✨ Modern Notes - Advanced Note Taking")
        self.geometry("1200x800")
        self.minsize(900, 600)

        # Initialize database
        init_database()

        # Load theme preference
        saved_theme = NotesDB.load_setting("theme", "light")
        theme.current_theme = saved_theme

        self.current_note = None
        self.current_view = None
        self.notes_data = []  # Store notes data for reference

        self.setup_style()
        self.create_modern_ui()
        self.apply_theme()
        self.refresh_notes_list()

    def setup_style(self):
        """Configure the application styling."""
        # Configure ttk styles
        style = ttk.Style()

        # Configure Combobox
        style.configure(
            "Modern.TCombobox",
            fieldbackground=theme.get_color("surface"),
            background=theme.get_color("surface"),
            foreground=theme.get_color("text"),
            bordercolor=theme.get_color("border"),
            lightcolor=theme.get_color("surface"),
            darkcolor=theme.get_color("surface"),
            relief="flat",
        )

        # Configure Scrollbar
        style.configure(
            "Modern.Vertical.TScrollbar",
            background=theme.get_color("surface_variant"),
            troughcolor=theme.get_color("surface"),
            bordercolor=theme.get_color("border"),
            arrowcolor=theme.get_color("text_secondary"),
            darkcolor=theme.get_color("surface_variant"),
            lightcolor=theme.get_color("surface_variant"),
        )

    def create_modern_ui(self):
        """Create the modern UI with glassy effects."""
        self.configure(bg=theme.get_color("bg"))

        # Main container with padding
        main_container = ModernFrame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Top header bar
        header_frame = GlassyFrame(main_container)
        header_frame.pack(fill=tk.X, pady=(0, 15))

        # App title and theme toggle
        header_content = ModernFrame(header_frame)
        header_content.pack(fill=tk.X, padx=20, pady=15)

        title_label = ModernLabel(header_content, style="title", text="✨ Modern Notes")
        title_label.pack(side=tk.LEFT)

        # Theme toggle button
        self.theme_btn = ModernButton(
            header_content,
            text="🌙" if theme.current_theme == "light" else "☀️",
            command=self.toggle_theme,
            style="secondary",
            font=("Segoe UI", 12),
        )
        self.theme_btn.pack(side=tk.RIGHT)

        # Main content area with paned window effect
        content_frame = ModernFrame(main_container)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Left sidebar - Notes list
        sidebar = GlassyFrame(content_frame)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        sidebar.configure(width=350)
        sidebar.pack_propagate(False)

        self.create_sidebar(sidebar)

        # Right panel - Note editor
        self.editor_container = GlassyFrame(content_frame)
        self.editor_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.create_editor_panel()

    def create_sidebar(self, parent):
        """Create the modern sidebar with notes list."""
        # Sidebar header
        sidebar_header = ModernFrame(parent)
        sidebar_header.pack(fill=tk.X, padx=15, pady=15)

        notes_label = ModernLabel(
            sidebar_header, style="subtitle", text="📚 Your Notes"
        )
        notes_label.pack(side=tk.LEFT)

        # Search section
        search_container = GlassyFrame(parent)
        search_container.pack(fill=tk.X, padx=15, pady=(0, 10))

        search_frame = ModernFrame(search_container)
        search_frame.pack(fill=tk.X, padx=15, pady=15)

        search_label = ModernLabel(search_frame, text="🔍 Search:")
        search_label.pack(anchor=tk.W, pady=(0, 5))

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search)
        self.search_entry = ModernEntry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(fill=tk.X, pady=(0, 10))

        # Category filter
        category_label = ModernLabel(search_frame, text="🏷️ Category:")
        category_label.pack(anchor=tk.W, pady=(0, 5))

        self.category_filter = ttk.Combobox(
            search_frame, style="Modern.TCombobox", width=20
        )
        self.category_filter.pack(fill=tk.X)
        self.category_filter.bind("<<ComboboxSelected>>", self.on_category_filter)

        # Notes list
        list_container = GlassyFrame(parent)
        list_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        list_frame = ModernFrame(list_container)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        self.notes_listbox = ModernListbox(list_frame)
        list_scrollbar = ttk.Scrollbar(
            list_frame,
            orient=tk.VERTICAL,
            command=self.notes_listbox.yview,
            style="Modern.Vertical.TScrollbar",
        )
        self.notes_listbox.configure(yscrollcommand=list_scrollbar.set)

        self.notes_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.notes_listbox.bind("<Double-Button-1>", self.on_note_select)

        # Action buttons
        btn_container = GlassyFrame(parent)
        btn_container.pack(fill=tk.X, padx=15, pady=15)

        btn_frame = ModernFrame(btn_container)
        btn_frame.pack(fill=tk.X, padx=15, pady=15)

        new_btn = ModernButton(
            btn_frame, text="📝 New Note", command=self.new_note, style="primary"
        )
        new_btn.pack(fill=tk.X, pady=(0, 8))

        delete_btn = ModernButton(
            btn_frame, text="🗑️ Delete", command=self.delete_note, style="danger"
        )
        delete_btn.pack(fill=tk.X)

    def create_editor_panel(self):
        """Create the modern editor panel."""
        # Editor header
        self.editor_header = ModernFrame(self.editor_container)
        self.editor_header.pack(fill=tk.X, padx=20, pady=20)

        # Title section
        title_container = GlassyFrame(self.editor_header)
        title_container.pack(fill=tk.X, pady=(0, 15))

        title_frame = ModernFrame(title_container)
        title_frame.pack(fill=tk.X, padx=20, pady=15)

        title_label = ModernLabel(title_frame, text="📄 Title:")
        title_label.pack(anchor=tk.W, pady=(0, 5))

        self.title_entry = ModernEntry(title_frame)
        self.title_entry.pack(fill=tk.X, pady=(0, 10))

        # Category section
        cat_label = ModernLabel(title_frame, text="🏷️ Category:")
        cat_label.pack(anchor=tk.W, pady=(0, 5))

        self.category_entry = ModernEntry(title_frame)
        self.category_entry.pack(fill=tk.X)

        # Control buttons
        controls_container = GlassyFrame(self.editor_header)
        controls_container.pack(fill=tk.X)

        controls_frame = ModernFrame(controls_container)
        controls_frame.pack(fill=tk.X, padx=20, pady=15)

        self.mode_button = ModernButton(
            controls_frame,
            text="📋 Switch to Tasks",
            command=self.toggle_mode,
            style="secondary",
        )
        self.mode_button.pack(side=tk.LEFT, padx=(0, 10))

        save_btn = ModernButton(
            controls_frame, text="💾 Save", command=self.save_note, style="primary"
        )
        save_btn.pack(side=tk.LEFT)

        # Timestamps
        self.timestamp_label = ModernLabel(controls_frame, style="caption", text="")
        self.timestamp_label.pack(side=tk.RIGHT)

        # Content area
        self.content_frame = ModernFrame(self.editor_container)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        self.show_welcome_message()

    def show_welcome_message(self):
        """Show a beautiful welcome message when no note is selected."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        welcome_container = GlassyFrame(self.content_frame)
        welcome_container.pack(fill=tk.BOTH, expand=True)

        welcome_frame = ModernFrame(welcome_container)
        welcome_frame.pack(expand=True)

        # Welcome icon and text
        icon_label = ModernLabel(welcome_frame, text="📝", font=("Segoe UI", 48))
        icon_label.pack(pady=20)

        welcome_title = ModernLabel(
            welcome_frame, style="title", text="Welcome to Modern Notes"
        )
        welcome_title.pack(pady=10)

        welcome_subtitle = ModernLabel(
            welcome_frame,
            style="subtitle",
            text="Select a note from the sidebar or create a new one to start writing",
        )
        welcome_subtitle.pack(pady=10)

        # Quick action buttons
        actions_frame = ModernFrame(welcome_frame)
        actions_frame.pack(pady=30)

        quick_note_btn = ModernButton(
            actions_frame, text="✨ Create Note", command=self.new_note, style="primary"
        )
        quick_note_btn.pack(pady=5)

    def toggle_theme(self):
        """Toggle between light and dark themes."""
        theme.toggle_theme()
        NotesDB.save_setting("theme", theme.current_theme)
        self.apply_theme()

    def apply_theme(self):
        """Apply the current theme to all widgets."""
        # Update main window
        self.configure(bg=theme.get_color("bg"))

        # Update theme button
        self.theme_btn.configure(text="🌙" if theme.current_theme == "light" else "☀️")

        # Recursively update all widgets
        self.update_widget_theme(self)

        # Refresh current view if exists
        if self.current_note:
            self.load_current_note()

    def update_widget_theme(self, widget):
        """Recursively update theme for all widgets."""
        widget_class = widget.__class__.__name__

        if isinstance(widget, (ModernFrame, GlassyFrame)):
            if isinstance(widget, ModernFrame):
                widget.configure(
                    bg=theme.get_color("surface"),
                    highlightbackground=theme.get_color("border"),
                    highlightcolor=theme.get_color("primary"),
                )
            else:  # GlassyFrame
                widget.configure(
                    bg=theme.get_color("surface_variant"),
                    highlightbackground=theme.get_color("border"),
                    highlightcolor=theme.get_color("primary"),
                )

        elif isinstance(widget, ModernEntry):
            widget.configure(
                bg=theme.get_color("surface"),
                fg=theme.get_color("text"),
                insertbackground=theme.get_color("primary"),
                highlightbackground=theme.get_color("border"),
                highlightcolor=theme.get_color("primary"),
                selectbackground=theme.get_color("primary"),
            )

        elif isinstance(widget, ModernText):
            widget.configure(
                bg=theme.get_color("surface"),
                fg=theme.get_color("text"),
                insertbackground=theme.get_color("primary"),
                highlightbackground=theme.get_color("border"),
                highlightcolor=theme.get_color("primary"),
                selectbackground=theme.get_color("primary"),
            )

        elif isinstance(widget, ModernListbox):
            widget.configure(
                bg=theme.get_color("surface"),
                fg=theme.get_color("text"),
                selectbackground=theme.get_color("primary"),
                highlightbackground=theme.get_color("border"),
                highlightcolor=theme.get_color("primary"),
            )

        elif isinstance(widget, ModernLabel):
            widget.configure(
                bg=theme.get_color("bg")
                if widget.master.__class__.__name__ == "Tk"
                else theme.get_color("surface"),
                fg=theme.get_color("text")
                if "secondary" not in str(widget.cget("font"))
                else theme.get_color("text_secondary"),
            )

        elif isinstance(widget, tk.Canvas):
            widget.configure(bg=theme.get_color("surface"), highlightthickness=0)

        elif isinstance(widget, tk.Checkbutton):
            widget.configure(
                bg=theme.get_color("surface"),
                fg=theme.get_color("text"),
                selectcolor=theme.get_color("primary"),
                activebackground=theme.get_color("surface"),
                activeforeground=theme.get_color("text"),
            )

        # Update children recursively
        for child in widget.winfo_children():
            self.update_widget_theme(child)

    def refresh_notes_list(self):
        """Refresh the notes list with modern styling."""
        self.notes_listbox.delete(0, tk.END)

        # Get search query and category filter
        search_query = self.search_var.get().strip()
        selected_category = self.category_filter.get()

        if search_query:
            notes = NotesDB.search_notes(search_query)
        else:
            notes = NotesDB.load_all_notes()

        # Store notes data for reference
        self.notes_data = notes

        # Filter by category if selected
        if selected_category and selected_category != "All":
            notes = [note for note in notes if note[2] == selected_category]
            self.notes_data = notes

        # Update listbox with enhanced formatting
        for note_id, title, category, modified_at, mode in notes:
            # Create formatted display text
            mode_icon = "📋" if mode == "task" else "📝"
            display_text = f"{mode_icon} {title}"

            if category:
                display_text += f" • {category}"

            # Add timestamp
            try:
                dt = datetime.fromisoformat(modified_at)
                time_str = dt.strftime("%m/%d %H:%M")
                display_text += f"\n   {time_str}"
            except:
                pass

            self.notes_listbox.insert(tk.END, display_text)

        # Update category filter
        categories = ["All"] + NotesDB.get_categories()
        self.category_filter["values"] = categories
        if not self.category_filter.get():
            self.category_filter.set("All")

    def on_search(self, *args):
        """Handle search input changes."""
        self.refresh_notes_list()

    def on_category_filter(self, event=None):
        """Handle category filter changes."""
        self.refresh_notes_list()

    def on_note_select(self, event=None):
        """Handle note selection from listbox."""
        selection = self.notes_listbox.curselection()
        if not selection or not self.notes_data:
            return

        if selection[0] < len(self.notes_data):
            note_id = self.notes_data[selection[0]][0]
            self.load_note(note_id)

    def new_note(self):
        """Create a new note with modern dialog."""
        title = simpledialog.askstring("✨ New Note", "Enter note title:", parent=self)
        if title:
            note = Note(title=title)
            note_id = NotesDB.save_note(note)
            note.id = note_id
            self.current_note = note
            self.load_current_note()
            self.refresh_notes_list()

    def delete_note(self):
        """Delete the selected note with confirmation."""
        selection = self.notes_listbox.curselection()
        if not selection:
            messagebox.showwarning(
                "⚠️ Warning", "Please select a note to delete.", parent=self
            )
            return

        if messagebox.askyesno(
            "🗑️ Confirm Delete",
            "Are you sure you want to delete this note?\nThis action cannot be undone.",
            parent=self,
        ):
            if selection[0] < len(self.notes_data):
                note_id = self.notes_data[selection[0]][0]
                NotesDB.delete_note(note_id)
                self.refresh_notes_list()
                self.show_welcome_message()
                self.current_note = None

    def load_note(self, note_id: int):
        """Load a note by ID."""
        note = NotesDB.load_note(note_id)
        if note:
            self.current_note = note
            self.load_current_note()

    def load_current_note(self):
        """Load the current note into the modern editor."""
        if not self.current_note:
            return

        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Update form fields
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, self.current_note.title)

        self.category_entry.delete(0, tk.END)
        self.category_entry.insert(0, self.current_note.category)

        # Update timestamps with modern formatting
        if self.current_note.created_at:
            try:
                created = datetime.fromisoformat(self.current_note.created_at)
                modified = datetime.fromisoformat(self.current_note.modified_at)
                timestamp_text = f"Created: {created.strftime('%m/%d/%Y %H:%M')} • Modified: {modified.strftime('%m/%d/%Y %H:%M')}"
                self.timestamp_label.config(text=timestamp_text)
            except:
                self.timestamp_label.config(text="")

        # Create appropriate modern view
        if self.current_note.mode == "normal":
            self.current_view = ModernNoteView(self.content_frame, self.current_note)
            self.mode_button.config(text="📋 Switch to Tasks")
        else:
            self.current_view = ModernTaskView(self.content_frame, self.current_note)
            self.mode_button.config(text="📝 Switch to Notes")

        self.current_view.pack(fill=tk.BOTH, expand=True)

        # Apply theme to new view
        self.update_widget_theme(self.current_view)

    def toggle_mode(self):
        """Toggle between normal and task mode with smooth transition."""
        if not self.current_note:
            return

        # Update content before switching
        if self.current_view and hasattr(self.current_view, "update_note"):
            self.current_view.update_note()

        # Toggle mode
        self.current_note.mode = (
            "task" if self.current_note.mode == "normal" else "normal"
        )

        # Reload the view with animation effect
        self.load_current_note()

    def save_note(self):
        """Save the current note with modern feedback."""
        if not self.current_note:
            messagebox.showwarning("⚠️ Warning", "No note to save.", parent=self)
            return

        # Update note data from form
        self.current_note.title = self.title_entry.get().strip()
        self.current_note.category = self.category_entry.get().strip()

        if not self.current_note.title:
            messagebox.showerror(
                "❌ Error", "Please enter a title for the note.", parent=self
            )
            return

        # Update content if in normal mode
        if self.current_view and hasattr(self.current_view, "update_note"):
            self.current_view.update_note()

        # Save to database
        NotesDB.save_note(self.current_note)

        # Refresh UI
        self.refresh_notes_list()
        self.load_current_note()  # Refresh timestamps

        messagebox.showinfo("✅ Success", "Note saved successfully!", parent=self)

    def on_closing(self):
        """Handle application closing."""
        # Auto-save current note if exists
        if self.current_note:
            self.current_note.title = self.title_entry.get().strip()
            self.current_note.category = self.category_entry.get().strip()

            if self.current_view and hasattr(self.current_view, "update_note"):
                self.current_view.update_note()

            if self.current_note.title:  # Only save if has title
                NotesDB.save_note(self.current_note)

        self.destroy()

    # ──────────────────────────────────────────────
    # Enhanced Entry Point
    # ──────────────────────────────────────────────


if __name__ == "__main__":
    app = ModernNoteApp()

    # Set window icon and properties
    try:
        # Try to set a nice window icon (optional)
        app.iconbitmap("")  # You can add an icon file path here
    except:
        pass

    # Handle window closing
    app.protocol("WM_DELETE_WINDOW", app.on_closing)

    # Center window on screen
    app.update_idletasks()
    width = app.winfo_width()
    height = app.winfo_height()
    x = (app.winfo_screenwidth() // 2) - (width // 2)
    y = (app.winfo_screenheight() // 2) - (height // 2)
    app.geometry(f"{width}x{height}+{x}+{y}")

    # Start the application
    app.mainloop()
