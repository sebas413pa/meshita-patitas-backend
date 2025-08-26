from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id_usuario = Column(Integer, primary_key=True, index=True)
    usuario = Column(String(100), unique=True, nullable=False)
    contrasenia = Column(String(100), nullable=False)
    rol_usuario = Column(Integer, nullable=False)
    id_colaborador = Column(Integer,ForeignKey("colaboradores.id_colaborador"))
    id_pregunta = Column(Integer,ForeignKey("preguntas_seguridad.id_pregunta"))
    respuesta_pregunta = Column(String(200))
    estado = Column(Boolean, default = True)

    pregunta = relationship("Pregunta",backref="usuarios")
    colaborador = relationship("Colaborador",backref="colaboradores")