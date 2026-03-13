"""
routes/formacion_routes.py
Rutas CRUD para Modalidades, Niveles y Programas de Formación
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from services.auth_service import login_required
from services import formacion_service, sena_service
from logger import logger

formacion_routes = Blueprint("formacion", __name__, url_prefix="/formacion")


# ---------------------------------------------------------------------------
# Modalidades
# ---------------------------------------------------------------------------

@formacion_routes.get("/modalidades")
@login_required
def modalidades():
    return render_template("formacion/modalidades.html", modalidades=formacion_service.listar_modalidades())


@formacion_routes.post("/modalidades/crear")
@login_required
def crear_modalidad():
    try:
        formacion_service.crear_modalidad(request.form["nombre"])
        flash("Modalidad creada.", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    return redirect(url_for("formacion.modalidades"))


@formacion_routes.post("/modalidades/<modalidad_id>/editar")
@login_required
def editar_modalidad(modalidad_id):
    try:
        formacion_service.editar_modalidad(modalidad_id, request.form["nombre"])
        flash("Modalidad actualizada.", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    return redirect(url_for("formacion.modalidades"))


@formacion_routes.post("/modalidades/<modalidad_id>/eliminar")
@login_required
def eliminar_modalidad(modalidad_id):
    try:
        formacion_service.eliminar_modalidad(modalidad_id)
        flash("Modalidad eliminada.", "success")
    except Exception as e:
        flash(f"No se puede eliminar: {e}", "danger")
    return redirect(url_for("formacion.modalidades"))


# ---------------------------------------------------------------------------
# Niveles
# ---------------------------------------------------------------------------

@formacion_routes.get("/niveles")
@login_required
def niveles():
    return render_template("formacion/niveles.html", niveles=formacion_service.listar_niveles())


@formacion_routes.post("/niveles/crear")
@login_required
def crear_nivel():
    try:
        formacion_service.crear_nivel(request.form["nombre"])
        flash("Nivel creado.", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    return redirect(url_for("formacion.niveles"))


@formacion_routes.post("/niveles/<nivel_id>/editar")
@login_required
def editar_nivel(nivel_id):
    try:
        formacion_service.editar_nivel(nivel_id, request.form["nombre"])
        flash("Nivel actualizado.", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    return redirect(url_for("formacion.niveles"))


@formacion_routes.post("/niveles/<nivel_id>/eliminar")
@login_required
def eliminar_nivel(nivel_id):
    try:
        formacion_service.eliminar_nivel(nivel_id)
        flash("Nivel eliminado.", "success")
    except Exception as e:
        flash(f"No se puede eliminar: {e}", "danger")
    return redirect(url_for("formacion.niveles"))


# ---------------------------------------------------------------------------
# Programas de Formación
# ---------------------------------------------------------------------------

@formacion_routes.get("/programas")
@login_required
def programas():
    return render_template(
        "formacion/programas.html",
        programas=formacion_service.listar_programas(),
        niveles=formacion_service.listar_niveles(),
        modalidades=formacion_service.listar_modalidades(),
        centros=sena_service.listar_centros(),
    )


@formacion_routes.post("/programas/crear")
@login_required
def crear_programa():
    try:
        formacion_service.crear_programa(
            request.form["nombre"],
            request.form["codigo"],
            request.form["nivel_id"],
            request.form["modalidad_id"],
            request.form["centro_id"],
        )
        flash("Programa creado.", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    return redirect(url_for("formacion.programas"))


@formacion_routes.post("/programas/<programa_id>/editar")
@login_required
def editar_programa(programa_id):
    try:
        formacion_service.editar_programa(
            programa_id,
            request.form["nombre"],
            request.form["codigo"],
            request.form["nivel_id"],
            request.form["modalidad_id"],
            request.form["centro_id"],
        )
        flash("Programa actualizado.", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    return redirect(url_for("formacion.programas"))


@formacion_routes.post("/programas/<programa_id>/eliminar")
@login_required
def eliminar_programa(programa_id):
    try:
        formacion_service.eliminar_programa(programa_id)
        flash("Programa eliminado.", "success")
    except Exception as e:
        flash(f"No se puede eliminar: {e}", "danger")
    return redirect(url_for("formacion.programas"))
