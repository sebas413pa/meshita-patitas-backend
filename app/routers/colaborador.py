from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.colaborador import Colaborador
from app.schemas.colaborador import ColaboradorBase, ColaboradorUpdate, ColaboradorCreate,ColaboradorResponse
from passlib.context import CryptContext
from app.models.pregunta_seguridad import Pregunta
router = APIRouter(prefix="/colaboradores", tags = ["colaboradores"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ColaboradorResponse)
def crear_colaborador(colaborador:ColaboradorCreate, db:Session = Depends(get_db)):
    colaborador_data = colaborador.dict()
    db_colaborador = Colaborador(**colaborador_data)
    db.add(db_colaborador)
    db.commit()
    db.refresh(db_colaborador)
    return db_colaborador

@router.get("/",response_model = list[ColaboradorResponse])
def obtener_colaboradores(db: Session = Depends(get_db)):
    return db.query(Colaborador).filter(Colaborador.estado == True).all()

@router.get("/{id_colaborador}",response_model=ColaboradorResponse)
def obtener_colaborador_por_id(id_colaborador: int, db: Session = Depends(get_db)):
    db_colaborador = db.query(Colaborador).filter(Colaborador.estado == True, Colaborador.id_colaborador == id_colaborador).first()
    if not db_colaborador:
        raise HTTPException(status_code=404, detail="Colaborador no encontrado")
    return db_colaborador

@router.put("/{id_colaborador}", response_model=ColaboradorResponse)
def actualizar_usuario(id_colaborador: int, colaborador: ColaboradorUpdate, db: Session = Depends(get_db)):
    db_colaborador = db.query(Colaborador).filter(Colaborador.id_colaborador == id_colaborador).first()
    if not db_colaborador:
        raise HTTPException(status_code=404, detail="Colaborador no encontrado")
    
    for key, value in colaborador.dict(exclude_unset=True).items():
        setattr(db_colaborador, key, value)
    
    db.commit()
    db.refresh(db_colaborador)
    return db_colaborador

@router.delete("/{id_colaborador}", response_model=ColaboradorResponse)
def eliminar_usuario_logico(id_colaborador: int, db: Session = Depends(get_db)):
    colaborador = db.query(Colaborador).filter(Colaborador.id_colaborador == id_colaborador).first()
    if not colaborador:
        raise HTTPException(status_code=404, detail="Colaborador no encontrado")
    
    colaborador.estado = False
    db.commit()
    db.refresh(colaborador)
    return JSONResponse(content={"mensaje":"Colaborador eliminado correctamente"}, status_code=200)