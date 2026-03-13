"""
services/sena_service.py
CRUD para estructura SENA: Regionales, Centros, Sedes, Ambientes, Coordinaciones
"""
import datetime
from app import db
from models.models import Regional, Centro, Sede, Ambiente, Coordinacion


# ---------------------------------------------------------------------------
# Regionales
# ---------------------------------------------------------------------------

def listar_regionales():
    return Regional.query.order_by(Regional.nombre).all()


def obtener_regional(regional_id: str):
    return Regional.query.get_or_404(regional_id)


def crear_regional(nombre: str, abreviatura: str) -> Regional:
    r = Regional(nombre=nombre.strip().upper(), abreviatura=abreviatura.strip().upper())
    db.session.add(r)
    db.session.commit()
    return r


def editar_regional(regional_id: str, nombre: str, abreviatura: str) -> Regional:
    r = obtener_regional(regional_id)
    r.nombre = nombre.strip().upper()
    r.abreviatura = abreviatura.strip().upper()
    r.fecha_actualizacion = datetime.datetime.utcnow()
    db.session.commit()
    return r


def eliminar_regional(regional_id: str):
    r = obtener_regional(regional_id)
    db.session.delete(r)
    db.session.commit()


# ---------------------------------------------------------------------------
# Centros
# ---------------------------------------------------------------------------

def listar_centros():
    return Centro.query.order_by(Centro.nombre).all()


def obtener_centro(centro_id: str):
    return Centro.query.get_or_404(centro_id)


def crear_centro(nombre: str, regional_id: str) -> Centro:
    c = Centro(nombre=nombre.strip(), regional_id=regional_id)
    db.session.add(c)
    db.session.commit()
    return c


def editar_centro(centro_id: str, nombre: str, regional_id: str) -> Centro:
    c = obtener_centro(centro_id)
    c.nombre = nombre.strip()
    c.regional_id = regional_id
    c.fecha_actualizacion = datetime.datetime.utcnow()
    db.session.commit()
    return c


def eliminar_centro(centro_id: str):
    c = obtener_centro(centro_id)
    db.session.delete(c)
    db.session.commit()


# ---------------------------------------------------------------------------
# Sedes
# ---------------------------------------------------------------------------

def listar_sedes():
    return Sede.query.order_by(Sede.nombre).all()


def obtener_sede(sede_id: str):
    return Sede.query.get_or_404(sede_id)


def crear_sede(nombre: str, centro_id: str, direccion: str, barrio: str | None, codigo_postal: str | None) -> Sede:
    s = Sede(
        nombre=nombre.strip(),
        centro_id=centro_id,
        direccion=direccion.strip(),
        barrio=barrio.strip() if barrio else None,
        codigo_postal=codigo_postal.strip() if codigo_postal else None,
    )
    db.session.add(s)
    db.session.commit()
    return s


def editar_sede(sede_id: str, nombre: str, centro_id: str, direccion: str, barrio: str | None, codigo_postal: str | None) -> Sede:
    s = obtener_sede(sede_id)
    s.nombre = nombre.strip()
    s.centro_id = centro_id
    s.direccion = direccion.strip()
    s.barrio = barrio.strip() if barrio else None
    s.codigo_postal = codigo_postal.strip() if codigo_postal else None
    s.fecha_actualizacion = datetime.datetime.utcnow()
    db.session.commit()
    return s


def eliminar_sede(sede_id: str):
    s = obtener_sede(sede_id)
    db.session.delete(s)
    db.session.commit()


# ---------------------------------------------------------------------------
# Ambientes
# ---------------------------------------------------------------------------

def listar_ambientes():
    return Ambiente.query.order_by(Ambiente.nombre).all()


def obtener_ambiente(ambiente_id: str):
    return Ambiente.query.get_or_404(ambiente_id)


def crear_ambiente(nombre: str, sede_id: str) -> Ambiente:
    a = Ambiente(nombre=nombre.strip(), sede_id=sede_id)
    db.session.add(a)
    db.session.commit()
    return a


def editar_ambiente(ambiente_id: str, nombre: str, sede_id: str) -> Ambiente:
    a = obtener_ambiente(ambiente_id)
    a.nombre = nombre.strip()
    a.sede_id = sede_id
    a.fecha_actualizacion = datetime.datetime.utcnow()
    db.session.commit()
    return a


def eliminar_ambiente(ambiente_id: str):
    a = obtener_ambiente(ambiente_id)
    db.session.delete(a)
    db.session.commit()


# ---------------------------------------------------------------------------
# Coordinaciones
# ---------------------------------------------------------------------------

def listar_coordinaciones():
    return Coordinacion.query.order_by(Coordinacion.nombre).all()


def obtener_coordinacion(coordinacion_id: str):
    return Coordinacion.query.get_or_404(coordinacion_id)


def crear_coordinacion(nombre: str, centro_id: str) -> Coordinacion:
    c = Coordinacion(nombre=nombre.strip(), centro_id=centro_id)
    db.session.add(c)
    db.session.commit()
    return c


def editar_coordinacion(coordinacion_id: str, nombre: str, centro_id: str) -> Coordinacion:
    c = obtener_coordinacion(coordinacion_id)
    c.nombre = nombre.strip()
    c.centro_id = centro_id
    c.fecha_actualizacion = datetime.datetime.utcnow()
    db.session.commit()
    return c


def eliminar_coordinacion(coordinacion_id: str):
    c = obtener_coordinacion(coordinacion_id)
    db.session.delete(c)
    db.session.commit()
