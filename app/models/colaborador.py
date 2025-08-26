from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class Colaborador(Base):
    __tablename__ = "colaboradores"

    id_colaborador = Column(Integer, primary_key=True, index=True)
    nombres = Column(String(100), nullable = False)
    apellidos = Column(String(100),nullable=False)
    correo_electronico = Column(String(100),nullable=False,unique=True)
    telefono = Column(String(20), nullable =  True)
    estado = Column(Boolean, default = True)