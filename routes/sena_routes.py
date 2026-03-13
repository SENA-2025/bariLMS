"""
routes/sena_routes.py
Rutas CRUD para: Regionales, Centros, Sedes, Ambientes, Coordinaciones
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from services.auth_service import login_required
from services import sena_service
from logger import logger

sena_routes = Blueprint("sena", __name__, url_prefix="/sena")


# ---------------------------------------------------------------------------
# Regionales
# ---------------------------------------------------------------------------

@sena_routes.get("/regionales")
@login_required
def regionales():
    return render_template("sena/regionales.html", regionales=sena_service.listar_regionales())


@sena_routes.post("/regionales/crear")
@login_required
def crear_regional():
    try:
        sena_service.crear_regional(request.form["nombre"], request.form["abreviatura"])
        flash("Regional creada correctamente.", "success")
    except Exception as e:
        flash(f"Error al crear: {e}", "danger")
        logger.error("Error crear regional: %s", e)
    return redirect(url_for("sena.regionales"))


@sena_routes.post("/regionales/<regional_id>/editar")
@login_required
def editar_regional(regional_id):
    try:
        sena_service.editar_regional(regional_id, request.form["nombre"], request.form["abreviatura"])
        flash("Regional actualizada.", "success")
    except Exception as e:
        flash(f"Error al actualizar: {e}", "danger")
    return redirect(url_for("sena.regionales"))


@sena_routes.post("/regionales/<regional_id>/eliminar")
@login_required
def eliminar_regional(regional_id):
    try:
        sena_service.eliminar_regional(regional_id)
        flash("Regional eliminada.", "success")
    except Exception as e:
        flash(f"No se puede eliminar: {e}", "danger")
    return redirect(url_for("sena.regionales"))


# ---------------------------------------------------------------------------
# Centros
# ---------------------------------------------------------------------------

@sena_routes.get("/centros")
@login_required
def centros():
    return render_template(
        "sena/centros.html",
        centros=sena_service.listar_centros(),
        regionales=sena_service.listar_regionales(),
    )


@sena_routes.post("/centros/crear")
@login_required
def crear_centro():
    try:
        sena_service.crear_centro(request.form["nombre"], request.form["regional_id"])
        flash("Centro creado correctamente.", "success")
    except Exception as e:
        flash(f"Error al crear: {e}", "danger")
    return redirect(url_for("sena.centros"))


@sena_routes.post("/centros/<centro_id>/editar")
@login_required
def editar_centro(centro_id):
    try:
        sena_service.editar_centro(centro_id, request.form["nombre"], request.form["regional_id"])
        flash("Centro actualizado.", "success")
    except Exception as e:
        flash(f"Error al actualizar: {e}", "danger")
    return redirect(url_for("sena.centros"))


@sena_routes.post("/centros/<centro_id>/eliminar")
@login_required
def eliminar_centro(centro_id):
    try:
        sena_service.eliminar_centro(centro_id)
        flash("Centro eliminado.", "success")
    except Exception as e:
        flash(f"No se puede eliminar: {e}", "danger")
    return redirect(url_for("sena.centros"))


# ---------------------------------------------------------------------------
# Sedes
# ---------------------------------------------------------------------------

@sena_routes.get("/sedes")
@login_required
def sedes():
    return render_template(
        "sena/sedes.html",
        sedes=sena_service.listar_sedes(),
        centros=sena_service.listar_centros(),
    )


@sena_routes.post("/sedes/crear")
@login_required
def crear_sede():
    try:
        sena_service.crear_sede(
            request.form["nombre"],
            request.form["centro_id"],
            request.form["direccion"],
            request.form.get("barrio"),
            request.form.get("codigo_postal"),
        )
        flash("Sede creada correctamente.", "success")
    except Exception as e:
        flash(f"Error al crear: {e}", "danger")
    return redirect(url_for("sena.sedes"))


@sena_routes.post("/sedes/<sede_id>/editar")
@login_required
def editar_sede(sede_id):
    try:
        sena_service.editar_sede(
            sede_id,
            request.form["nombre"],
            request.form["centro_id"],
            request.form["direccion"],
            request.form.get("barrio"),
            request.form.get("codigo_postal"),
        )
        flash("Sede actualizada.", "success")
    except Exception as e:
        flash(f"Error al actualizar: {e}", "danger")
    return redirect(url_for("sena.sedes"))


@sena_routes.post("/sedes/<sede_id>/eliminar")
@login_required
def eliminar_sede(sede_id):
    try:
        sena_service.eliminar_sede(sede_id)
        flash("Sede eliminada.", "success")
    except Exception as e:
        flash(f"No se puede eliminar: {e}", "danger")
    return redirect(url_for("sena.sedes"))


# ---------------------------------------------------------------------------
# Ambientes
# ---------------------------------------------------------------------------

@sena_routes.get("/ambientes")
@login_required
def ambientes():
    return render_template(
        "sena/ambientes.html",
        ambientes=sena_service.listar_ambientes(),
        sedes=sena_service.listar_sedes(),
    )


@sena_routes.post("/ambientes/crear")
@login_required
def crear_ambiente():
    try:
        sena_service.crear_ambiente(request.form["nombre"], request.form["sede_id"])
        flash("Ambiente creado correctamente.", "success")
    except Exception as e:
        flash(f"Error al crear: {e}", "danger")
    return redirect(url_for("sena.ambientes"))


@sena_routes.post("/ambientes/<ambiente_id>/editar")
@login_required
def editar_ambiente(ambiente_id):
    try:
        sena_service.editar_ambiente(ambiente_id, request.form["nombre"], request.form["sede_id"])
        flash("Ambiente actualizado.", "success")
    except Exception as e:
        flash(f"Error al actualizar: {e}", "danger")
    return redirect(url_for("sena.ambientes"))


@sena_routes.post("/ambientes/<ambiente_id>/eliminar")
@login_required
def eliminar_ambiente(ambiente_id):
    try:
        sena_service.eliminar_ambiente(ambiente_id)
        flash("Ambiente eliminado.", "success")
    except Exception as e:
        flash(f"No se puede eliminar: {e}", "danger")
    return redirect(url_for("sena.ambientes"))


# ---------------------------------------------------------------------------
# Coordinaciones
# ---------------------------------------------------------------------------

@sena_routes.get("/coordinaciones")
@login_required
def coordinaciones():
    return render_template(
        "sena/coordinaciones.html",
        coordinaciones=sena_service.listar_coordinaciones(),
        centros=sena_service.listar_centros(),
    )


@sena_routes.post("/coordinaciones/crear")
@login_required
def crear_coordinacion():
    try:
        sena_service.crear_coordinacion(request.form["nombre"], request.form["centro_id"])
        flash("Coordinación creada correctamente.", "success")
    except Exception as e:
        flash(f"Error al crear: {e}", "danger")
    return redirect(url_for("sena.coordinaciones"))


@sena_routes.post("/coordinaciones/<coordinacion_id>/editar")
@login_required
def editar_coordinacion(coordinacion_id):
    try:
        sena_service.editar_coordinacion(coordinacion_id, request.form["nombre"], request.form["centro_id"])
        flash("Coordinación actualizada.", "success")
    except Exception as e:
        flash(f"Error al actualizar: {e}", "danger")
    return redirect(url_for("sena.coordinaciones"))


@sena_routes.post("/coordinaciones/<coordinacion_id>/eliminar")
@login_required
def eliminar_coordinacion(coordinacion_id):
    try:
        sena_service.eliminar_coordinacion(coordinacion_id)
        flash("Coordinación eliminada.", "success")
    except Exception as e:
        flash(f"No se puede eliminar: {e}", "danger")
    return redirect(url_for("sena.coordinaciones"))
