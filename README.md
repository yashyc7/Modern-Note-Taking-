# Modern Notes

**Modern Notes** is a sleek, feature-rich desktop note-taking application built with Python and Tkinter. Designed for Windows, it offers a modern, user-friendly interface with light and dark themes, supporting both traditional note-taking and task management. The app uses SQLite for persistent storage and is compiled into a standalone executable using PyInstaller for easy distribution.

## Features

### Core Functionality
- **Note Creation and Management**: Create, edit, save, and delete notes with titles and optional categories.
- **Task Lists**: Switch between standard notes and task list modes for managing to-do items with checkboxes.
- **Persistent Storage**: Notes and tasks are saved in a local SQLite database (`notes.db`), ensuring data persists across sessions.
- **Search and Filter**: Search notes by title or content and filter by category for quick access.
- **Categories**: Assign categories to notes for better organization, with a dynamic category filter in the sidebar.
- **Timestamps**: Automatically track creation and modification dates for each note, displayed in a clean format.

### Modern User Interface
- **Light and Dark Themes**: Toggle between light and dark themes with a single click, with preferences saved in the database.
- **Glassy Design**: Features a modern, glassy UI with subtle transparency effects for frames and panels.
- **Custom Widgets**: Includes styled buttons, entries, text areas, listboxes, and labels with hover effects and theme integration.
- **Responsive Layout**: Uses a sidebar for note navigation and a main editor panel, with a resizable window (minimum 900x600 pixels).
- **Welcome Screen**: Displays a visually appealing welcome message with a quick action button to create new notes when no note is selected.
- **Smooth Transitions**: Animated-like transitions when switching between note and task modes or toggling themes.

### Task Management
- **Task View**: Add, edit, mark as done, or delete tasks within a note, with a scrollable task list.
- **Interactive Checkboxes**: Tasks have modern checkboxes that toggle completion status, with strikethrough text for completed tasks.
- **Add Task Interface**: A dedicated input field and button for adding new tasks, with Enter key support for quick entry.

### Technical Features
- **SQLite Database**: Stores notes, tasks, and settings in a lightweight, file-based database.
- **Data Classes**: Uses Python dataclasses for clean, type-hinted note and task models.
- **Theme Management**: Centralized theme configuration with a `ThemeManager` class for consistent color application.
- **PyInstaller Support**: Compiled into a standalone `.exe` for Windows, bundling all dependencies for easy distribution.
- **Error Handling**: Includes validation (e.g., requiring a note title) and confirmation dialogs for destructive actions like deletion.
- **Auto-Save on Close**: Automatically saves the current note when closing the app, if it has a title.

## Installation

### Prerequisites
- **Windows Operating System**: The app is compiled as a Windows executable.
- **Python 3.12 or 3.13** (for development or running from source):
  - Required for compatibility with `pyinstaller` and other dependencies.

### Running the Pre-Built Executable
1. **Download the Latest Release**:
   - Visit the [Releases page](https://github.com/your-username/note-taking-app/releases) on GitHub.
   - Download the latest `NoteTakingApp-vX.Y.Z.exe` file (e.g., `NoteTakingApp-v1.0.0.exe`).
2. **Run the Executable**:
   - Double-click the `.exe` file to launch the app.
   - The app will create a `notes.db` file in the same directory to store your notes.
3. **Optional: Move the Executable**:
   - Place the `.exe` in a dedicated folder to keep the database and app together.

### Running from Source
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/note-taking-app.git
   cd note-taking-app
   ```
2. **Install Poetry**:
   - Follow the [Poetry installation guide](https://python-poetry.org/docs/#installation).
3. **Install Dependencies**:
   ```bash
   poetry install
   ```
4. **Run the App**:
   ```bash
   poetry run python app.py
   ```
5. **Build Your Own Executable** (Optional):
   ```bash
   poetry run pyinstaller --onefile --name NoteTakingApp app.py
   ```
   - Find the executable in the `dist` folder.

## Usage

1. **Launch the App**:
   - Run the `.exe` or start from source with `poetry run python app.py`.
   - The app opens with a welcome screen and a sidebar for note management.

2. **Create a Note**:
   - Click **New Note** in the sidebar or welcome screen.
   - Enter a title in the dialog and click **OK**.
   - Add content in the editor or switch to task mode with **Switch to Tasks**.

3. **Manage Tasks**:
   - In task mode, add tasks using the input field and **Add** button or Enter key.
   - Check tasks to mark them as done (strikethrough applied).
   - Delete tasks with the **×** button.

4. **Organize Notes**:
   - Assign a category in the editor’s category field.
   - Filter notes by category using the sidebar’s dropdown.
   - Search notes by typing in the search bar.

5. **Save and Delete**:
   - Click **Save** to store changes (auto-saved on app close if titled).
   - Select a note and click **Delete** to remove it (confirmation required).

6. **Toggle Themes**:
   - Click the theme button (🌙/☀️) in the header to switch between light and dark modes.
   - Theme preference is saved automatically.

## Project Structure

```
note-taking-app/
├── app.py          # Main application script
├── notes.db        # SQLite database (generated on first run)
├── pyproject.toml  # Poetry configuration and dependencies
├── README.md       # Project documentation
├── dist/           # PyInstaller output (contains .exe)
└── CHANGELOG.md    # Version history (recommended)
```

## Dependencies
- **Python Libraries** (managed via Poetry):
  - `tkinter`: For the GUI (included in Python standard library).
  - `sqlite3`: For database storage (included in Python standard library).
  - `ruff`: For linting and code formatting.
  - `pyinstaller`: For compiling the app into a Windows executable.
- See `pyproject.toml` for version constraints.

## Building the Executable
To create a new `.exe`:
```bash
poetry run pyinstaller --onefile --name NoteTakingApp app.py
```
- The executable is generated in `dist/NoteTakingApp.exe`.
- Ensure Python 3.12 or 3.13 is used due to `pyinstaller` compatibility.

## Releasing on GitHub
1. Update the version in `pyproject.toml` (e.g., `version = "1.0.0"`).
2. Commit changes and tag the release:
   ```bash
   git commit -am "Bump version to 1.0.0"
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin main v1.0.0
   ```
3. Create a release on GitHub with `dist/NoteTakingApp.exe`:
   ```bash
   gh release create v1.0.0 dist/NoteTakingApp.exe -t "v1.0.0" -n "Initial release with note and task features"
   ```

## Contributing
Contributions are welcome! Please:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -am "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact
- **Author**: Yash Chauhan
- **Email**: yashc9411407582@gmail.com
- **GitHub**: [yashyc7](https://github.com/yashyc7)

---

*✨ Start taking notes with style using Modern Notes!*