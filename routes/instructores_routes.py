"""
routes/instructores_routes.py
CRUD de Instructores
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from services.auth_service import login_required
from services import instructores_service, sena_service
from logger import logger

instructores_routes = Blueprint("instructores", __name__, url_prefix="/instructores")


@instructores_routes.get("/")
@login_required
def lista():
    return render_template(
        "instructores/instructores.html",
        instructores=instructores_service.listar_instructores(),
        coordinaciones=sena_service.listar_coordinaciones(),
    )


@instructores_routes.post("/crear")
@login_required
def crear():
    try:
        instructores_service.crear_instructor(
            tipo_documento=request.form["tipo_documento"],
            identificacion=request.form["identificacion"],
            correo=request.form["correo"],
            primer_nombre=request.form["primer_nombre"],
            segundo_nombre=request.form.get("segundo_nombre") or None,
            primer_apellido=request.form["primer_apellido"],
            segundo_apellido=request.form.get("segundo_apellido") or None,
            contrasena=request.form["contrasena"],
            coordinacion_id=request.form["coordinacion_id"],
        )
        flash("Instructor creado correctamente.", "success")
    except Exception as e:
        flash(f"Error al crear instructor: {e}", "danger")
        logger.error("Error crear instructor: %s", e)
    return redirect(url_for("instructores.lista"))


@instructores_routes.post("/<instructor_id>/editar")
@login_required
def editar(instructor_id):
    try:
        instructores_service.editar_instructor(instructor_id, request.form["coordinacion_id"])
        flash("Instructor actualizado.", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    return redirect(url_for("instructores.lista"))


@instructores_routes.post("/<instructor_id>/eliminar")
@login_required
def eliminar(instructor_id):
    try:
        instructores_service.eliminar_instructor(instructor_id)
        flash("Instructor eliminado.", "success")
    except Exception as e:
        flash(f"No se puede eliminar: {e}", "danger")
    return redirect(url_for("instructores.lista"))
