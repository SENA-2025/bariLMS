"""
routes/fichas_routes.py
CRUD de Fichas + Proyecto Formativo + Fases + Actividades
"""
import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for
from services.auth_service import login_required
from services import fichas_service, sena_service, formacion_service, instructores_service
from logger import logger

fichas_routes = Blueprint("fichas", __name__, url_prefix="/fichas")


def _parse_date(value: str) -> datetime.datetime:
    return datetime.datetime.strptime(value, "%Y-%m-%d")


# ---------------------------------------------------------------------------
# Lista y detalle
# ---------------------------------------------------------------------------

@fichas_routes.get("/")
@login_required
def lista():
    return render_template(
        "fichas/fichas.html",
        fichas=fichas_service.listar_fichas(),
        programas=formacion_service.listar_programas(),
        coordinaciones=sena_service.listar_coordinaciones(),
        ambientes=sena_service.listar_ambientes(),
        instructores=instructores_service.listar_instructores(),
    )


@fichas_routes.get("/<ficha_id>")
@login_required
def detalle(ficha_id):
    ficha = fichas_service.obtener_ficha(ficha_id)
    return render_template(
        "fichas/detalle.html",
        ficha=ficha,
        instructores=instructores_service.listar_instructores(),
        instructores_disponibles=fichas_service.instructores_disponibles_para_ficha(ficha),
    )


# ---------------------------------------------------------------------------
# CRUD ficha
# ---------------------------------------------------------------------------

@fichas_routes.post("/crear")
@login_required
def crear():
    try:
        fichas_service.crear_ficha(
            codigo=int(request.form["codigo"]),
            programa_id=request.form["programa_id"],
            coordinacion_id=request.form["coordinacion_id"],
            ambiente_id=request.form["ambiente_id"],
            instructor_lider_id=request.form["instructor_lider_id"],
            fecha_inicio=_parse_date(request.form["fecha_inicio"]),
            fecha_etapa_productiva=_parse_date(request.form["fecha_etapa_productiva"]),
            fecha_fin=_parse_date(request.form["fecha_fin"]),
        )
        flash("Ficha creada correctamente.", "success")
    except Exception as e:
        flash(f"Error al crear ficha: {e}", "danger")
        logger.error("Error crear ficha: %s", e)
    return redirect(url_for("fichas.lista"))


@fichas_routes.post("/<ficha_id>/editar")
@login_required
def editar(ficha_id):
    try:
        fichas_service.editar_ficha(
            ficha_id,
            codigo=int(request.form["codigo"]),
            programa_id=request.form["programa_id"],
            coordinacion_id=request.form["coordinacion_id"],
            ambiente_id=request.form["ambiente_id"],
            instructor_lider_id=request.form["instructor_lider_id"],
            fecha_inicio=_parse_date(request.form["fecha_inicio"]),
            fecha_etapa_productiva=_parse_date(request.form["fecha_etapa_productiva"]),
            fecha_fin=_parse_date(request.form["fecha_fin"]),
        )
        flash("Ficha actualizada.", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    return redirect(url_for("fichas.lista"))


@fichas_routes.post("/<ficha_id>/eliminar")
@login_required
def eliminar(ficha_id):
    try:
        fichas_service.eliminar_ficha(ficha_id)
        flash("Ficha eliminada.", "success")
    except Exception as e:
        flash(f"No se puede eliminar: {e}", "danger")
    return redirect(url_for("fichas.lista"))


# ---------------------------------------------------------------------------
# Instructores de ficha
# ---------------------------------------------------------------------------

@fichas_routes.post("/<ficha_id>/instructores/asignar")
@login_required
def asignar_instructor(ficha_id):
    try:
        fichas_service.asignar_instructor(ficha_id, request.form["instructor_id"])
        flash("Instructor asignado.", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    return redirect(url_for("fichas.detalle", ficha_id=ficha_id))


@fichas_routes.post("/<ficha_id>/instructores/<fi_id>/desasignar")
@login_required
def desasignar_instructor(ficha_id, fi_id):
    try:
        fichas_service.desasignar_instructor(fi_id)
        flash("Instructor desasignado.", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    return redirect(url_for("fichas.detalle", ficha_id=ficha_id))


# ---------------------------------------------------------------------------
# Proyecto Formativo
# ---------------------------------------------------------------------------

@fichas_routes.post("/<ficha_id>/proyecto/crear")
@login_required
def crear_proyecto(ficha_id):
    try:
        fichas_service.crear_proyecto(
            ficha_id,
            request.form["titulo"],
            request.form.get("descripcion") or None,
        )
        flash("Proyecto formativo creado.", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    return redirect(url_for("fichas.detalle", ficha_id=ficha_id))


# ---------------------------------------------------------------------------
# Fases
# ---------------------------------------------------------------------------

@fichas_routes.post("/proyecto/<proyecto_id>/fases/crear")
@login_required
def crear_fase(proyecto_id):
    proyecto = fichas_service.obtener_proyecto(proyecto_id)
    try:
        fichas_service.crear_fase(
            proyecto_id,
            request.form["nombre"],
            int(request.form.get("orden", 1)),
            request.form.get("descripcion") or None,
        )
        flash("Fase creada.", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    return redirect(url_for("fichas.detalle", ficha_id=proyecto.ficha_id))


@fichas_routes.post("/fases/<fase_id>/eliminar")
@login_required
def eliminar_fase(fase_id):
    from models.models import Fase
    fase = Fase.query.get_or_404(fase_id)
    ficha_id = fase.proyecto.ficha_id
    try:
        fichas_service.eliminar_fase(fase_id)
        flash("Fase eliminada.", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    return redirect(url_for("fichas.detalle", ficha_id=ficha_id))


# ---------------------------------------------------------------------------
# Actividades de Proyecto
# ---------------------------------------------------------------------------

@fichas_routes.post("/fases/<fase_id>/actividades/crear")
@login_required
def crear_actividad_proyecto(fase_id):
    from models.models import Fase
    fase = Fase.query.get_or_404(fase_id)
    ficha_id = fase.proyecto.ficha_id
    try:
        fichas_service.crear_actividad_proyecto(
            fase_id,
            request.form["nombre"],
            int(request.form.get("orden", 1)),
            request.form.get("descripcion") or None,
        )
        flash("Actividad de proyecto creada.", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    return redirect(url_for("fichas.detalle", ficha_id=ficha_id))


@fichas_routes.post("/actividades-proyecto/<act_id>/eliminar")
@login_required
def eliminar_act_proyecto(act_id):
    from models.models import ActividadProyecto
    act = ActividadProyecto.query.get_or_404(act_id)
    ficha_id = act.fase.proyecto.ficha_id
    try:
        fichas_service.eliminar_actividad_proyecto(act_id)
        flash("Actividad eliminada.", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    return redirect(url_for("fichas.detalle", ficha_id=ficha_id))


# ---------------------------------------------------------------------------
# Actividades de Aprendizaje
# ---------------------------------------------------------------------------

@fichas_routes.post("/actividades-proyecto/<act_proyecto_id>/actividades-aprendizaje/crear")
@login_required
def crear_actividad_aprendizaje(act_proyecto_id):
    from models.models import ActividadProyecto
    act_p = ActividadProyecto.query.get_or_404(act_proyecto_id)
    ficha_id = act_p.fase.proyecto.ficha_id
    try:
        fichas_service.crear_actividad_aprendizaje(
            act_proyecto_id,
            request.form["nombre"],
            int(request.form.get("orden", 1)),
            request.form.get("descripcion") or None,
        )
        flash("Actividad de aprendizaje creada.", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    return redirect(url_for("fichas.detalle", ficha_id=ficha_id))


@fichas_routes.post("/actividades-aprendizaje/<act_id>/eliminar")
@login_required
def eliminar_act_aprendizaje(act_id):
    from models.models import ActividadAprendizaje
    act = ActividadAprendizaje.query.get_or_404(act_id)
    ficha_id = act.actividad_proyecto.fase.proyecto.ficha_id
    try:
        fichas_service.eliminar_actividad_aprendizaje(act_id)
        flash("Actividad de aprendizaje eliminada.", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    return redirect(url_for("fichas.detalle", ficha_id=ficha_id))
