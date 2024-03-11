from weasyprint import CSS
from datetime import datetime
import os

OUTPUT_FILENAME = f"output-{datetime.now().strftime('%d-%b-%Y')}"
TEMPLATE_HTML_PATH = os.path.join(os.getcwd(), "templates", "index.html")

TEMPLATE_CSS = [CSS(os.path.join(os.getcwd(), "static", "invoice.css"))]
