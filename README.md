# Invoice Generator

## Main Technologies

- Python
- FastAPI
- WeasyPrint
- Jinja2
- PyQt5
- SQLite3
- Docker

## Getting Started

1. **Install Poetry**

   You can learn how to install Poetry on your computer by visiting [this link](https://python-poetry.org/docs/main#installation).

2. **Activate the virtual environment**

   ```bash
   poetry shell
   ```

3. **Create a `.env.local` file** in the root directory based on the `env.example` file.

4. **Install PyQt5 using pip through Poetry**

   ```bash
   poetry run pip install pyqt5-qt5
   ```

5. **Install all dependencies**

   ```bash
   poetry install
   ```

6. **Populate the database**

   ```bash
   task seed
   ```

7. **Run the server**

   ```bash
   task run
   ```

8. **Run the GUI in another tab**

   ```bash
   task gui
   ```

9. **Still Working 😊**
