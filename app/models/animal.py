from sqlalchemy import Column, Integer, String, Date, DECIMAL, Enum
from app.database import Base
import enum
from sqlalchemy.orm import relationship

class SexoEnum(enum.Enum):
    macho = "macho"
    hembra = "hembra"

class TamanioEnum(enum.Enum):
    pequenio = "pequenio"
    mediano = "mediano"
    grande = "grande"


class Animal(Base):
    __tablename__ = "animales"
    
    id_animal = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=False, nullable=False)
    edad_aproximada = Column(String(100), nullable=True)
    tamanio_aproximado = Column(Enum(TamanioEnum), nullable=False)
    raza = Column(String(100), nullable=True)
    descripcion_general = Column(String(100), nullable=True)
    descripcion_veterinaria = Column(String(100), nullable=True)
    fecha_ingreso = Column(Date, nullable=True)
    fecha_egreso = Column(Date, nullable=True)
    sexo = Column(Enum(SexoEnum), nullable=False)  
    estado = Column(Integer, nullable=False)
    peso_aproximado = Column(DECIMAL, nullable=True)
    imagenes = relationship("Imagen", backref="animal")