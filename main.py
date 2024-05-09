from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import status
from pydantic import BaseModel
from ManagerWebSocket import *


class Caballero_del_zodiaco(BaseModel):
    nombre:Optional[str]
    constelacion:Optional[str]
    dios:Optional[str]



app=FastAPI()
m_ws=ManagerWebSocket()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET","POST","PUT","DELETE"],
    allow_headers=["*"],
    allow_credentials=True,

)

@app.get("/")
async def home():
    return {"mensaje":"hola les saluda Jesus desde el servidor fastapi#"}

@app.post("/enviar")
async def enviar(caballero:Caballero_del_zodiaco):
    diccionario_caballero=dict(caballero)
    print(diccionario_caballero)
    sys.stdout.flush()
    return {"mensaje":"paquete recivido"}

@app.websocket("/ws")
async def wSocket(ws:WebSocket):
    await m_ws.conectar(ws)
    await m_ws.escuchador_retransmision(ws)
