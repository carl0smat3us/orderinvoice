from dotenv import load_dotenv
load_dotenv()

import api.config.firebase
from fastapi import FastAPI, Security, HTTPException
from firebase_admin import db
from api.utils.secure import get_api_key

app = FastAPI()


@app.get("/invoice/{order_id}")
async def invoice(order_id: str, _:str = Security(get_api_key)):
    ref = db.reference(f'/orders/{order_id}')
    order = ref.get()
    if order == None:
        raise HTTPException(status_code=404, detail="O pedido pretendido não foi encontrado")
    return order

@app.get("/")
def root(_:str = Security(get_api_key)):
    return {"message": "Welcome to the RACIUS CARE INVOICE API!"}