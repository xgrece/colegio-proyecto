from sqlalchemy.orm import Session
from . import models, schemas

def create_alumno(db: Session, alumno: schemas.AlumnoCreate):
    db_alumno = models.Alumno(**alumno.dict())
    db.add(db_alumno)
    db.commit()
    db.refresh(db_alumno)
    return db_alumno

def get_alumno(db: Session, alumno_id: int):
    return db.query(models.Alumno).filter(models.Alumno.id == alumno_id).first()

def get_alumnos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Alumno).offset(skip).limit(limit).all()

def update_alumno(db: Session, alumno_id: int, alumno: schemas.AlumnoUpdate):
    db_alumno = get_alumno(db, alumno_id)
    if db_alumno:
        for key, value in alumno.dict(exclude_unset=True).items():
            setattr(db_alumno, key, value)
        db.commit()
        db.refresh(db_alumno)
        return db_alumno
    return None

def delete_alumno(db: Session, alumno_id: int):
    db_alumno = get_alumno(db, alumno_id)
    if db_alumno:
        db.delete(db_alumno)
        db.commit()
    return db_alumno

def create_curso(db: Session, curso: schemas.CursoCreate):
    new_curso = models.Curso(**curso.dict())
    db.add(new_curso)
    db.commit()
    db.refresh(new_curso)
    return new_curso

def get_cursos(db: Session):
    return db.query(models.Curso).all()

def get_curso(db: Session, curso_id: int):
    return db.query(models.Curso).filter(models.Curso.id == curso_id).first()

def update_curso(db: Session, curso_id: int, curso: schemas.CursoUpdate):
    db_curso = get_curso(db, curso_id)
    if db_curso:
        for key, value in curso.dict(exclude_unset=True).items():
            setattr(db_curso, key, value)
        db.commit()
        db.refresh(db_curso)
        return db_curso
    return None

def delete_curso(db: Session, curso_id: int):
    db_curso = get_curso(db, curso_id)
    if db_curso:
        db.delete(db_curso)
        db.commit()
    return db_curso