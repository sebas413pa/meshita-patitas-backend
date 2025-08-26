from pydantic import BaseModel 
from typing import Optional

class ColaboradorBase(BaseModel):
    nombres: str
    apellidos: str
    correo_electronico: str
    telefono: Optional[str] = None

class ColaboradorCreate(ColaboradorBase):
    pass
    
class ColaboradorUpdate(BaseModel):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    correo_electronico: Optional[str] = None
    telefono: Optional[str] = None

class ColaboradorResponse(ColaboradorBase):
    id_colaborador: int
    model_config = {
        "from_attributes": True
    }