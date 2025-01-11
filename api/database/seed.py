import os
import sqlite3
from datetime import datetime

from config import DATABASE_PATH, connect, execute


def seed_database():
    try:
        # Insert data into the Client table
        execute(
            """
            INSERT INTO Client (client_id, name, phone, address)
            VALUES
            (1, 'John Smith', '+33 xx3 x21 63x', 'ABC Street'),
            (2, 'Davison Star', '+33 7xx 93x x05', 'DEF Street');
        """
        )

        # Insert data into the Product table
        execute(
            """
            INSERT INTO Product (product_id, name, unit_price)
            VALUES
            (1, 'Product A', 2500.00),
            (2, 'Product B', 1500.00),
            (3, 'Product C', 3500.00);
        """
        )

        # Insert data into the Invoice table with formatted dates
        execute(
            """
            INSERT INTO Invoice (invoice_id, client_id, reference, created_at, total_price)
            VALUES
            (1, 1, 'INV001', ?, 5000.00),
            (2, 2, 'INV002', ?, 3500.00);
        """,
            (
                datetime(2025, 1, 11, 10, 0, 0, 123456).strftime(
                    "%Y-%m-%dT%H:%M:%S.%fZ"
                ),
                datetime(2025, 1, 12, 15, 30, 0, 654321).strftime(
                    "%Y-%m-%dT%H:%M:%S.%fZ"
                ),
            ),
        )

        # Insert data into the InvoiceProduct table (relating products to invoices)
        execute(
            """
            INSERT INTO InvoiceProduct (invoice_product_id, invoice_id, product_id, quantity, total_price)
            VALUES
            (1, 1, 1, 1, 2500.00),
            (2, 1, 2, 1, 1500.00),
            (3, 2, 2, 1, 1500.00),
            (4, 2, 3, 1, 3500.00);
        """
        )

        print("Database seeded successfully!")

    except sqlite3.Error as e:
        print(f"Error occurred while seeding database: {e}")


# Run the seed function
if __name__ == "__main__":
    # Delete db if exists
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)

    connect()
    seed_database()
