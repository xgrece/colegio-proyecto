from pydantic import BaseModel
from datetime import date
from typing import Optional
# Schemas para los cursos

class CursoBase(BaseModel):
    nombre: str

class CursoCreate(CursoBase):
    pass

class CursoUpdate(CursoBase):  # Añadido CursoUpdate
    pass

class CursoUpdate(BaseModel):
    nombre: Optional[str] = None

    class Config:
        from_attributes = True

# Schemas para los alumnos

class AlumnoBase(BaseModel):
    nombre: str
    apellido: str
    fecha_nac: date
    curso_id: int

class AlumnoCreate(BaseModel):
    nombre: str
    apellido: str
    fecha_nac: date
    curso_id: int
    
    
class AlumnoUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    fecha_nac: Optional[date] = None
    curso_id: Optional[int] = None
    
class Alumno(AlumnoBase):
    id: int

    class Config:
        from_attributes = True