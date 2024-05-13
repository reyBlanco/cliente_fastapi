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

key="$2a$12$HoLJeoXZNJXZo3defenEDuyv7vquFdm/SZ6waakoQSjHEm3WoH1Jy"
j_wt=""

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
    global j_wt
    j_wt="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc190b2tlbiI6Inl1cmVjdWFybyJ9.5NtVFIP9DzPoFnneeTmMVJq8KLIPXYdQsOSfRK_oyUk"
    
    if not crypt.verify(password,key):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="contraseña incorrecta")
    return j_wt



@app.get("/")
async def home():
    return {"mensaje":"hola les saluda Jesus desde el servidor fastapi"}

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
    
    if j_wt==datos_json.get("mensaje"):

        await m_ws.escuchador_retransmision(ws)
    else:
        await ws.send_json({"mensaje":"acceso denegado"})
        await ws.close()
        m_ws.removerClienteDesconectado(ws)