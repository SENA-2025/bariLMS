"""
services/instructores_service.py
CRUD para Instructores (usuario + vínculo instructor)
"""
import datetime
from werkzeug.security import generate_password_hash
from app import db
from models.models import Instructor, Usuario, Rol


def listar_instructores():
    return Instructor.query.join(Usuario).order_by(Usuario.primer_apellido).all()


def obtener_instructor(instructor_id: str):
    return Instructor.query.get_or_404(instructor_id)


def crear_instructor(
    tipo_documento: str,
    identificacion: str,
    correo: str,
    primer_nombre: str,
    segundo_nombre: str | None,
    primer_apellido: str,
    segundo_apellido: str | None,
    contrasena: str,
    coordinacion_id: str,
) -> Instructor:
    rol_instructor = Rol.query.filter_by(nombre="Instructor").first()
    if not rol_instructor:
        raise ValueError("Rol 'Instructor' no encontrado en la base de datos.")

    usuario = Usuario(
        tipo_documento=tipo_documento,
        identificacion=identificacion.strip(),
        correo=correo.strip().lower(),
        primer_nombre=primer_nombre.strip().upper(),
        segundo_nombre=segundo_nombre.strip().upper() if segundo_nombre else None,
        primer_apellido=primer_apellido.strip().upper(),
        segundo_apellido=segundo_apellido.strip().upper() if segundo_apellido else None,
        contrasena_hash=generate_password_hash(contrasena),
        rol_id=rol_instructor.rol_id,
        cuenta_activa=True,
    )
    db.session.add(usuario)
    db.session.flush()

    instructor = Instructor(usuario_id=usuario.usuario_id, coordinacion_id=coordinacion_id)
    db.session.add(instructor)
    db.session.commit()
    return instructor


def editar_instructor(instructor_id: str, coordinacion_id: str) -> Instructor:
    i = obtener_instructor(instructor_id)
    i.coordinacion_id = coordinacion_id
    i.fecha_actualizacion = datetime.datetime.utcnow()
    db.session.commit()
    return i


def eliminar_instructor(instructor_id: str):
    i = obtener_instructor(instructor_id)
    db.session.delete(i)
    db.session.commit()
