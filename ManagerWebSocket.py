from fastapi.websockets import *
from typing import Optional
import sys

class ManagerWebSocket:
    def __init__(self):
        self.listaConectados:list[WebSocket]=[]
    
    async def conectar(self,wsCliente:Optional[WebSocket]):
        await wsCliente.accept()
        self.listaConectados.append(wsCliente)
    
    async def removerClienteDesconectado(self,wsCliente:Optional[WebSocket]):
        await self.listaConectados.remove(wsCliente)
    
    async def broadCast(self,datos:Optional[dict]):
        for ws in self.listaConectados:
            await ws.send_json(datos)

    async def escuchador_retransmision(self,ws:Optional[WebSocket]):
        while True:
            try:
                diccionario_datos=await ws.receive_json()
                print(f"datos:{diccionario_datos} de:{ws.url} No: {len(self.listaConectados)}")
                
                await self.broadCast(diccionario_datos)
                sys.stdout.flush()
            
            except WebSocketDisconnect as mensaje:
                print(f"se desconecto:{mensaje}")
                sys.stdout.flush()
                break
        
        await self.removerClienteDesconectado(ws)