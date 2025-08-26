from pydantic import BaseModel
from typing import Optional
from datetime import date
from datetime import datetime
from fastapi import Form
from typing import List
from .imagen import ImagenResponse

class CampaniaBase(BaseModel):
    nombre_campania: str
    descripcion_campania: str
    fecha_realizacion: Optional[date] = None
    hora: Optional[str] = None
    lugar: Optional[str] = None
    estado: int
    telefono: Optional[str] = None

class CampaniaCreate(BaseModel):
    nombre_campania: str
    descripcion_campania: str
    fecha_realizacion: Optional[date]
    hora: Optional[str]
    lugar: Optional[str]
    estado: int
    telefono: Optional[str]

    @classmethod
    def as_form(
        cls,
        nombre_campania: str = Form(...),
        descripcion_campania: str = Form(...),
        fecha_realizacion: Optional[date] = Form(None),
        hora: Optional[str] = Form(None),
        lugar: Optional[str] = Form(None),
        estado: int = Form(...),
        telefono: Optional[str] = Form(None),
    ):
        return cls(
            nombre_campania=nombre_campania,
            descripcion_campania=descripcion_campania,
            fecha_realizacion=fecha_realizacion,
            hora=hora,
            lugar=lugar,
            estado=estado,
            telefono=telefono,
        )

class CampaniaResponse(CampaniaBase):
    id_campania: int
    created_at: datetime
    updated_at: datetime
    imagenes: List[ImagenResponse] = []

    class Config:
        orm_mode = True