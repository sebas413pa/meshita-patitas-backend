from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session 
from app.database import SessionLocal
from app.models.pregunta_seguridad import Pregunta
from app.schemas.pregunta_seguridad import PreguntaBase, PreguntaResponse, PreguntaCreate

router = APIRouter(prefix="/preguntas",tags=["preguntas"])
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
@router.post("/", response_model=PreguntaResponse)
def crear_pregunta(pregunta:PreguntaCreate, db: Session = Depends(get_db)):
    pregunta_data = pregunta.dict()

    db_pregunta = Pregunta(**pregunta_data)
    db.add(db_pregunta)
    db.commit()
    db.refresh(db_pregunta)
    return db_pregunta

@router.get("/{id_pregunta}", response_model = PreguntaResponse)
def obtener_preguntas_id(id_pregunta: int, db: Session = Depends(get_db)):
    db_pregunta = db.query(Pregunta).filter(Pregunta.id_pregunta == id_pregunta).first()
    if not db_pregunta: 
        raise HTTPException(status_code=404, detail="Colaborador no encontrado")
    return db_pregunta

@router.get("/", response_model =list[PreguntaResponse])
def obtener_preguntas(db: Session = Depends(get_db)):
    return db.query(Pregunta).all()

@router.put("/{id_pregunta}",response_model= PreguntaResponse)
def actualizar_pregunta(id_pregunta:int,pregunta:PreguntaCreate, db:Session = Depends(get_db)):
    db_pregunta = db.query(Pregunta).filter(Pregunta.id_pregunta == id_pregunta).first()

    if not db_pregunta:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    
    for key, value in pregunta.dict(exclude_unset=True).items():
        setattr(db_pregunta, key, value)
    
    db.commit()
    db.refresh(db_pregunta)
    return db_pregunta
