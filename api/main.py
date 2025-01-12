import datetime

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates

from api.database.config import connect, execute
from api.settings import OUTPUT_FILENAME, TEMPLATE_CSS, TEMPLATE_HTML_PATH
from api.utils.invoice import render_template
from api.utils.secure import get_api_key

# Load environment variables
load_dotenv()

# Database intialization
connect()

# CORS settings
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app = FastAPI(dependencies=[Depends(get_api_key)])
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="/tmp/")


@app.get("/data/{order_id}")
async def invoice_data(order_id: str):
    # Query the Invoice table for the specific order_id
    order = execute("SELECT * FROM Invoice WHERE invoice_id = ?", (order_id,))

    if order is None:
        raise HTTPException(status_code=404, detail="Invoice not found")

    order = dict(order)

    client = dict(
        execute("SELECT * FROM Client WHERE client_id = ?", (order["client_id"],))
    )

    invoice_products = execute(
        "SELECT * from InvoiceProduct WHERE invoice_id = ?",
        (order["invoice_id"],),
        fetchall=True,
    )

    products = []

    for product in list(invoice_products):
        product = dict(product)

        product_data = dict(
            execute(
                "SELECT * FROM Product WHERE product_id = ?",
                (product["product_id"],),
            )
        )

        products.append(
            {
                "name": product_data["name"],
                "unit_price": product_data["unit_price"],
                "quantity": product["quantity"],
                "total_price": product["total_price"],
            }
        )

    tt = datetime.datetime.strptime(order["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
    order["created_at"] = tt.strftime("%Y-%m-%d %H:%M")

    # Prepare template context data
    context_data = {
        "name": client["name"],
        "phone": client["phone"],
        "address": client["address"],
        "reference": order["reference"],
        "created_at": order["created_at"],
        "products": products,
        "total_price": order["total_price"],
    }

    return context_data


@app.get("/invoice/{order_id}")
async def invoice(order_id: str):
    # Query the Invoice table for the specific order_id
    order = execute("SELECT * FROM Invoice WHERE invoice_id = ?", (order_id,))

    if order is None:
        raise HTTPException(status_code=404, detail="Invoice not found")

    order = dict(order)

    client = dict(
        execute("SELECT * FROM Client WHERE client_id = ?", (order["client_id"],))
    )

    invoice_products = execute(
        "SELECT * from InvoiceProduct WHERE invoice_id = ?",
        (order["invoice_id"],),
        fetchall=True,
    )

    products = []

    for product in list(invoice_products):
        product = dict(product)

        product_data = dict(
            execute(
                "SELECT * FROM Product WHERE product_id = ?",
                (product["product_id"],),
            )
        )

        products.append(
            {
                "name": product_data["name"],
                "unit_price": product_data["unit_price"],
                "quantity": product["quantity"],
                "total_price": product["total_price"],
            }
        )

    tt = datetime.datetime.strptime(order["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
    order["created_at"] = tt.strftime("%Y-%m-%d %H:%M")

    # Prepare template context data
    context_data = {
        "name": client["name"],
        "phone": client["phone"],
        "address": client["address"],
        "reference": order["reference"],
        "created_at": order["created_at"],
        "products": products,
        "total_price": order["total_price"],
    }

    # Read the HTML template
    with open(TEMPLATE_HTML_PATH) as template:
        template_html = template.read()

    # Render the template
    template_url = render_template(
        template_html, context_data, TEMPLATE_CSS, OUTPUT_FILENAME
    )

    # Create the PDF response
    response = FileResponse(
        template_url,
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename={OUTPUT_FILENAME}"},
    )

    return response


@app.get("/")
def root():
    return {"message": "Welcome back!"}
