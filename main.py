from fastapi import FastAPI,Depends,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import status
from pydantic import BaseModel
from ManagerWebSocket import *
from jose import jwt
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from passlib.context import CryptContext



class Caballero_del_zodiaco(BaseModel):
    nombre:Optional[str]
    constelacion:Optional[str]
    dios:Optional[str]



app=FastAPI()
m_ws=ManagerWebSocket()

oauth2=OAuth2PasswordBearer(tokenUrl="/login")
crypt=CryptContext(schemes=["bcrypt"])

contaseña="$2a$12$11nk4jG2pkGMzOqx9EzQdO57CX2623hKZgLemoMOYw7UQ1PCwDyme"
pass_acces="michoacan"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET","POST","PUT","DELETE"],
    allow_headers=["*"],
    allow_credentials=True,

)

@app.post("/login")
async def login(form:OAuth2PasswordRequestForm = Depends()):
    password=form.password

    if not crypt.verify(password,contaseña):
        return {"mensaje":"contraseña incorrecta"}
    
    key_acces=pass_acces

    return {"password":key_acces,"token_type":"bearer"}



@app.get("/")
async def home():
    return {"mensaje":"hola les saluda Jesus desde el servidor fastapi$%&"}

@app.post("/enviar")
async def enviar(caballero:Caballero_del_zodiaco):
    diccionario_caballero=dict(caballero)
    print(diccionario_caballero)
    sys.stdout.flush()
    return {"mensaje":"paquete recivido"}

@app.websocket("/ws")
async def wSocket(ws:WebSocket):
    await m_ws.conectar(ws)
    datos_json:dict=await ws.receive_json()
    
    if pass_acces==datos_json.get("constelacion"):


        await m_ws.escuchador_retransmision(ws)
    else:
        await ws.send_json({"mensaje":"acceso denegado"})
        await ws.close()
        await m_ws.removerClienteDesconectado(ws)

