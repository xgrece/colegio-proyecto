from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .database import engine, SessionLocal
from . import models, crud, schemas
from datetime import date
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse

# Iniciar el server: uvicorn main:app --reload
# uvicorn app.main:app --reload

# detener el server: CTRL+C

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuración de Jinja2Templates para usar la carpeta 'templates'
templates = Jinja2Templates(directory="app/templates")

# Montar la carpeta static para servir archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

#metodos create

@app.get("/create_alumno", response_class=HTMLResponse)
async def create_alumno_form(request: Request, db: Session = Depends(get_db)):
    cursos = crud.get_cursos(db)  # Supongamos que tienes una función que recupera todos los cursos
    return templates.TemplateResponse("create_alumno.html", {"request": request, "cursos": cursos})

@app.post("/create_alumno", response_class=HTMLResponse)
async def create_alumno(request: Request, nombre: str = Form(...), apellido: str = Form(...), fecha_nac: str = Form(...), curso_id: int = Form(...), db: Session = Depends(get_db)):
    try:
        fecha_nac_date = date.fromisoformat(fecha_nac)  # Convertir str a date
        new_alumno = crud.create_alumno(db, schemas.AlumnoCreate(nombre=nombre, apellido=apellido, fecha_nac=fecha_nac_date, curso_id=curso_id))
        return templates.TemplateResponse("create_alumno.html", {"request": request, "message": "Alumno creado con éxito"})
    except Exception as e:
        return templates.TemplateResponse("create_alumno.html", {"request": request, "message": f"Error al crear el alumno: {str(e)}"})

@app.get("/create_curso", response_class=HTMLResponse)
async def get_create_curso(request: Request):
    return templates.TemplateResponse("create_curso.html", {"request": request})

@app.post("/create_curso", response_class=HTMLResponse)
async def create_curso(request: Request, nombre: str = Form(...), db: Session = Depends(get_db)):
    print(request.method)
    new_curso = crud.create_curso(db, schemas.CursoCreate(nombre=nombre))
    return templates.TemplateResponse("create_curso.html", {"request": request, "message": "Curso creado con éxito"})

#metodos update
@app.get("/update_alumno", response_class=HTMLResponse)
async def update_alumno_form(request: Request):
    return templates.TemplateResponse("update_alumno.html", {"request": request})

@app.post("/update_alumno", response_class=HTMLResponse)
async def update_alumno(request: Request, id: int = Form(...), nombre: str = Form(None), apellido: str = Form(None), fecha_nac: str = Form(None), curso_id: int = Form(None), db: Session = Depends(get_db)):
    alumno = crud.get_alumno(db, id)
    if alumno:
        if fecha_nac:
            fecha_nac = date.fromisoformat(fecha_nac)
        updated_alumno = schemas.AlumnoUpdate(nombre=nombre, apellido=apellido, fecha_nac=fecha_nac, curso_id=curso_id)
        alumno = crud.update_alumno(db, id, updated_alumno)
        alumnos = crud.get_alumnos(db)
        return templates.TemplateResponse("read_alumnos.html", {"request": request, "alumnos": alumnos, "message": "Alumno actualizado con éxito"})
    else:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")

@app.get("/get_alumno_json/{id}", response_class=JSONResponse)
async def get_alumno_json(id: int, db: Session = Depends(get_db)):
    alumno = crud.get_alumno(db, id)
    if alumno:
        return alumno  # JSONResponse devolverá los datos en formato JSON
    else:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
#metodo read
@app.get("/read_alumnos", response_class=HTMLResponse)
async def read_alumnos(request: Request, db: Session = Depends(get_db)):
    alumnos = crud.get_alumnos(db)
    return templates.TemplateResponse("read_alumnos.html", {"request": request, "alumnos": alumnos})

#metodos delete
@app.get("/delete_alumno", response_class=HTMLResponse)
async def delete_alumno_form(request: Request):
    return templates.TemplateResponse("delete_alumno.html", {"request": request})

@app.post("/delete_alumno", response_class=HTMLResponse)
async def delete_alumno(request: Request, id: int = Form(...), db: Session = Depends(get_db)):
    alumno = crud.get_alumno(db, id)
    if alumno:
        crud.delete_alumno(db, id)
        alumnos = crud.get_alumnos(db)
        return templates.TemplateResponse("read_alumnos.html", {"request": request, "alumnos": alumnos, "message": "Alumno eliminado con éxito"})
    else:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    
#metodo icon    
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("app/static/assets/favicon.ico")