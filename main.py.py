from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import status
import sys
from pydantic import BaseModel
from typing import Optional


class Caballero_del_zodiaco(BaseModel):
    nombre:Optional[str]
    constelacion:Optional[str]
    dios:Optional[str]



app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET","POST","PUT","DELETE"],
    allow_headers=["*"],
    allow_credentials=True,

)

@app.get("/")
async def home():
    return {"mensaje":"hola les saluda Jesus desde el servidor fastapi"}

@app.post("/enviar")
async def enviar(caballero:Optional[Caballero_del_zodiaco]):
    diccionario_caballero=dict(caballero)
    print(diccionario_caballero)
    sys.stdout.flush()
    return {"mensaje":"paquete recivido"}