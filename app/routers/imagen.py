from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
import shutil
import os
from app.database import SessionLocal
from app.models.imagen import Imagen
from app.schemas.imagen import ImagenResponse

router = APIRouter(prefix="/imagenes", tags=["imagenes"])

UPLOAD_DIR = "app/static/imagenes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ImagenResponse)
def subir_imagen(
    file: UploadFile = File(...),
    id_animal: int = Form(None),
    id_campania: int = Form(None),
    db: Session = Depends(get_db)
):
    try:
        filepath = os.path.join(UPLOAD_DIR, file.filename)
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        url_relative = f"static/imagenes/{file.filename}"
        imagen = Imagen(url_imagen=url_relative, id_animal=id_animal, id_campania=id_campania)
        db.add(imagen)
        db.commit()
        db.refresh(imagen)
        return imagen
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir la imagen: {str(e)}")

from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
import shutil
import os
from app.database import SessionLocal
from app.models.imagen import Imagen
from app.schemas.imagen import ImagenResponse

router = APIRouter(prefix="/imagenes", tags=["imagenes"])

UPLOAD_DIR = "app/static/imagenes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[ImagenResponse])
def obtener_imagenes(db: Session = Depends(get_db)):
    imagenes = db.query(Imagen).all()
    return imagenes

@router.delete("/{id_imagen}")
def eliminar_imagen(id_imagen: int, db: Session = Depends(get_db)):
    imagen = db.query(Imagen).filter(Imagen.id_imagen == id_imagen).first()
    if not imagen:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    filepath = os.path.join("app", imagen.url_imagen)
    print(filepath)
    if os.path.exists(filepath):
        os.remove(filepath)

    db.delete(imagen)
    db.commit()

    return {"mensaje": "Imagen eliminada correctamente"}


@router.post("/", response_model=ImagenResponse)
def subir_imagen(
    file: UploadFile = File(...),
    id_animal: int = Form(None),
    id_campania: int = Form(None),
    db: Session = Depends(get_db)
):
    try:
        filepath = os.path.join(UPLOAD_DIR, file.filename)
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        url_relative = f"static/imagenes/{file.filename}"
        imagen = Imagen(url_imagen=url_relative, id_animal=id_animal, id_campania=id_campania)
        db.add(imagen)
        db.commit()
        db.refresh(imagen)
        return imagen
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir la imagen: {str(e)}")