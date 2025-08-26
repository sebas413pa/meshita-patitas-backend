from pydantic import BaseModel
from typing import Optional
from datetime import date
from decimal import Decimal
from enum import Enum
from fastapi import Form
from typing import List
from .imagen import ImagenResponse

# Enum para reflejar el Enum de SQLAlchemy
class SexoEnum(str, Enum):
    macho = "macho"
    hembra = "hembra"

class TamanioEnum(str, Enum):
    pequenio = "pequenio"
    mediano = "mediano"
    grande = "grande"

# Base común
class AnimalBase(BaseModel):
    nombre: str
    edad_aproximada: Optional[str] = None
    tamanio_aproximado: TamanioEnum
    raza: Optional[str] = None
    descripcion_general: Optional[str] = None
    descripcion_veterinaria: Optional[str] = None
    fecha_ingreso: Optional[date] = None
    fecha_egreso: Optional[date] = None
    sexo: SexoEnum
    estado: int
    peso_aproximado: Optional[Decimal] = None

class AnimalCreate(BaseModel):
    nombre: str
    edad_aproximada: Optional[str]
    raza: Optional[str]
    tamanio_aproximado: TamanioEnum
    descripcion_general: Optional[str]
    descripcion_veterinaria: Optional[str]
    fecha_ingreso: Optional[date]
    fecha_egreso: Optional[date]
    sexo: SexoEnum
    estado: int
    peso_aproximado: Optional[float]

    @classmethod
    def as_form(
        cls,
        nombre: str = Form(...),
        edad_aproximada: Optional[str] = Form(None),
        tamanio_aproximado: TamanioEnum = Form(...),
        raza: Optional[str] = Form(None),
        descripcion_general: Optional[str] = Form(None),
        descripcion_veterinaria: Optional[str] = Form(None),
        fecha_ingreso: Optional[date] = Form(None),
        fecha_egreso: Optional[date] = Form(None),
        sexo: SexoEnum = Form(...),
        estado: int = Form(...),
        peso_aproximado: Optional[float] = Form(None),
    ):
        return cls(
            nombre=nombre,
            edad_aproximada=edad_aproximada,
            tamanio_aproximado= tamanio_aproximado,
            raza=raza,
            descripcion_general=descripcion_general,
            descripcion_veterinaria=descripcion_veterinaria,
            fecha_ingreso=fecha_ingreso,
            fecha_egreso=fecha_egreso,
            sexo=sexo,
            estado=estado,
            peso_aproximado=peso_aproximado,
        )


# Modelo para respuesta con ID incluido y configuración ORM
class AnimalResponse(AnimalBase):
    id_animal: int
    imagenes: List[ImagenResponse] = []

    class Config:
        orm_mode = True

class EstadoUpdate(BaseModel):
    estado: int