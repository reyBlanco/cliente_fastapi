from pydantic import BaseModel

class Caballero_del_zodiaco(BaseModel):
    nombre:str
    constelacion:str
    dios:str
