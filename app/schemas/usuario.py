from pydantic import BaseModel
from typing import Optional  # Importar Optional

class UsuarioBase(BaseModel):
    usuario: str    
    contrasenia: str
    rol_usuario: int 
    id_colaborador: int
    id_pregunta: int
    respuesta_pregunta: str

class UsuarioPreguntaResponse(BaseModel):
    id_usuario: int
    id_pregunta: int
    respuesta_pregunta: str  # sí, el hash

    class Config:
        orm_mode = True
        
class RestaurarContraseniaRequest(BaseModel):
    id_usuario: int
    respuesta_pregunta: str
    nueva_contrasenia: str

class UsuarioCreate(UsuarioBase):
    contrasenia: str  

class UsuarioUpdate(BaseModel):
    usuario: Optional[str] = None
    contrasenia: Optional[str] = None
    rol_usuario: Optional[int] = None
    id_colaborador: Optional[int] = None
    id_pregunta: Optional[int] = None
    respuesta_pregunta: Optional[str] = None

class UsuarioResponse(UsuarioBase):
    id_usuario: int
    model_config = {
        "from_attributes": True
    }