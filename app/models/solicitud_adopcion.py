from sqlalchemy import Column, Integer, String, Boolean, Text,ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Solicitud_Adopcion(Base):

    __tablename__ = "solicitudes_adopcion"

    id_solicitud = Column(Integer, primary_key = True, index = True)
    nombre_adoptante = Column(String(100), nullable = False)
    apellido_adoptante = Column(String(100), nullable = False)
    telefono_adoptante = Column(String(20),nullable = False)
    correo_electronico_adoptante = Column(String(100), nullable = False)
    descripcion = Column(Text, nullable = False)
    estado = Column(Integer, default = 0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(),default = func.now())
    id_animal = Column(Integer, ForeignKey("animales.id_animal"),nullable = True)
    id_colaborador = Column(Integer,ForeignKey("colaboradores.id_colaborador"), nullable= True) 
    id_campania = Column(Integer, ForeignKey("campanias.id_campania"),nullable = True)
    colaborador = relationship("Colaborador", backref="solicitudes_adopcion")
    animal = relationship("Animal", backref="animales")
    campania = relationship("Campania", backref="campanias") 