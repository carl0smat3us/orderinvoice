-- Table to store client information
CREATE TABLE IF NOT EXISTS Client (
    client_id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    address VARCHAR(255)
);

-- Table to store invoice information
CREATE TABLE IF NOT EXISTS Invoice (
    invoice_id INTEGER PRIMARY KEY,
    client_id INTEGER NOT NULL,
    reference VARCHAR(50) NOT NULL,
    created_at DATE NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (client_id) REFERENCES Client(client_id)
);

-- Table to store product information
CREATE TABLE IF NOT EXISTS Product (
    product_id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL
);

-- Table to link products and invoices
CREATE TABLE IF NOT EXISTS InvoiceProduct (
    invoice_product_id INTEGER PRIMARY KEY,
    invoice_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (invoice_id) REFERENCES Invoice(invoice_id),
    FOREIGN KEY (product_id) REFERENCES Product(product_id)
);

