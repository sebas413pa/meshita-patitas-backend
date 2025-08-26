from sqlalchemy import Column, Integer, Text, ForeignKey
from app.database import Base

class Imagen(Base):
    __tablename__ = "imagenes"

    id_imagen = Column(Integer, primary_key=True, index=True)
    url_imagen = Column(Text, nullable=False)
    id_animal = Column(Integer, ForeignKey("animales.id_animal"), nullable=True)
    id_campania = Column(Integer, ForeignKey("campanias.id_campania"), nullable=True)
