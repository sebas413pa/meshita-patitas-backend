from fastapi import FastAPI
from app.database import engine
from app.models import usuario
from app.models import pregunta_seguridad
from app.models import colaborador
from app.routers import usuario as usuario_router
from app.routers import pregunta_seguridad as pregunta_router
from app.routers import colaborador as colaborador_router
from fastapi.staticfiles import StaticFiles
from app.routers import imagen as imagen_router
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from app.models import animal
from app.models import campania
from app.models import solicitud_adopcion
from app.routers import usuario as usuario_router
from app.routers import animal as animal_router
from app.routers import campania as campania_router
from app.routers import solicitud_adopcion as solicitud_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
# Crea las tablas en la BDC
usuario.Base.metadata.create_all(bind=engine)
pregunta_seguridad.Base.metadata.create_all(bind=engine)
colaborador.Base.metadata.create_all(bind=engine)
animal.Base.metadata.create_all(bind=engine)
campania.Base.metadata.create_all(bind=engine)
solicitud_adopcion.Base.metadata.create_all(bind=engine)
# Incluye los routers


app.include_router(usuario_router.router)
app.include_router(pregunta_router.router)
app.include_router(colaborador_router.router)
app.include_router(animal_router.router)
app.include_router(campania_router.router)
app.include_router(imagen_router.router)
app.include_router(solicitud_router.router)

