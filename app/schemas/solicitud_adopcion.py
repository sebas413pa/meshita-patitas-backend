from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SolicitudBase(BaseModel):
    nombre_adoptante: str
    apellido_adoptante: str
    telefono_adoptante: str
    correo_electronico_adoptante: str
    id_animal: Optional[int] = None
    id_colaborador: Optional[int] = None
    id_campania: Optional[int] = None
    descripcion: Optional[str] = None
    estado: Optional[int] = 0

class SolicitudCreate(SolicitudBase):
    pass

class SolicitudUpdate(BaseModel):
    nombre_adoptante: Optional[str] = None
    apellido_adoptante: Optional[str] = None
    correo_electronico: Optional[str] = None
    telefono: Optional[str] = None
    id_animal: Optional[int] = None
    id_colaborador: Optional[int] = None
    id_campania: Optional[int] = None
    descripcion: Optional[str] = None

    
class SolicitudResponse(SolicitudBase):
    id_solicitud: int
    created_at: datetime
    model_config = {
        "from_attributes": True
    }