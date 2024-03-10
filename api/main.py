from dotenv import load_dotenv

load_dotenv()

import api.config.firebase
from fastapi import FastAPI, Security, HTTPException
from firebase_admin import db
from api.utils.secure import get_api_key
from api.utils.invoice import render_template
from api.settings import *

import os, json

app = FastAPI()


@app.get("/invoice/{order_id}")
async def invoice(order_id: str, _: str = Security(get_api_key)):
    ref = db.reference(f"/orders/{order_id}")
    order = ref.get()

    if order == None:
        raise HTTPException(
            status_code=404, detail="O pedido pretendido não foi encontrado"
        )

    context_data = {}
    with open(os.path.join(os.getcwd(), "api", "data.json")) as data:
        context_data = get_context_data(json.load(data))

    template_html = ""
    with open(TEMPLATE_HTML_PATH) as template:
        template_html = template.read()
    return render_template(template_html, context_data, TEMPLATE_CSS, OUTPUT_FILENAME)


@app.get("/")
def root(_: str = Security(get_api_key)):
    return {"message": "Welcome to the RACIUS CARE INVOICE API!"}
