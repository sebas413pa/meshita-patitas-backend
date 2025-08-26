from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import SessionLocal
from app.models.campania import Campania
from app.schemas.campania import CampaniaCreate, CampaniaResponse
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from typing import List, Optional
import shutil, os, uuid
from sqlalchemy.orm import Session
from app.models.imagen import Imagen

router = APIRouter(prefix="/campanias", tags=["campanias"])

UPLOAD_DIR = "app/static/imagenes"  
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=CampaniaResponse)
def crear_campania_con_imagenes(
    campania: CampaniaCreate = Depends(CampaniaCreate.as_form),
    files: List[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    db_campania = Campania(**campania.dict())
    db.add(db_campania)
    db.commit()
    db.refresh(db_campania)

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
                    id_campania=db_campania.id_campania
                )
                db.add(imagen)

            except Exception as e:
                print(f"Error procesando {file.filename}: {e}")

        db.commit()

    return db_campania

@router.get("/", response_model=list[CampaniaResponse])
def obtener_campanias(db: Session = Depends(get_db)):
    return db.query(Campania).filter(Campania.estado != 0).all()


@router.get("/{id_campania}", response_model=CampaniaResponse)
def obtener_campania(id_campania: int, db: Session = Depends(get_db)):
    campania = db.query(Campania).filter(Campania.id_campania == id_campania).first()
    if not campania:
        raise HTTPException(status_code=404, detail="Campaña no encontrada")
    return campania

@router.put("/{id_campania}", response_model=CampaniaResponse)
def actualizar_campania_con_imagenes(
    id_campania: int,
    campania: CampaniaCreate = Depends(CampaniaCreate.as_form),
    files: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db)
):
    db_campania = db.query(Campania).filter(Campania.id_campania == id_campania).first()
    if not db_campania:
        raise HTTPException(status_code=404, detail="Campaña no encontrada")

    # Actualizar campos
    for key, value in campania.dict(exclude_unset=True).items():
        setattr(db_campania, key, value)

    db_campania.updated_at = datetime.now()

    # Guardar nuevas imágenes si vienen
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
                    id_campania=db_campania.id_campania
                )
                db.add(nueva_imagen)

            except Exception as e:
                print(f"Error al guardar imagen {file.filename}: {e}")

    db.commit()
    db.refresh(db_campania)
    return db_campania

@router.put("/{id_campania}/estado")
def eliminar_campania(id_campania: int, db: Session = Depends(get_db)):
    db_campania = db.query(Campania).filter(Campania.id_campania == id_campania).first()
    if not db_campania:
        raise HTTPException(status_code=404, detail="Campaña no encontrada")

    # Cambiar estado
    db_campania.estado = 0

    # Eliminar imágenes asociadas
    imagenes = db.query(Imagen).filter(Imagen.id_campania == id_campania).all()
    eliminadas = 0
    for imagen in imagenes:
        ruta = os.path.join("app", imagen.url_imagen)
        if os.path.exists(ruta):
            try:
                os.remove(ruta)
            except Exception as e:
                print(f"Error al borrar {ruta}: {e}")
        db.delete(imagen)
        eliminadas += 1

    db.commit()
    db.refresh(db_campania)

    return {
        "mensaje": "Campaña eliminada lógicamente (estado = 0)",
        "imagenes_eliminadas": eliminadas
    }