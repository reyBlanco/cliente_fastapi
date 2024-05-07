from pydantic import BaseModel
from typing import Optional

class Caballero_del_zodiaco(BaseModel):
    nombre:Optional[str]
    constelacion:Optional[str]
    dios:Optional[str]
