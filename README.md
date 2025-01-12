# Invoice Generator
Automated invoice generation in an e-commerce scenario.

![Gui Screenshot](https://github.com/user-attachments/assets/591c26c2-e205-4818-a7a6-4827d141738c)
![Invoice example](https://github.com/user-attachments/assets/e48bbe74-6968-42bb-b851-e2e7871415b5)

You can check the full invoice PDF [here](https://github.com/user-attachments/files/18389705/invoice_1.pdf).

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
