from pydantic import BaseModel
from typing import Optional


class ImagenBase(BaseModel):
    id_animal: Optional[int] = None
    id_campania: Optional[int] = None

class ImagenCreate(ImagenBase):
    pass  

class ImagenResponse(ImagenBase):
    id_imagen: int
    url_imagen: str

    class Config:
        orm_mode = True
