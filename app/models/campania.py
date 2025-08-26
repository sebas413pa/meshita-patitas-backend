from sqlalchemy import Column, Integer, String, Date, DateTime,Text, func
from app.database import Base
from sqlalchemy.orm import relationship

class Campania(Base):
    __tablename__ = "campanias"
    
    id_campania = Column(Integer, primary_key=True, index=True)
    nombre_campania = Column(String(100), unique=False, nullable=False)
    descripcion_campania = Column(Text)
    fecha_realizacion = Column(Date, nullable=True)
    hora = Column(String, nullable=True)
    lugar = Column(String(100), nullable=True)
    estado = Column(Integer, nullable=False)
    telefono = Column(String(20), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now(), nullable=False)
    imagenes = relationship("Imagen", backref="campania")