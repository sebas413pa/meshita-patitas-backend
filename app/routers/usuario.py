from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate, UsuarioBase, RestaurarContraseniaRequest, UsuarioPreguntaResponse
from passlib.context import CryptContext
from app.models.pregunta_seguridad import Pregunta
from app.models.colaborador import Colaborador
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from datetime import timedelta, datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")
router = APIRouter(prefix="/usuarios", tags=["usuarios"])
SECRET_KEY = "mi_clave_secreta"
ALGORITHM = "HS256"
ACCES_TOKEN_EXPIRE_MINUTES = 60

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def crear_token(data: dict,expires_delta:timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCES_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM )

@router.post("/restaurar", response_model=UsuarioResponse)
def restaurar_contrasenia(
    datos: RestaurarContraseniaRequest,
    db: Session = Depends(get_db)
):
    db_usuario = db.query(Usuario).filter(Usuario.id_usuario == datos.id_usuario, Usuario.estado == True).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if not verify_password(datos.respuesta_pregunta, db_usuario.respuesta_pregunta):
        raise HTTPException(status_code=400, detail="Respuesta a la pregunta de seguridad incorrecta")

    db_usuario.contrasenia = hash_password(datos.nueva_contrasenia)
    db.commit()
    db.refresh(db_usuario)

    return db_usuario

@router.get("/user/{username}", response_model=UsuarioPreguntaResponse)
def obtener_usuario_por_username(username: str, db: Session = Depends(get_db)):
    print(username)
    usuario = db.query(Usuario).filter(Usuario.usuario == username, Usuario.estado == True).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.post("/", response_model=UsuarioResponse)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    pregunta = db.query(Pregunta).filter(Pregunta.id_pregunta == usuario.id_pregunta).first()
    colaborador = db.query(Colaborador).filter(Colaborador.id_colaborador == usuario.id_colaborador).first()
    if not pregunta:
        raise HTTPException(status_code=400, detail="Pregunta de seguridad no válida")
    elif not colaborador:
        raise HTTPException(status_code=400, detail="Colaborador no valido")
    usuario_data = usuario.dict()
    usuario_data["contrasenia"] = hash_password(usuario_data["contrasenia"])
    usuario_data["respuesta_pregunta"] = hash_password(usuario_data["respuesta_pregunta"])
    db_usuario = Usuario(**usuario_data)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.estado == True, Usuario.usuario == form_data.username).first()
    if not db_usuario or not verify_password(form_data.password,db_usuario.contrasenia):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    
    token_data = {"sub": db_usuario.id_colaborador,"id_usuario":db_usuario.id_usuario,"role": db_usuario.rol_usuario}
    token = crear_token(token_data)
    return {"acces_token": token, "token_type":"bearer"}

@router.get("/", response_model=list[UsuarioResponse])
def obtener_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).filter(Usuario.estado == True).all()

@router.get("/{id_usuario}", response_model=UsuarioResponse)
def obtener_usuario_por_id(id_usuario: int, db: Session = Depends(get_db)):
    print(id_usuario)
    db_usuario = db.query(Usuario).filter(Usuario.estado == True, Usuario.id_usuario == id_usuario ).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario
    
@router.put("/{id_usuario}", response_model=UsuarioResponse)
def actualizar_usuario(id_usuario: int, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    for key, value in usuario.dict(exclude_unset=True).items():
        setattr(db_usuario, key, value)
    
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@router.delete("/{id_usuario}", response_model=UsuarioResponse)
def eliminar_usuario_logico(id_usuario: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    usuario.estado = False
    db.commit()
    db.refresh(usuario)
    return JSONResponse(content={"mensaje":"Usuario eliminado correctamente"}, status_code=200)