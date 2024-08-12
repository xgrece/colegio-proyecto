from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, Session
from .database import Base

class Curso(Base):
    __tablename__ = 'cursos'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(250), index=True)
    alumnos = relationship("Alumno", back_populates="curso")
   
    @classmethod
    def create(cls, session: Session, **kwargs):
        new_curso = cls(**kwargs)
        session.add(new_curso)
        session.commit()
        session.refresh(new_curso)
        return new_curso

    @classmethod
    def read(cls, session: Session, curso_id: int):
        return session.query(cls).filter(cls.id == curso_id).first()

    @classmethod
    def read_all(cls, session: Session, skip: int = 0, limit: int = 10):
        return session.query(cls).offset(skip).limit(limit).all()

    def update(self, session: Session, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        session.commit()
        session.refresh(self)
        return self

    def delete(self, session: Session):
        session.delete(self)
        session.commit() 

class Alumno(Base):
    __tablename__ = 'alumnos'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(250), index=True)
    apellido = Column(String(250), index=True)
    fecha_nac = Column(Date)
    curso_id = Column(Integer, ForeignKey('cursos.id'))
    curso = relationship("Curso", back_populates="alumnos")
    
    @classmethod
    def create(cls, session: Session, **kwargs):
        new_alumno = cls(**kwargs)
        session.add(new_alumno)
        session.commit()
        session.refresh(new_alumno)
        return new_alumno

    @classmethod
    def read(cls, session: Session, alumno_id: int):
        return session.query(cls).filter(cls.id == alumno_id).first()

    @classmethod
    def read_all(cls, session: Session, skip: int = 0, limit: int = 10):
        return session.query(cls).offset(skip).limit(limit).all()

    def update(self, session: Session, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        session.commit()
        session.refresh(self)
        return self

    def delete(self, session: Session):
        session.delete(self)
        session.commit()