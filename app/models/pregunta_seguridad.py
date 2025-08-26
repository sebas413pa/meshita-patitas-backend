from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class Pregunta(Base):
    __tablename__ = "preguntas_seguridad"

    id_pregunta = Column(Integer, primary_key = True, index = True)
    pregunta = Column(String(250), unique=True,nullable= False)

