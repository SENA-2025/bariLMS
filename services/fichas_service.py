"""
services/fichas_service.py
CRUD para Fichas, Proyecto Formativo, Fases, Actividades, asignación de instructores
"""
import datetime
from app import db
from models.models import (
    Ficha, FichaInstructor, Instructor,
    ProyectoFormativo, Fase, ActividadProyecto, ActividadAprendizaje,
    Ambiente, Coordinacion, ProgramaFormacion,
)


# ---------------------------------------------------------------------------
# Fichas
# ---------------------------------------------------------------------------

def listar_fichas():
    return Ficha.query.order_by(Ficha.codigo).all()


def obtener_ficha(ficha_id: str):
    return Ficha.query.get_or_404(ficha_id)


def crear_ficha(
    codigo: int,
    programa_id: str,
    coordinacion_id: str,
    ambiente_id: str,
    instructor_lider_id: str,
    fecha_inicio: datetime.datetime,
    fecha_etapa_productiva: datetime.datetime,
    fecha_fin: datetime.datetime,
) -> Ficha:
    f = Ficha(
        codigo=codigo,
        programa_id=programa_id,
        coordinacion_id=coordinacion_id,
        ambiente_id=ambiente_id,
        instructor_lider_id=instructor_lider_id,
        fecha_inicio=fecha_inicio,
        fecha_etapa_productiva=fecha_etapa_productiva,
        fecha_fin=fecha_fin,
    )
    db.session.add(f)
    db.session.commit()
    return f


def editar_ficha(ficha_id: str, **kwargs) -> Ficha:
    f = obtener_ficha(ficha_id)
    for key, value in kwargs.items():
        setattr(f, key, value)
    f.fecha_actualizacion = datetime.datetime.utcnow()
    db.session.commit()
    return f


def eliminar_ficha(ficha_id: str):
    f = obtener_ficha(ficha_id)
    db.session.delete(f)
    db.session.commit()


# ---------------------------------------------------------------------------
# Asignación de instructores a ficha
# ---------------------------------------------------------------------------

def asignar_instructor(ficha_id: str, instructor_id: str) -> FichaInstructor:
    fi = FichaInstructor(ficha_id=ficha_id, instructor_id=instructor_id)
    db.session.add(fi)
    db.session.commit()
    return fi


def desasignar_instructor(fi_id: str):
    fi = FichaInstructor.query.get_or_404(fi_id)
    db.session.delete(fi)
    db.session.commit()


def instructores_disponibles_para_ficha(ficha: Ficha) -> list[Instructor]:
    asignados_ids = {fi.instructor_id for fi in ficha.instructores_asignados}
    asignados_ids.add(ficha.instructor_lider_id)
    return Instructor.query.filter(~Instructor.instructor_id.in_(asignados_ids)).all()


# ---------------------------------------------------------------------------
# Proyecto Formativo
# ---------------------------------------------------------------------------

def crear_proyecto(ficha_id: str, titulo: str, descripcion: str | None) -> ProyectoFormativo:
    p = ProyectoFormativo(ficha_id=ficha_id, titulo=titulo.strip(), descripcion=descripcion)
    db.session.add(p)
    db.session.commit()
    return p


def obtener_proyecto(proyecto_id: str):
    return ProyectoFormativo.query.get_or_404(proyecto_id)


# ---------------------------------------------------------------------------
# Fases
# ---------------------------------------------------------------------------

def crear_fase(proyecto_id: str, nombre: str, orden: int, descripcion: str | None) -> Fase:
    f = Fase(proyecto_id=proyecto_id, nombre=nombre.strip(), orden=orden, descripcion=descripcion)
    db.session.add(f)
    db.session.commit()
    return f


def eliminar_fase(fase_id: str):
    f = Fase.query.get_or_404(fase_id)
    db.session.delete(f)
    db.session.commit()


# ---------------------------------------------------------------------------
# Actividades de Proyecto
# ---------------------------------------------------------------------------

def crear_actividad_proyecto(fase_id: str, nombre: str, orden: int, descripcion: str | None) -> ActividadProyecto:
    a = ActividadProyecto(fase_id=fase_id, nombre=nombre.strip(), orden=orden, descripcion=descripcion)
    db.session.add(a)
    db.session.commit()
    return a


def eliminar_actividad_proyecto(act_id: str):
    a = ActividadProyecto.query.get_or_404(act_id)
    db.session.delete(a)
    db.session.commit()


# ---------------------------------------------------------------------------
# Actividades de Aprendizaje
# ---------------------------------------------------------------------------

def crear_actividad_aprendizaje(actividad_proyecto_id: str, nombre: str, orden: int, descripcion: str | None) -> ActividadAprendizaje:
    a = ActividadAprendizaje(
        actividad_proyecto_id=actividad_proyecto_id,
        nombre=nombre.strip(),
        orden=orden,
        descripcion=descripcion,
    )
    db.session.add(a)
    db.session.commit()
    return a


def eliminar_actividad_aprendizaje(act_id: str):
    a = ActividadAprendizaje.query.get_or_404(act_id)
    db.session.delete(a)
    db.session.commit()
