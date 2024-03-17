from dotenv import load_dotenv

load_dotenv()

import api.config.firebase
from fastapi import FastAPI, Security, HTTPException
from fastapi.responses import FileResponse
from firebase_admin import db
from api.utils.secure import get_api_key
from api.utils.invoice import render_template
from api.settings import *

from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import datetime

origins = [
    "https://cuddly-meme-jww47799jrj2q6v7-3000.app.github.dev",
    "https://raciuscare.com",
    "https://raciuscare.vercel.app",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="/tmp/")



@app.get("/invoice/{order_id}")
async def invoice(order_id: str, _=Security(get_api_key)):
    ref = db.reference(f"/orders/{order_id}")
    order = ref.get()

    if order == None:
        raise HTTPException(
            status_code=404, detail="O pedido pretendido não foi encontrado"
        )

    context_data = ref.get()
    context_data["order_id"] = order_id

    data_string = context_data["createdAt"]
    format = "%Y-%m-%dT%H:%M:%S.%fZ"

    tt = datetime.datetime.strptime(data_string, format)
    formatted_time = tt.strftime("%Y-%m-%d %H:%M")

    context_data["createdAt"] = formatted_time
    template_html: str

    with open(TEMPLATE_HTML_PATH) as template:
        template_html = template.read()
    template_url = render_template(
        template_html, context_data, TEMPLATE_CSS, OUTPUT_FILENAME
    )

    response = FileResponse(
        template_url,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"inline; filename=${template_url.replace('/tmp', '')}"
        },
    )
    return response


@app.get("/")
def root(_=Security(get_api_key)):
    return {"message": "Welcome to the RACIUS CARE INVOICE API!"}
