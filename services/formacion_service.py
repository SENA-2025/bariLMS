"""
services/formacion_service.py
CRUD para Modalidades, Niveles, Programas de Formación
"""
import datetime
from app import db
from models.models import Modalidad, Nivel, ProgramaFormacion


# ---------------------------------------------------------------------------
# Modalidades
# ---------------------------------------------------------------------------

def listar_modalidades():
    return Modalidad.query.order_by(Modalidad.nombre).all()


def obtener_modalidad(modalidad_id: str):
    return Modalidad.query.get_or_404(modalidad_id)


def crear_modalidad(nombre: str) -> Modalidad:
    m = Modalidad(nombre=nombre.strip())
    db.session.add(m)
    db.session.commit()
    return m


def editar_modalidad(modalidad_id: str, nombre: str) -> Modalidad:
    m = obtener_modalidad(modalidad_id)
    m.nombre = nombre.strip()
    m.fecha_actualizacion = datetime.datetime.utcnow()
    db.session.commit()
    return m


def eliminar_modalidad(modalidad_id: str):
    m = obtener_modalidad(modalidad_id)
    db.session.delete(m)
    db.session.commit()


# ---------------------------------------------------------------------------
# Niveles
# ---------------------------------------------------------------------------

def listar_niveles():
    return Nivel.query.order_by(Nivel.nombre).all()


def obtener_nivel(nivel_id: str):
    return Nivel.query.get_or_404(nivel_id)


def crear_nivel(nombre: str) -> Nivel:
    n = Nivel(nombre=nombre.strip())
    db.session.add(n)
    db.session.commit()
    return n


def editar_nivel(nivel_id: str, nombre: str) -> Nivel:
    n = obtener_nivel(nivel_id)
    n.nombre = nombre.strip()
    n.fecha_actualizacion = datetime.datetime.utcnow()
    db.session.commit()
    return n


def eliminar_nivel(nivel_id: str):
    n = obtener_nivel(nivel_id)
    db.session.delete(n)
    db.session.commit()


# ---------------------------------------------------------------------------
# Programas de Formación
# ---------------------------------------------------------------------------

def listar_programas():
    return ProgramaFormacion.query.order_by(ProgramaFormacion.nombre).all()


def obtener_programa(programa_id: str):
    return ProgramaFormacion.query.get_or_404(programa_id)


def crear_programa(nombre: str, codigo: str, nivel_id: str, modalidad_id: str, centro_id: str) -> ProgramaFormacion:
    p = ProgramaFormacion(
        nombre=nombre.strip(),
        codigo=codigo.strip(),
        nivel_id=nivel_id,
        modalidad_id=modalidad_id,
        centro_id=centro_id,
    )
    db.session.add(p)
    db.session.commit()
    return p


def editar_programa(programa_id: str, nombre: str, codigo: str, nivel_id: str, modalidad_id: str, centro_id: str) -> ProgramaFormacion:
    p = obtener_programa(programa_id)
    p.nombre = nombre.strip()
    p.codigo = codigo.strip()
    p.nivel_id = nivel_id
    p.modalidad_id = modalidad_id
    p.centro_id = centro_id
    p.fecha_actualizacion = datetime.datetime.utcnow()
    db.session.commit()
    return p


def eliminar_programa(programa_id: str):
    p = obtener_programa(programa_id)
    db.session.delete(p)
    db.session.commit()
