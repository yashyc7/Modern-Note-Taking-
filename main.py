import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from dataclasses import dataclass
from typing import List, Optional
import sqlite3
from datetime import datetime

# ──────────────────────────────────────────────
# Theme Configuration (Unchanged)
# ──────────────────────────────────────────────


class ThemeManager:
    def __init__(self):
        self.current_theme = "dark"  # Default to dark for modern look
        self.themes = {
            "light": {
                "bg": "#ffffff",
                "surface": "#ffffff",
                "surface_variant": "#e8ecef",
                "primary": "#ff6f61",
                "primary_variant": "#ff4b3a",
                "secondary": "#40c4ff",
                "text": "#212121",
                "text_secondary": "#757575",
                "accent": "#ff4081",
                "border": "#d0d7de",
                "hover": "#e0e0e0",
                "success": "#4caf50",
                "warning": "#ff9800",
                "error": "#f44336",
                "shadow": "#00000020",
            },
            "dark": {
                "bg": "#2d3748",  # Navy background
                "surface": "#2d3748",
                "surface_variant": "#4a5568",
                "primary": "#ff6f61",  # Neon coral
                "primary_variant": "#ff4b3a",
                "secondary": "#40c4ff",  # Neon cyan
                "text": "#e2e8f0",
                "text_secondary": "#a0aec0",
                "accent": "#ff6090",
                "border": "#4a5568",
                "hover": "#718096",
                "success": "#81c784",
                "warning": "#ffb74d",
                "error": "#e57373",
                "shadow": "#00000040",
            },
        }

    def get_color(self, color_name):
        return self.themes[self.current_theme][color_name]

    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"


# Global theme manager
theme = ThemeManager()

# ──────────────────────────────────────────────
# Custom Widgets with Rounded Borders (Unchanged)
# ──────────────────────────────────────────────


class ModernFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(
            bg=theme.get_color("surface"),
            relief="raised",  # Use raised relief to simulate rounded edges
            bd=2,  # Border width to enhance the effect
            highlightthickness=0,  # Remove default highlight
        )


class GlassyFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(
            bg=theme.get_color("surface_variant"),
            relief="raised",
            bd=2,
            highlightthickness=0,
        )


class ModernButton(tk.Button):
    def __init__(self, parent, **kwargs):
        button_style = kwargs.pop("style", "primary")
        super().__init__(parent, **kwargs)
        if button_style == "primary":
            self.configure(
                bg=theme.get_color("primary"),
                fg="white",
                activebackground=theme.get_color("primary_variant"),
                activeforeground="white",
                relief="raised",
                bd=2,
                font=("Segoe UI", 10, "normal"),
                cursor="hand2",
                padx=15,
                pady=5,
            )
        elif button_style == "secondary":
            self.configure(
                bg=theme.get_color("surface_variant"),
                fg=theme.get_color("text"),
                activebackground=theme.get_color("hover"),
                activeforeground=theme.get_color("text"),
                relief="raised",
                bd=2,
                font=("Segoe UI", 10, "normal"),
                cursor="hand2",
                padx=15,
                pady=5,
            )
        elif button_style == "danger":
            self.configure(
                bg=theme.get_color("error"),
                fg="white",
                activebackground="#d32f2f",
                activeforeground="white",
                relief="raised",
                bd=2,
                font=("Segoe UI", 10, "normal"),
                cursor="hand2",
                padx=15,
                pady=5,
            )
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
            relief="sunken",
            bd=2,
            highlightthickness=0,
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
            relief="sunken",
            bd=2,
            highlightthickness=0,
            font=("Segoe UI", 11, "normal"),
            selectbackground=theme.get_color("primary"),
            selectforeground="white",
            wrap=tk.WORD,
            padx=10,
            pady=10,
            spacing1=2,
            spacing3=2,
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
# Note Card (Unchanged)
# ──────────────────────────────────────────────


class NoteCard(tk.Frame):
    def __init__(
        self,
        parent,
        note_id,
        title,
        category,
        modified_at,
        mode,
        color_tag,
        pinned,
        on_click,
        on_pin,
    ):
        super().__init__(parent)
        self.note_id = note_id
        self.pinned = pinned
        self.color_tag = color_tag or "default"
        self.bg_color = (
            theme.get_color("surface")
            if self.color_tag == "default"
            else self.color_tag
        )
        self.configure(
            bg=self.bg_color,
            relief="raised",
            bd=2,
            highlightthickness=0,
        )
        self.grid_propagate(False)
        self.configure(width=200, height=150)

        # Card content
        card_frame = tk.Frame(self, bg=self.bg_color)
        card_frame.pack(fill=tk.BOTH, padx=5, pady=5)

        # Pin button
        pin_btn = tk.Button(
            card_frame,
            text="📌" if pinned else "📍",
            font=("Segoe UI", 8),
            bg=self.bg_color,
            fg=theme.get_color("text"),
            relief="flat",
            bd=0,
            command=lambda: on_pin(self.note_id),
            cursor="hand2",
        )
        pin_btn.pack(side=tk.RIGHT, padx=5)

        # Mode icon and title
        mode_icon = "📋" if mode == "task" else "📝"
        title_text = f"{mode_icon} {title[:20]}{'...' if len(title) > 20 else ''}"
        title_label = tk.Label(
            card_frame,
            text=title_text,
            bg=self.bg_color,
            fg=theme.get_color("text"),
            font=("Segoe UI", 12, "bold"),
            anchor="w",
            wraplength=160,
        )
        title_label.pack(fill=tk.X, pady=(5, 2))

        # Category
        if category:
            cat_label = tk.Label(
                card_frame,
                text=category,
                bg=self.bg_color,
                fg=theme.get_color("secondary"),
                font=("Segoe UI", 9, "normal"),
                anchor="w",
                wraplength=160,
            )
            cat_label.pack(fill=tk.X)

        # Timestamp
        try:
            dt = datetime.fromisoformat(modified_at)
            time_str = dt.strftime("%m/%d %H:%M")
            time_label = tk.Label(
                card_frame,
                text=time_str,
                bg=self.bg_color,
                fg=theme.get_color("text_secondary"),
                font=("Segoe UI", 8, "normal"),
                anchor="w",
            )
            time_label.pack(fill=tk.X, pady=(2, 5))
        except:
            pass

        # Bind click and hover effects
        self.bind("<Button-1>", lambda e: on_click(self.note_id))
        for child in self.winfo_children():
            child.bind("<Button-1>", lambda e: on_click(self.note_id))
            for subchild in child.winfo_children():
                subchild.bind("<Button-1>", lambda e: on_click(self.note_id))

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        for child in self.winfo_children():
            child.bind("<Enter>", self._on_enter)
            child.bind("<Leave>", self._on_leave)
            for subchild in child.winfo_children():
                subchild.bind("<Enter>", self._on_enter)
                subchild.bind("<Leave>", self._on_leave)

    def _on_enter(self, event):
        hover_color = (
            theme.get_color("hover")
            if self.color_tag == "default"
            else self._lighten_color(self.color_tag)
        )
        self.configure(bg=hover_color, highlightthickness=2)
        for child in self.winfo_children():
            child.configure(bg=hover_color)

    def _on_leave(self, event):
        self.configure(bg=self.bg_color, highlightthickness=0)
        for child in self.winfo_children():
            child.configure(bg=self.bg_color)

    def _lighten_color(self, hex_color):
        # Simple function to lighten a hex color for hover effect
        hex_color = hex_color.lstrip("#")
        rgb = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
        rgb = tuple(min(255, int(c * 1.2)) for c in rgb)
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"


# ──────────────────────────────────────────────
# Database Setup (Unchanged)
# ──────────────────────────────────────────────

DB_FILE = "notes.db"


def init_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create the notes table if it doesn't exist
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

    # Check if 'pinned' column exists, and add it if not
    cursor.execute("PRAGMA table_info(notes)")
    columns = [col[1] for col in cursor.fetchall()]
    if "pinned" not in columns:
        cursor.execute("ALTER TABLE notes ADD COLUMN pinned BOOLEAN DEFAULT 0")

    # Check if 'color_tag' column exists, and add it if not
    if "color_tag" not in columns:
        cursor.execute("ALTER TABLE notes ADD COLUMN color_tag TEXT DEFAULT 'default'")

    # Create the tasks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            note_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            done BOOLEAN DEFAULT 0,
            FOREIGN KEY (note_id) REFERENCES notes (id) ON DELETE CASCADE
        )
    """)

    # Create the settings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ──────────────────────────────────────────────
# Models (Unchanged)
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
    mode: str = "normal"
    category: str = ""
    pinned: bool = False
    color_tag: str = "default"
    id: Optional[int] = None
    created_at: Optional[str] = None
    modified_at: Optional[str] = None

    def __post_init__(self):
        if self.tasks is None:
            self.tasks = []


# ──────────────────────────────────────────────
# Database Operations (Unchanged)
# ──────────────────────────────────────────────


class NotesDB:
    @staticmethod
    def save_note(note: Note) -> int:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        now = datetime.now().isoformat()
        if note.id is None:
            cursor.execute(
                """
                INSERT INTO notes (title, content, mode, category, created_at, modified_at, pinned, color_tag)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    note.title,
                    note.content,
                    note.mode,
                    note.category,
                    now,
                    now,
                    note.pinned,
                    note.color_tag,
                ),
            )
            note_id = cursor.lastrowid
            note.id = note_id
        else:
            cursor.execute(
                """
                UPDATE notes 
                SET title=?, content=?, mode=?, category=?, modified_at=?, pinned=?, color_tag=?
                WHERE id=?
            """,
                (
                    note.title,
                    note.content,
                    note.mode,
                    note.category,
                    now,
                    note.pinned,
                    note.color_tag,
                    note.id,
                ),
            )
            note_id = note.id
        cursor.execute("DELETE FROM tasks WHERE note_id=?", (note_id,))
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
            pinned=bool(row[7]),
            color_tag=row[8],
        )
        cursor.execute("SELECT content, done FROM tasks WHERE note_id=?", (note_id,))
        tasks = cursor.fetchall()
        note.tasks = [TaskItem(content=task[0], done=bool(task[1])) for task in tasks]
        conn.close()
        return note

    @staticmethod
    def load_all_notes() -> List[tuple]:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, title, category, modified_at, mode, pinned, color_tag
            FROM notes 
            ORDER BY pinned DESC, modified_at DESC
        """)
        notes = cursor.fetchall()
        conn.close()
        return notes

    @staticmethod
    def delete_note(note_id: int):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notes WHERE id=?", (note_id,))
        cursor.execute("DELETE FROM tasks WHERE note_id=?", (note_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def search_notes(query: str) -> List[tuple]:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, title, category, modified_at, mode, pinned, color_tag
            FROM notes 
            WHERE title LIKE ? OR content LIKE ?
            ORDER BY pinned DESC, modified_at DESC
        """,
            (f"%{query}%", f"%{query}%"),
        )
        notes = cursor.fetchall()
        conn.close()
        return notes

    @staticmethod
    def get_categories() -> List[str]:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT category FROM notes WHERE category != ""')
        categories = [row[0] for row in cursor.fetchall()]
        conn.close()
        return sorted(categories)

    @staticmethod
    def save_setting(key: str, value: str):
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
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key=?", (key,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else default


# ──────────────────────────────────────────────
# Enhanced Views (Unchanged)
# ──────────────────────────────────────────────


class ModernNoteView(ModernFrame):
    def __init__(self, master, note):
        super().__init__(master)
        self.note = note
        # Toolbar for formatting
        toolbar = tk.Frame(self, bg=theme.get_color("surface"))
        toolbar.pack(fill=tk.X, padx=10, pady=5)

        bold_btn = ModernButton(
            toolbar,
            text="B",
            style="secondary",
            font=("Segoe UI", 10, "bold"),
            command=self.toggle_bold,
            width=2,
        )
        bold_btn.pack(side=tk.LEFT, padx=2)

        italic_btn = ModernButton(
            toolbar,
            text="I",
            style="secondary",
            font=("Segoe UI", 10, "italic"),
            command=self.toggle_italic,
            width=2,
        )
        italic_btn.pack(side=tk.LEFT, padx=2)

        # Text area
        container = GlassyFrame(self)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.text = ModernText(container)
        scrollbar = ttk.Scrollbar(
            container, orient=tk.VERTICAL, command=self.text.yview
        )
        self.text.configure(yscrollcommand=scrollbar.set)
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.insert("1.0", self.note.content)

        # Configure tags for formatting
        self.text.tag_configure("bold", font=("Segoe UI", 11, "bold"))
        self.text.tag_configure("italic", font=("Segoe UI", 11, "italic"))

    def toggle_bold(self):
        try:
            current_tags = self.text.tag_names("sel.first")
            if "bold" in current_tags:
                self.text.tag_remove("bold", "sel.first", "sel.last")
            else:
                self.text.tag_add("bold", "sel.first", "sel.last")
        except tk.TclError:
            pass

    def toggle_italic(self):
        try:
            current_tags = self.text.tag_names("sel.first")
            if "italic" in current_tags:
                self.text.tag_remove("italic", "sel.first", "sel.last")
            else:
                self.text.tag_add("italic", "sel.first", "sel.last")
        except tk.TclError:
            pass

    def update_note(self):
        self.note.content = self.text.get("1.0", tk.END).strip()


class ModernTaskView(ModernFrame):
    def __init__(self, master, note):
        super().__init__(master)
        self.note = note
        self.entries = []
        main_container = GlassyFrame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        header = ModernFrame(main_container)
        header.pack(fill=tk.X, padx=10, pady=5)
        title_label = ModernLabel(header, style="subtitle", text="📋 Task List")
        title_label.pack(side=tk.LEFT)
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

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<MouseWheel>", _on_mousewheel)
        self.render_tasks()

    def render_tasks(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.entries = []
        for i, task in enumerate(self.note.tasks):
            task_container = GlassyFrame(self.scrollable_frame)
            task_container.pack(fill=tk.X, padx=10, pady=3)
            task_frame = ModernFrame(task_container)
            task_frame.pack(fill=tk.X, padx=5, pady=5)
            var = tk.BooleanVar(value=task.done)
            cb = tk.Checkbutton(
                task_frame,
                text=task.content,
                variable=var,
                command=self.update_task_states,
                wraplength=300,
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
            del_btn = ModernButton(
                task_frame,
                text="×",
                command=lambda idx=i: self.delete_task(idx),
                style="danger",
                width=2,
                font=("Segoe UI", 10, "bold"),
            )
            del_btn.pack(side=tk.RIGHT, padx=3)
            self.entries.append((task, var))
        add_container = GlassyFrame(self.scrollable_frame)
        add_container.pack(fill=tk.X, padx=10, pady=5)
        add_frame = ModernFrame(add_container)
        add_frame.pack(fill=tk.X, padx=5, pady=5)
        add_label = ModernLabel(add_frame, text="✨ Add new task:")
        add_label.pack(anchor=tk.W, pady=(0, 3))
        entry_frame = ModernFrame(add_frame)
        entry_frame.pack(fill=tk.X, pady=3)
        self.new_entry = ModernEntry(entry_frame)
        self.new_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
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
# Main Modern Application (Updated Sidebar Fix)
# ──────────────────────────────────────────────


class ModernNoteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("✨ Modern Notes - Advanced Note Taking")
        self.geometry("1200x800")
        self.minsize(900, 600)
        init_database()
        saved_theme = NotesDB.load_setting("theme", "dark")
        theme.current_theme = saved_theme
        self.current_note = None
        self.current_view = None
        self.notes_data = []
        self.sidebar_visible = False
        self.editor_visible = False
        self.top_bar_height = 0  # To store the height of the top bar
        self.setup_style()
        self.create_modern_ui()
        self.apply_theme()
        self.refresh_notes_grid()

    def setup_style(self):
        style = ttk.Style()
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
        self.configure(bg=theme.get_color("bg"))

        # Main container
        self.main_container = tk.Frame(self, bg=theme.get_color("bg"))
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Top bar
        self.top_bar = ModernFrame(self.main_container)
        self.top_bar.pack(fill=tk.X, padx=5, pady=5)

        # Hamburger menu
        self.menu_btn = ModernButton(
            self.top_bar,
            text="☰",
            style="secondary",
            font=("Segoe UI", 12),
            command=self.toggle_sidebar,
            width=3,
        )
        self.menu_btn.pack(side=tk.LEFT, padx=10)

        # Title
        title_label = ModernLabel(self.top_bar, style="title", text="✨ Modern Notes")
        title_label.pack(side=tk.LEFT)

        # Theme toggle
        self.theme_btn = ModernButton(
            self.top_bar,
            text="🌙" if theme.current_theme == "light" else "☀️",
            command=self.toggle_theme,
            style="secondary",
            font=("Segoe UI", 12),
        )
        self.theme_btn.pack(side=tk.RIGHT, padx=10)

        # Update the top bar height after it's rendered
        self.top_bar.update_idletasks()
        self.top_bar_height = self.top_bar.winfo_height()

        # Sidebar (hidden by default)
        self.sidebar = ModernFrame(self.main_container, width=200)
        self.create_sidebar(self.sidebar)

        # Notes grid
        self.grid_container = tk.Frame(self.main_container, bg=theme.get_color("bg"))
        self.grid_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.notes_canvas = tk.Canvas(
            self.grid_container, bg=theme.get_color("bg"), highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(
            self.grid_container, orient="vertical", command=self.notes_canvas.yview
        )
        self.notes_frame = tk.Frame(self.notes_canvas, bg=theme.get_color("bg"))
        self.notes_frame.bind(
            "<Configure>",
            lambda e: self.notes_canvas.configure(
                scrollregion=self.notes_canvas.bbox("all")
            ),
        )
        self.notes_canvas.create_window((0, 0), window=self.notes_frame, anchor="nw")
        self.notes_canvas.configure(yscrollcommand=scrollbar.set)
        self.notes_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            self.notes_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.notes_canvas.bind("<MouseWheel>", _on_mousewheel)

        # Floating editor panel (larger size)
        self.editor_panel = ModernFrame(self)
        self.editor_panel.place(
            relx=0.5, rely=0.5, anchor="center", width=800, height=600
        )
        self.editor_panel.lower()  # Keep it hidden initially
        self.create_editor_panel()

        # Floating Action Button
        fab_frame = tk.Frame(self, bg=theme.get_color("bg"))
        fab_frame.place(relx=0.95, rely=0.9, anchor="se")
        self.fab = ModernButton(
            fab_frame,
            text="+",
            font=("Segoe UI", 20, "bold"),
            style="primary",
            width=3,
            height=1,
            command=self.new_note,
        )
        self.fab.pack()

        # Bind window resize to update sidebar position
        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        # Update top bar height and sidebar position on window resize
        self.top_bar.update_idletasks()
        self.top_bar_height = self.top_bar.winfo_height()
        if self.sidebar_visible:
            self.sidebar.place_configure(
                x=0,
                y=self.top_bar_height,
                height=self.winfo_height() - self.top_bar_height,
            )
            self.top_bar.lift()

    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.animate_sidebar_out()
            self.menu_btn.configure(text="☰")
            self.sidebar_visible = False
        else:
            # Position the sidebar below the top bar
            self.sidebar.place(
                x=0,
                y=self.top_bar_height,
                height=self.winfo_height() - self.top_bar_height,
            )
            self.animate_sidebar_in()
            self.menu_btn.configure(text="✖")
            self.sidebar_visible = True
            # Ensure the top bar stays on top
            self.top_bar.lift()

    def animate_sidebar_in(self):
        self.sidebar.place(
            x=-200,
            y=self.top_bar_height,
            height=self.winfo_height() - self.top_bar_height,
        )
        self.sidebar.lift()
        self.top_bar.lift()  # Ensure top bar stays on top
        x = -200

        def slide():
            nonlocal x
            x += 20
            if x <= 0:
                self.sidebar.place_configure(x=x)
                self.top_bar.lift()  # Keep top bar on top during animation
                self.after(10, slide)

        slide()

    def animate_sidebar_out(self):
        x = 0

        def slide():
            nonlocal x
            x -= 20
            if x >= -200:
                self.sidebar.place_configure(x=x)
                self.top_bar.lift()  # Keep top bar on top during animation
                self.after(10, slide)
            else:
                self.sidebar.place_forget()

        slide()

    def create_sidebar(self, parent):
        # Add a small padding frame at the top to ensure content isn't too close to the edge
        padding_frame = tk.Frame(parent, bg=theme.get_color("surface"), height=10)
        padding_frame.pack(fill=tk.X)

        # Search section
        search_frame = ModernFrame(parent)
        search_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        search_label = ModernLabel(search_frame, text="🔍 Search:")
        search_label.pack(anchor=tk.W, pady=(0, 3))

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search)
        self.search_entry = ModernEntry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(fill=tk.X, pady=(0, 5))

        # Category filter
        category_label = ModernLabel(search_frame, text="🏷️ Category:")
        category_label.pack(anchor=tk.W, pady=(0, 3))

        self.category_filter = ttk.Combobox(
            search_frame, style="Modern.TCombobox", width=15
        )
        self.category_filter.pack(fill=tk.X)
        self.category_filter.bind("<<ComboboxSelected>>", self.on_category_filter)

    def create_editor_panel(self):
        # Editor header
        editor_header = ModernFrame(self.editor_panel)
        editor_header.pack(fill=tk.X, padx=10, pady=10)

        # Title bar with close button
        title_bar = ModernFrame(editor_header)
        title_bar.pack(fill=tk.X)

        title_label = ModernLabel(title_bar, style="title", text="✏️ Edit Note")
        title_label.pack(side=tk.LEFT)

        close_btn = ModernButton(
            title_bar,
            text="✖",
            style="secondary",
            font=("Segoe UI", 10),
            command=self.hide_editor,
            width=2,
        )
        close_btn.pack(side=tk.RIGHT)

        # Title and category
        form_frame = ModernFrame(editor_header)
        form_frame.pack(fill=tk.X, pady=5)

        title_label = ModernLabel(form_frame, text="📄 Title:")
        title_label.pack(anchor=tk.W, pady=(0, 3))
        self.title_entry = ModernEntry(form_frame)
        self.title_entry.pack(fill=tk.X, pady=(0, 5))

        cat_label = ModernLabel(form_frame, text="🏷️ Category:")
        cat_label.pack(anchor=tk.W, pady=(0, 3))
        self.category_entry = ModernEntry(form_frame)
        self.category_entry.pack(fill=tk.X)

        # Color tag selection
        color_label = ModernLabel(form_frame, text="🎨 Color Tag:")
        color_label.pack(anchor=tk.W, pady=(0, 3))
        self.color_var = tk.StringVar(value="default")
        color_options = ["default", "#ff9999", "#99ff99", "#9999ff"]
        self.color_menu = ttk.OptionMenu(
            form_frame, self.color_var, "default", *color_options
        )
        self.color_menu.pack(fill=tk.X)

        # Controls
        controls_frame = ModernFrame(editor_header)
        controls_frame.pack(fill=tk.X, pady=5)

        self.mode_button = ModernButton(
            controls_frame,
            text="📋 Switch to Tasks",
            command=self.toggle_mode,
            style="secondary",
        )
        self.mode_button.pack(side=tk.LEFT, padx=(0, 5))

        save_btn = ModernButton(
            controls_frame, text="💾 Save", command=self.save_note, style="primary"
        )
        save_btn.pack(side=tk.LEFT)

        delete_btn = ModernButton(
            controls_frame, text="🗑️ Delete", command=self.delete_note, style="danger"
        )
        delete_btn.pack(side=tk.LEFT, padx=5)

        self.timestamp_label = ModernLabel(controls_frame, style="caption", text="")
        self.timestamp_label.pack(side=tk.RIGHT)

        # Content area
        self.content_frame = ModernFrame(self.editor_panel)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def show_editor(self):
        self.editor_panel.lift()
        self.editor_visible = True
        # Fade-in animation (simulated)
        self.editor_panel.configure(bg=theme.get_color("surface"))
        self.content_frame.configure(bg=theme.get_color("surface"))
        alpha = 0

        def fade():
            nonlocal alpha
            alpha += 0.1
            if alpha <= 1:
                self.editor_panel.lift()
                self.after(50, fade)

        fade()

    def hide_editor(self):
        # Fade-out animation (simulated)
        alpha = 1

        def fade():
            nonlocal alpha
            alpha -= 0.1
            if alpha >= 0:
                self.after(50, fade)
            else:
                self.editor_panel.lower()
                self.current_note = None
                self.current_view = None
                self.editor_visible = False

        fade()

    def refresh_notes_grid(self):
        for widget in self.notes_frame.winfo_children():
            widget.destroy()
        search_query = self.search_var.get().strip()
        selected_category = self.category_filter.get()
        if search_query:
            notes = NotesDB.search_notes(search_query)
        else:
            notes = NotesDB.load_all_notes()
        self.notes_data = notes
        if selected_category and selected_category != "All":
            notes = [note for note in notes if note[2] == selected_category]
            self.notes_data = notes
        row = 0
        col = 0
        for note_id, title, category, modified_at, mode, pinned, color_tag in notes:
            card = NoteCard(
                self.notes_frame,
                note_id,
                title,
                category,
                modified_at,
                mode,
                color_tag,
                pinned,
                self.load_note,
                self.toggle_pin,
            )
            card.grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col >= 4:  # 4 cards per row
                col = 0
                row += 1
        categories = ["All"] + NotesDB.get_categories()
        self.category_filter["values"] = categories
        if not self.category_filter.get():
            self.category_filter.set("All")

    def on_search(self, *args):
        self.refresh_notes_grid()

    def on_category_filter(self, event=None):
        self.refresh_notes_grid()

    def load_note(self, note_id: int):
        note = NotesDB.load_note(note_id)
        if note:
            self.current_note = note
            self.color_var.set(note.color_tag)
            self.load_current_note()
            self.show_editor()

    def new_note(self):
        title = simpledialog.askstring("✨ New Note", "Enter note title:", parent=self)
        if title:
            note = Note(title=title)
            note_id = NotesDB.save_note(note)
            note.id = note_id
            self.current_note = note
            self.load_current_note()
            self.refresh_notes_grid()
            self.show_editor()

    def delete_note(self):
        if not self.current_note:
            messagebox.showwarning("⚠️ Warning", "No note to delete.", parent=self)
            return
        if messagebox.askyesno(
            "🗑️ Confirm Delete",
            "Are you sure you want to delete this note?\nThis action cannot be undone.",
            parent=self,
        ):
            NotesDB.delete_note(self.current_note.id)
            self.hide_editor()
            self.refresh_notes_grid()

    def toggle_pin(self, note_id: int):
        note = NotesDB.load_note(note_id)
        if note:
            note.pinned = not note.pinned
            NotesDB.save_note(note)
            self.refresh_notes_grid()

    def load_current_note(self):
        if not self.current_note:
            return
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, self.current_note.title)
        self.category_entry.delete(0, tk.END)
        self.category_entry.insert(0, self.current_note.category)
        self.color_var.set(self.current_note.color_tag)
        if self.current_note.created_at:
            try:
                created = datetime.fromisoformat(self.current_note.created_at)
                modified = datetime.fromisoformat(self.current_note.modified_at)
                timestamp_text = f"Created: {created.strftime('%m/%d/%Y %H:%M')} • Modified: {modified.strftime('%m/%d/%Y %H:%M')}"
                self.timestamp_label.config(text=timestamp_text)
            except:
                self.timestamp_label.config(text="")
        if self.current_note.mode == "normal":
            self.current_view = ModernNoteView(self.content_frame, self.current_note)
            self.mode_button.config(text="📋 Switch to Tasks")
        else:
            self.current_view = ModernTaskView(self.content_frame, self.current_note)
            self.mode_button.config(text="📝 Switch to Notes")
        self.current_view.pack(fill=tk.BOTH, expand=True)
        self.update_widget_theme(self.current_view)

    def toggle_mode(self):
        if not self.current_note:
            return
        if self.current_view and hasattr(self.current_view, "update_note"):
            self.current_view.update_note()
        self.current_note.mode = (
            "task" if self.current_note.mode == "normal" else "normal"
        )
        self.load_current_note()

    def save_note(self):
        if not self.current_note:
            messagebox.showwarning("⚠️ Warning", "No note to save.", parent=self)
            return
        self.current_note.title = self.title_entry.get().strip()
        self.current_note.category = self.category_entry.get().strip()
        self.current_note.color_tag = self.color_var.get()
        if not self.current_note.title:
            messagebox.showerror(
                "❌ Error", "Please enter a title for the note.", parent=self
            )
            return
        if self.current_view and hasattr(self.current_view, "update_note"):
            self.current_view.update_note()
        NotesDB.save_note(self.current_note)
        self.refresh_notes_grid()
        self.load_current_note()
        messagebox.showinfo("✅ Success", "Note saved successfully!", parent=self)

    def toggle_theme(self):
        theme.toggle_theme()
        NotesDB.save_setting("theme", theme.current_theme)
        self.apply_theme()

    def apply_theme(self):
        self.configure(bg=theme.get_color("bg"))
        self.main_container.configure(bg=theme.get_color("bg"))
        self.grid_container.configure(bg=theme.get_color("bg"))
        self.notes_canvas.configure(bg=theme.get_color("bg"))
        self.notes_frame.configure(bg=theme.get_color("bg"))
        self.sidebar.configure(bg=theme.get_color("surface"))
        self.editor_panel.configure(bg=theme.get_color("surface"))
        self.content_frame.configure(bg=theme.get_color("surface"))
        self.menu_btn.configure(
            bg=theme.get_color("surface_variant"),
            fg=theme.get_color("text"),
            activebackground=theme.get_color("hover"),
            activeforeground=theme.get_color("text"),
        )
        self.theme_btn.configure(text="🌙" if theme.current_theme == "light" else "☀️")
        self.fab.configure(
            bg=theme.get_color("primary"),
            fg="white",
            activebackground=theme.get_color("primary_variant"),
            activeforeground="white",
        )
        self.update_widget_theme(self)
        if self.current_note:
            self.load_current_note()

    def update_widget_theme(self, widget):
        widget_class = widget.__class__.__name__
        if isinstance(widget, (ModernFrame, GlassyFrame)):
            if isinstance(widget, ModernFrame):
                widget.configure(
                    bg=theme.get_color("surface"),
                )
            else:
                widget.configure(
                    bg=theme.get_color("surface_variant"),
                )
        elif isinstance(widget, ModernEntry):
            widget.configure(
                bg=theme.get_color("surface"),
                fg=theme.get_color("text"),
                insertbackground=theme.get_color("primary"),
                selectbackground=theme.get_color("primary"),
            )
        elif isinstance(widget, ModernText):
            widget.configure(
                bg=theme.get_color("surface"),
                fg=theme.get_color("text"),
                insertbackground=theme.get_color("primary"),
                selectbackground=theme.get_color("primary"),
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
        for child in widget.winfo_children():
            self.update_widget_theme(child)

    def on_closing(self):
        if self.current_note:
            self.current_note.title = self.title_entry.get().strip()
            self.current_note.category = self.category_entry.get().strip()
            self.current_note.color_tag = self.color_var.get()
            if self.current_view and hasattr(self.current_view, "update_note"):
                self.current_view.update_note()
            if self.current_note.title:
                NotesDB.save_note(self.current_note)
        self.destroy()


# ──────────────────────────────────────────────
# Enhanced Entry Point (Unchanged)
# ──────────────────────────────────────────────

if __name__ == "__main__":
    app = ModernNoteApp()
    try:
        app.iconbitmap("")
    except:
        pass
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.update_idletasks()
    width = app.winfo_width()
    height = app.winfo_height()
    x = (app.winfo_screenwidth() // 2) - (width // 2)
    y = (app.winfo_screenheight() // 2) - (height // 2)
    app.geometry(f"{width}x{height}+{x}+{y}")
    app.mainloop()
