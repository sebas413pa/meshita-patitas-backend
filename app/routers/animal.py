import os
import shutil
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.animal import Animal
from app.schemas.animal import AnimalCreate, AnimalResponse
from typing import Optional, List
import shutil, os
from app.models.imagen import Imagen
from fastapi import UploadFile, File, Depends, APIRouter
from app.models.imagen import Imagen
import shutil, os

router = APIRouter(prefix="/animales", tags=["animales"])
UPLOAD_DIR = "app/static/imagenes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=AnimalResponse)
def crear_animal_con_imagenes(
    animal: AnimalCreate = Depends(AnimalCreate.as_form),
    files: list[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    db_animal = Animal(**animal.dict())
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)

    if files:
        for file in files:
            try:
                if not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
                    continue  

                unique_filename = f"{uuid.uuid4().hex}_{file.filename}"
                filepath = os.path.join(UPLOAD_DIR, unique_filename)
                with open(filepath, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)

                imagen = Imagen(
                    url_imagen=f"static/imagenes/{unique_filename}",
                    id_animal=db_animal.id_animal
                )
                db.add(imagen)
            except Exception as e:
                print(f"Error al procesar el archivo {file.filename}: {e}")

        db.commit()

    return db_animal


@router.get("/", response_model=list[AnimalResponse])
def obtener_animals(
    db: Session = Depends(get_db),
    tamanio: Optional[str] = None,
    sexo: Optional[str] = None
):
    query = db.query(Animal).filter(Animal.estado == 1)  # Filtrar por estado = 1
    
    if tamanio:
        query = query.filter(Animal.tamanio_aproximado == tamanio)
    
    if sexo:
        query = query.filter(Animal.sexo == sexo)
    
    animals = query.all()
    return animals

@router.get("/{id_animal}", response_model=AnimalResponse)
def obtener_animal_por_id(id_animal: int, db: Session = Depends(get_db)):
    db_animal = db.query(Animal).filter(Animal.id_animal == id_animal, Animal.estado == 1).first()  # Filtrar por estado = 1
    if not db_animal:
        raise HTTPException(status_code=404, detail="Animal no encontrado o no disponible")
    return db_animal


@router.put("/{id_animal}", response_model=AnimalResponse)
def actualizar_animal_con_imagenes(
    id_animal: int,
    animal: AnimalCreate = Depends(AnimalCreate.as_form),
    files: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db)
):
    db_animal = db.query(Animal).filter(Animal.id_animal == id_animal).first()
    if not db_animal:
        raise HTTPException(status_code=404, detail="Animal no encontrado")

    for key, value in animal.dict(exclude_unset=True).items():
        setattr(db_animal, key, value)

    if files:
        for file in files:
            try:
                if not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
                    continue

                unique_filename = f"{uuid.uuid4().hex}_{file.filename}"
                filepath = os.path.join("app/static/imagenes", unique_filename)
                with open(filepath, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)

                nueva_imagen = Imagen(
                    url_imagen=f"static/imagenes/{unique_filename}",
                    id_animal=db_animal.id_animal
                )
                db.add(nueva_imagen)
            except Exception as e:
                print(f"Error al guardar imagen {file.filename}: {e}")

    db.commit()
    db.refresh(db_animal)
    return db_animal

from app.schemas.animal import EstadoUpdate

@router.put("/{id_animal}/estado", response_model=AnimalResponse)
def cambiar_estado_animal(id_animal: int, estado_update: EstadoUpdate, db: Session = Depends(get_db)):
    db_animal = db.query(Animal).filter(Animal.id_animal == id_animal).first()
    if not db_animal:
        raise HTTPException(status_code=404, detail="Animal no encontrado")
    
    nuevo_estado = estado_update.estado
    db_animal.estado = nuevo_estado

    if nuevo_estado in [0, 2]:
        imagenes = db.query(Imagen).filter(Imagen.id_animal == id_animal).all()
        for imagen in imagenes:
            ruta_archivo = os.path.join("app", imagen.url_imagen)
            if os.path.exists(ruta_archivo):
                os.remove(ruta_archivo)
            
            db.delete(imagen)

    db.commit()
    db.refresh(db_animal)
    return db_animal