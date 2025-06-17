import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from dataclasses import dataclass
from typing import List, Optional
import sqlite3
from datetime import datetime


# ──────────────────────────────────────────────
# Database Setup
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

    conn.commit()
    conn.close()


# ──────────────────────────────────────────────
# Models
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
# Database Operations
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


# ──────────────────────────────────────────────
# Views
# ──────────────────────────────────────────────


class NoteView(tk.Frame):
    def __init__(self, master, note):
        super().__init__(master)
        self.note = note

        # Text widget with scrollbar
        text_frame = tk.Frame(self)
        text_frame.pack(fill=tk.BOTH, expand=True)

        self.text = tk.Text(text_frame, wrap=tk.WORD, font=("Arial", 11))
        scrollbar = ttk.Scrollbar(
            text_frame, orient=tk.VERTICAL, command=self.text.yview
        )
        self.text.configure(yscrollcommand=scrollbar.set)

        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text.insert("1.0", self.note.content)

    def update_note(self):
        self.note.content = self.text.get("1.0", tk.END).strip()


class TaskView(tk.Frame):
    def __init__(self, master, note):
        super().__init__(master)
        self.note = note
        self.entries = []

        # Scrollable frame for tasks
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.render_tasks()

    def render_tasks(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.entries = []

        # Add existing tasks
        for i, task in enumerate(self.note.tasks):
            task_frame = tk.Frame(self.scrollable_frame)
            task_frame.pack(fill=tk.X, padx=10, pady=2)

            var = tk.BooleanVar(value=task.done)
            cb = tk.Checkbutton(
                task_frame,
                text=task.content,
                variable=var,
                command=self.update_task_states,
                wraplength=400,
                justify=tk.LEFT,
            )
            cb.pack(side=tk.LEFT, fill=tk.X, expand=True)
            cb.config(
                fg="gray" if task.done else "black",
                font=("Arial", 10, "overstrike" if task.done else "normal"),
            )

            # Delete button
            del_btn = tk.Button(
                task_frame,
                text="×",
                command=lambda idx=i: self.delete_task(idx),
                fg="red",
                width=2,
                height=1,
            )
            del_btn.pack(side=tk.RIGHT)

            self.entries.append((task, var))

        # Add new task entry
        entry_frame = tk.Frame(self.scrollable_frame)
        entry_frame.pack(fill=tk.X, padx=10, pady=5)

        self.new_entry = tk.Entry(entry_frame, font=("Arial", 10))
        self.new_entry.pack(fill=tk.X)
        self.new_entry.bind("<Return>", self.add_task)

        add_btn = ttk.Button(entry_frame, text="Add Task", command=self.add_task)
        add_btn.pack(pady=2)

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
# Main Application
# ──────────────────────────────────────────────


class NoteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Advanced Note Taking App")
        self.geometry("900x700")

        # Initialize database
        init_database()

        self.current_note = None
        self.current_view = None

        self.create_ui()
        self.refresh_notes_list()

    def create_ui(self):
        # Main container with paned window
        main_paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Left panel - Notes list
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=1)

        # Search and controls
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Category filter
        category_frame = ttk.Frame(left_frame)
        category_frame.pack(fill=tk.X, padx=5, pady=2)

        ttk.Label(category_frame, text="Category:").pack(side=tk.LEFT)
        self.category_filter = ttk.Combobox(category_frame, width=15)
        self.category_filter.pack(side=tk.LEFT, padx=5)
        self.category_filter.bind("<<ComboboxSelected>>", self.on_category_filter)

        # Notes list
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Listbox with scrollbar
        list_container = tk.Frame(list_frame)
        list_container.pack(fill=tk.BOTH, expand=True)

        self.notes_listbox = tk.Listbox(list_container)
        list_scrollbar = ttk.Scrollbar(
            list_container, orient=tk.VERTICAL, command=self.notes_listbox.yview
        )
        self.notes_listbox.configure(yscrollcommand=list_scrollbar.set)

        self.notes_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.notes_listbox.bind("<Double-Button-1>", self.on_note_select)

        # Left panel buttons
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(btn_frame, text="New Note", command=self.new_note).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(btn_frame, text="Delete", command=self.delete_note).pack(
            side=tk.LEFT, padx=2
        )

        # Right panel - Note editor
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=2)

        # Top controls for note editor
        self.editor_frame = ttk.Frame(right_frame)
        self.editor_frame.pack(fill=tk.BOTH, expand=True)

        self.top_frame = ttk.Frame(self.editor_frame)
        self.top_frame.pack(fill=tk.X, padx=10, pady=5)

        # Title
        title_frame = ttk.Frame(self.top_frame)
        title_frame.pack(fill=tk.X, pady=2)

        ttk.Label(title_frame, text="Title:").pack(side=tk.LEFT)
        self.title_entry = ttk.Entry(title_frame)
        self.title_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Category
        cat_frame = ttk.Frame(self.top_frame)
        cat_frame.pack(fill=tk.X, pady=2)

        ttk.Label(cat_frame, text="Category:").pack(side=tk.LEFT)
        self.category_entry = ttk.Entry(cat_frame)
        self.category_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Control buttons
        ctrl_frame = ttk.Frame(self.top_frame)
        ctrl_frame.pack(fill=tk.X, pady=5)

        self.mode_button = ttk.Button(
            ctrl_frame, text="Switch to Tasks", command=self.toggle_mode
        )
        self.mode_button.pack(side=tk.LEFT, padx=2)

        ttk.Button(ctrl_frame, text="💾 Save", command=self.save_note).pack(
            side=tk.LEFT, padx=2
        )

        # Timestamps
        self.timestamp_label = ttk.Label(ctrl_frame, text="", font=("Arial", 8))
        self.timestamp_label.pack(side=tk.RIGHT)

        # Content area
        self.content_frame = ttk.Frame(self.editor_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.show_welcome_message()

    def show_welcome_message(self):
        """Show welcome message when no note is selected."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        welcome_label = ttk.Label(
            self.content_frame,
            text="Select a note or create a new one to start editing",
            font=("Arial", 12),
            foreground="gray",
        )
        welcome_label.pack(expand=True)

    def refresh_notes_list(self):
        """Refresh the notes list and category filter."""
        self.notes_listbox.delete(0, tk.END)

        # Get search query and category filter
        search_query = self.search_var.get().strip()
        selected_category = self.category_filter.get()

        if search_query:
            notes = NotesDB.search_notes(search_query)
        else:
            notes = NotesDB.load_all_notes()

        # Filter by category if selected
        if selected_category and selected_category != "All":
            notes = [note for note in notes if note[2] == selected_category]

        # Update listbox
        for note_id, title, category, modified_at, mode in notes:
            display_text = f"{title}"
            if category:
                display_text += f" [{category}]"
            if mode == "task":
                display_text += " 📋"

            # Add timestamp
            try:
                dt = datetime.fromisoformat(modified_at)
                time_str = dt.strftime("%m/%d %H:%M")
                display_text += f" - {time_str}"
            except:
                pass

            self.notes_listbox.insert(tk.END, display_text)
            # Store note_id as a reference
            self.notes_listbox.insert(tk.END, f"ID:{note_id}")
            self.notes_listbox.delete(
                tk.END
            )  # Remove the ID line (just used for reference)

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
        if not selection:
            return

        # Get note ID from the selected item
        # We need to parse this from our display format
        notes = NotesDB.load_all_notes()
        if selection[0] < len(notes):
            note_id = notes[selection[0]][0]
            self.load_note(note_id)

    def new_note(self):
        """Create a new note."""
        title = simpledialog.askstring("New Note", "Enter note title:")
        if title:
            note = Note(title=title)
            note_id = NotesDB.save_note(note)
            note.id = note_id
            self.current_note = note
            self.load_current_note()
            self.refresh_notes_list()

    def delete_note(self):
        """Delete the selected note."""
        selection = self.notes_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a note to delete.")
            return

        if messagebox.askyesno(
            "Confirm Delete", "Are you sure you want to delete this note?"
        ):
            notes = NotesDB.load_all_notes()
            if selection[0] < len(notes):
                note_id = notes[selection[0]][0]
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
        """Load the current note into the editor."""
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

        # Update timestamps
        if self.current_note.created_at:
            try:
                created = datetime.fromisoformat(self.current_note.created_at)
                modified = datetime.fromisoformat(self.current_note.modified_at)
                timestamp_text = f"Created: {created.strftime('%m/%d/%Y %H:%M')} | Modified: {modified.strftime('%m/%d/%Y %H:%M')}"
                self.timestamp_label.config(text=timestamp_text)
            except:
                self.timestamp_label.config(text="")

        # Create appropriate view
        if self.current_note.mode == "normal":
            self.current_view = NoteView(self.content_frame, self.current_note)
            self.mode_button.config(text="Switch to Tasks")
        else:
            self.current_view = TaskView(self.content_frame, self.current_note)
            self.mode_button.config(text="Switch to Notes")

        self.current_view.pack(fill=tk.BOTH, expand=True)

    def toggle_mode(self):
        """Toggle between normal and task mode."""
        if not self.current_note:
            return

        # Update content before switching
        if self.current_view and hasattr(self.current_view, "update_note"):
            self.current_view.update_note()

        # Toggle mode
        self.current_note.mode = (
            "task" if self.current_note.mode == "normal" else "normal"
        )

        # Reload the view
        self.load_current_note()

    def save_note(self):
        """Save the current note."""
        if not self.current_note:
            messagebox.showwarning("Warning", "No note to save.")
            return

        # Update note data from form
        self.current_note.title = self.title_entry.get().strip()
        self.current_note.category = self.category_entry.get().strip()

        if not self.current_note.title:
            messagebox.showerror("Error", "Please enter a title for the note.")
            return

        # Update content if in normal mode
        if self.current_view and hasattr(self.current_view, "update_note"):
            self.current_view.update_note()

        # Save to database
        NotesDB.save_note(self.current_note)

        # Refresh UI
        self.refresh_notes_list()
        self.load_current_note()  # Refresh timestamps

        messagebox.showinfo("Success", "Note saved successfully!")


# ──────────────────────────────────────────────
# Entry Point
# ──────────────────────────────────────────────

if __name__ == "__main__":
    app = NoteApp()
    app.mainloop()
