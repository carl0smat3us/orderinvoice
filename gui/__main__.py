import os

import requests
from dotenv import load_dotenv
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QFileDialog, QGridLayout, QLabel,
                             QLineEdit, QMainWindow, QPushButton, QTableWidget,
                             QTableWidgetItem, QVBoxLayout, QWidget)

load_dotenv()


class InvoiceGenerator(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("Invoice Generator")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #212121;")

        # Create the central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a vertical layout
        self.layout = QVBoxLayout()
        central_widget.setLayout(self.layout)

        # Add sections
        self.search_reference_section()
        self.client_information_section()
        self.invoice_details_section()
        self.download_invoice_section()

    def search_reference_section(self):
        # Create a grid layout for the search section
        search_layout = QGridLayout()

        # Add reference label
        referenceLabel = QLabel("Reference:")
        referenceLabel.setFont(QFont("Arial", 14))
        referenceLabel.setStyleSheet("color: white;")
        search_layout.addWidget(referenceLabel, 0, 0, alignment=Qt.AlignLeft)

        # Add entry field
        self.referenceInput = QLineEdit()
        self.referenceInput.setFont(QFont("Arial", 12))
        self.referenceInput.setStyleSheet(
            """
            color: white;
            border: 2px solid white;
            padding: 5px;
            """
        )
        search_layout.addWidget(self.referenceInput, 0, 1)

        # Add button
        search_button = QPushButton("Search")
        search_button.setFont(QFont("Arial", 12))
        search_button.setStyleSheet(
            """
            color: white;
            background-color: #4CAF50;
            border: none;
            padding: 8px;
            """
        )
        search_button.clicked.connect(self.on_search_clicked)
        search_layout.addWidget(search_button, 0, 2)

        self.layout.addLayout(search_layout)

    def client_information_section(self):
        # Client information title
        clientTitle = QLabel("Client Information")
        clientTitle.setFont(QFont("Arial", 16))
        clientTitle.setStyleSheet("color: #FFD700;")
        self.layout.addWidget(clientTitle, alignment=Qt.AlignLeft)

        # Client details
        self.clientDetails = QLabel("")
        self.clientDetails.setFont(QFont("Arial", 14))
        self.clientDetails.setStyleSheet("color: white;")
        self.layout.addWidget(self.clientDetails, alignment=Qt.AlignLeft)

    def invoice_details_section(self):
        # Invoice details title
        invoiceTitle = QLabel("Invoice Details")
        invoiceTitle.setFont(QFont("Arial", 16))
        invoiceTitle.setStyleSheet("color: #FFD700;")
        self.layout.addWidget(invoiceTitle, alignment=Qt.AlignLeft)

        # Create a table for invoice details
        self.invoiceTable = QTableWidget()
        self.invoiceTable.setColumnCount(4)
        self.invoiceTable.setHorizontalHeaderLabels(
            ["Product Name", "Unit Price", "Quantity", "Total Price"]
        )
        self.invoiceTable.setStyleSheet(
            """
            QTableWidget { 
                background-color: #333; 
                color: white; 
                gridline-color: #555; 
            }
            QHeaderView::section { 
                background-color: #444; 
                color: white; 
                font-weight: bold; 
            }
            """
        )
        self.layout.addWidget(self.invoiceTable)

    def download_invoice_section(self):
        self.download_button = QPushButton("Download invoice")
        self.download_button.setFont(QFont("Arial", 12))
        self.download_button.setStyleSheet(
            """
            color: white;
            background-color: #505050;
            border: none;
            padding: 8px;
            """
        )
        self.download_button.clicked.connect(self.download_invoice)
        self.layout.addWidget(self.download_button, alignment=Qt.AlignLeft)

    def download_invoice(self):
        self.download_button.setText("Downloading...")
        self.download_button.setEnabled(False)

        try:
            response = requests.get(
                f"http://localhost:8000/invoice/{self.referenceInput.text().strip()}?api-key={os.getenv('API_KEY')}",
                stream=True,
            )

            if response.status_code == 200:
                save_path, _ = QFileDialog.getSaveFileName(
                    self,
                    "Save Invoice",
                    f"invoice_{self.referenceInput.text().strip()}.pdf",
                    "PDF Files (*.pdf)",
                )

                if save_path:
                    with open(save_path, "wb") as pdf_file:
                        for chunk in response.iter_content(chunk_size=8192):
                            pdf_file.write(chunk)
                    self.clientDetails.setText("Invoice downloaded successfully!")
                else:
                    self.clientDetails.setText("Download canceled.")
            else:
                self.clientDetails.setText("Error: Unable to download invoice.")
        except Exception as e:
            self.clientDetails.setText("Error: Unable to connect to the server.")
            print(f"Error during download: {e}")
        finally:
            self.download_button.setText("Download invoice")
            self.download_button.setEnabled(True)

    def on_search_clicked(self):
        # Fetch the reference entered by the user
        reference = self.referenceInput.text().strip()

        if not reference:
            self.download_button.setEnabled(False)
            self.clientDetails.setText("Error: Please enter a valid reference.")
            return

        self.download_button.setEnabled(True)

        try:
            response = requests.get(
                f"http://localhost:8000/data/{reference}?api-key={os.getenv('API_KEY')}"
            )
            if response.status_code == 200:
                invoice_data = response.json()
                self.populate_client_information(invoice_data)
                self.populate_invoice_details(invoice_data)

                self.download_button.setStyleSheet(
                    """
                    color: white;
                    background-color: #4CAF50;
                    border: none;
                    padding: 8px;
                    """
                )
            else:
                self.clientDetails.setText("Error: Invoice not found.")
                self.clear_invoice_table()
                self.download_button.setStyleSheet(
                    """
                    color: white;
                    background-color: #505050;
                    border: none;
                    padding: 8px;
                    """
                )
        except Exception as e:
            self.clientDetails.setText("Error: Unable to connect to the server.")
            print(f"Error: Unable to connect to the server. {e}")

            self.clear_invoice_table()
            self.download_button.setStyleSheet(
                """
                color: white;
                background-color: #505050;
                border: none;
                padding: 8px;
                """
            )

    def populate_client_information(self, invoice_data):
        # Populate client information section
        client_info = (
            f"Name: {invoice_data['name']}\n"
            f"Phone: {invoice_data['phone']}\n"
            f"Address: {invoice_data['address']}"
        )
        self.clientDetails.setText(client_info)

    def populate_invoice_details(self, invoice_data):
        # Populate the invoice details table
        products = invoice_data["products"]
        self.invoiceTable.setRowCount(len(products))
        for row, product in enumerate(products):
            self.invoiceTable.setItem(row, 0, QTableWidgetItem(product["name"]))
            self.invoiceTable.setItem(
                row, 1, QTableWidgetItem(str(product["unit_price"]))
            )
            self.invoiceTable.setItem(
                row, 2, QTableWidgetItem(str(product["quantity"]))
            )
            self.invoiceTable.setItem(
                row, 3, QTableWidgetItem(str(product["total_price"]))
            )

    def clear_invoice_table(self):
        # Clear the invoice table
        self.invoiceTable.setRowCount(0)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = InvoiceGenerator()
    window.show()
    sys.exit(app.exec_())
