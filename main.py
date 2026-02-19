from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from auth import router as auth_router
from deps import get_current_user
from db import get_db
from models import Incidencia

app = FastAPI(
    title="API Incidencias - FastAPI + MySQL + JWT",
    version="1.0.0"
)

app.include_router(auth_router)

class IncidenciaCreate(BaseModel):
    titulo: str = Field(min_length=1, max_length=150)
    descripcion: str = Field(min_length=1)
    prioridad: str = Field(min_length=1, max_length=20)
    estado: str = Field(min_length=1, max_length=20)

class IncidenciaResponse(IncidenciaCreate):
    id: int
    class Config:
        from_attributes = True

# ENDPOINTS

@app.get("/")
def root():
    return {"ok": True, "mensaje": "API de incidencias funcionando. Ve a /docs"}

# Endpoint protegido que obtiene info del token
@app.get("/usuario")
def me(usuario: str = Depends(get_current_user)):
    return {"usuario": usuario}

@app.get("/incidencias", response_model=list[IncidenciaResponse])
def listar_incidencias(db: Session = Depends(get_db)):
    return db.query(Incidencia).all()

# POST /incidencias PROTEGIDO y se inserta en MySQL
@app.post("/incidencias", response_model=IncidenciaResponse, status_code=status.HTTP_201_CREATED)
def crear_incidencia(
    data: IncidenciaCreate,
    db: Session = Depends(get_db),
    usuario: str = Depends(get_current_user)  # protección JWT
):
    nueva = Incidencia(
        titulo=data.titulo,
        descripcion=data.descripcion,
        prioridad=data.prioridad,
        estado=data.estado
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva