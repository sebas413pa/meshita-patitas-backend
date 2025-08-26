from pydantic import BaseModel
from typing import Optional

class PreguntaBase(BaseModel):
    pregunta:str

class PreguntaCreate(PreguntaBase):
    pregunta:str

class PreguntaResponse(PreguntaBase):
    id_pregunta: int
    model_config = {
        "from_attributes": True
    }
