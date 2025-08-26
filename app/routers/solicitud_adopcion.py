from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.solicitud_adopcion import Solicitud_Adopcion
from app.schemas.solicitud_adopcion import SolicitudUpdate,SolicitudBase,SolicitudCreate, SolicitudResponse 
from app.models.animal import Animal
from app.models.campania import Campania
from app.models.colaborador import Colaborador
router = APIRouter(prefix="/solicitudes", tags =["solicitudes"])

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

@router.post("/",response_model = SolicitudResponse)
def crear_solicitud(solicitud: SolicitudCreate, db:Session = Depends(get_db)):
    print("Solicitud:", solicitud)
    animal = db.query(Animal).filter(Animal.id_animal == solicitud.id_animal).first()
    campania = db.query(Campania).filter(Campania.id_campania == solicitud.id_campania).first()
    colaborador = db.query(Colaborador).filter(Colaborador.id_colaborador == solicitud.id_colaborador).first()
    # if not animal:
    #     raise HTTPException(status_code=400, detail="Animal no valido")
    # elif not campania:
    #     raise HTTPException(status_code=400, detail="Campania no valida")
    solicitud_data = solicitud.dict()
    db_solicitud = Solicitud_Adopcion(**solicitud_data)
    db.add(db_solicitud)
    db.commit()
    db.refresh(db_solicitud)
    return db_solicitud

@router.put("/revisar/{id_solicitud}", response_model=SolicitudResponse)
def marcar_revisada(id_solicitud: int, db: Session = Depends(get_db)):
    solicitud = db.query(Solicitud_Adopcion).filter(Solicitud_Adopcion.id_solicitud == id_solicitud).first()
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    solicitud.estado = 1  # Revisada
    db.commit()
    db.refresh(solicitud)
    return solicitud

@router.put("/aceptar/{id_solicitud}", response_model=SolicitudResponse)
def aceptar_solicitud(id_solicitud: int, db: Session = Depends(get_db)):
    solicitud = db.query(Solicitud_Adopcion).filter(Solicitud_Adopcion.id_solicitud == id_solicitud).first()
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    solicitud.estado = 2  # Aceptada
    db.commit()
    db.refresh(solicitud)
    return solicitud

@router.put("/rechazar/{id_solicitud}", response_model=SolicitudResponse)
def rechazar_solicitud(id_solicitud: int, db: Session = Depends(get_db)):
    solicitud = db.query(Solicitud_Adopcion).filter(Solicitud_Adopcion.id_solicitud == id_solicitud).first()
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    solicitud.estado = 3  # Rechazada
    db.commit()
    db.refresh(solicitud)
    return solicitud
@router.get("/adopciones", response_model=list[SolicitudResponse])
def obtener_solicitudes_adopcion(db: Session = Depends(get_db)):
    solicitudes = db.query(Solicitud_Adopcion).filter(Solicitud_Adopcion.id_campania == None).all()
    return solicitudes

@router.get("/donaciones", response_model=list[SolicitudResponse])
def obtener_solicitudes_donacion(db: Session = Depends(get_db)):
    solicitudes = db.query(Solicitud_Adopcion).filter(Solicitud_Adopcion.id_animal == None).all()
    return solicitudes

@router.get("/adopciones/{id_colaborador}", response_model=list[SolicitudResponse])
def obtener_solicitudes_por_colaborador(id_colaborador: int, db: Session = Depends(get_db)):
    solicitudes = db.query(Solicitud_Adopcion).filter(Solicitud_Adopcion.id_colaborador == id_colaborador, Solicitud_Adopcion.id_campania == None).all()
    return solicitudes

@router.get("/donaciones/{id_colaborador}", response_model=list[SolicitudResponse])
def obtener_solicitudes_donacion_por_colaborador(id_colaborador: int, db: Session = Depends(get_db)):
    solicitudes = db.query(Solicitud_Adopcion).filter(Solicitud_Adopcion.id_colaborador == id_colaborador, Solicitud_Adopcion.id_animal == None).all()
    return solicitudes

@router.get("/estado/{estado}", response_model=list[SolicitudResponse])
def obtener_solicitudes_por_estado(estado: int, db: Session = Depends(get_db)):
    solicitudes = db.query(Solicitud_Adopcion).filter(Solicitud_Adopcion.estado == estado).all()
    return solicitudes

@router.get("/",response_model=list[SolicitudResponse])
def obtener_solicitudes(db: Session = Depends(get_db)):
    return db.query(Solicitud_Adopcion).all()

@router.get("/{id_solicitud}",response_model=SolicitudResponse)
def obtener_solicitud_por_id(id_solicitud: int, db:Session = Depends(get_db)):
    db_solicitud = db.query(Solicitud_Adopcion).filter(Solicitud_Adopcion.estado == 1, Solicitud_Adopcion.id_solicitud ==id_solicitud).first()
    if not db_solicitud:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_solicitud

@router.put("/{id_solicitud}", response_model=SolicitudResponse)
def actualizar_solicitud(id_solicitud: int, solicitud: SolicitudUpdate, db: Session = Depends(get_db)):
    db_solicitud = db.query(Solicitud_Adopcion).filter(Solicitud_Adopcion.id_solicitud == id_solicitud).first()
    if not db_solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    for key, value in solicitud.dict(exclude_unset=True).items():
        setattr(db_solicitud,key,value)
    db.commit()
    db.refresh(db_solicitud)
    return db_solicitud

@router.delete("/{id_solicitud}",response_model = SolicitudResponse)
def eliminar_solicitud_logico(id_solicitud: int, db: Session = Depends(get_db)):
    solicitud = db.query(Solicitud_Adopcion).filter(Solicitud_Adopcion.id_solicitud == id_solicitud).first()
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    
    solicitud.estado = 0
    db.commit()
    db.refresh(solicitud)
    return JSONResponse(content={"mensaje":"Solicitud eliminada correctamente"}, status_code=200)