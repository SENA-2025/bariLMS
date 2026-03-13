"""
routes/aprendices_routes.py
CRUD de Aprendices + carga masiva
"""
import datetime
import io as io_module
from flask import Blueprint, flash, redirect, render_template, request, url_for, send_file, session
from services.auth_service import login_required
from services import aprendices_service, fichas_service
from logger import logger

aprendices_routes = Blueprint("aprendices", __name__, url_prefix="/aprendices")


# ---------------------------------------------------------------------------
# Lista general
# ---------------------------------------------------------------------------

@aprendices_routes.get("/")
@login_required
def lista():
    ficha_filtro = request.args.get("ficha_id", "")
    estado_filtro = request.args.get("estado", "")
    aprendices = aprendices_service.listar_aprendices(
        ficha_id=ficha_filtro or None,
        estado=estado_filtro or None,
    )
    return render_template(
        "aprendices/aprendices.html",
        aprendices=aprendices,
        fichas=fichas_service.listar_fichas(),
        ficha_filtro=ficha_filtro,
        estado_filtro=estado_filtro,
    )


# ---------------------------------------------------------------------------
# Crear aprendiz (desde detalle de ficha)
# ---------------------------------------------------------------------------

@aprendices_routes.post("/crear/<ficha_id>")
@login_required
def crear(ficha_id):
    try:
        fecha_str = request.form.get("fecha_ingreso", "")
        fecha_ingreso = datetime.datetime.strptime(fecha_str, "%Y-%m-%d") if fecha_str else datetime.datetime.utcnow()
        aprendices_service.crear_aprendiz(
            ficha_id=ficha_id,
            tipo_documento=request.form["tipo_documento"],
            identificacion=request.form["identificacion"],
            correo=request.form["correo"],
            primer_nombre=request.form["primer_nombre"],
            segundo_nombre=request.form.get("segundo_nombre") or None,
            primer_apellido=request.form["primer_apellido"],
            segundo_apellido=request.form.get("segundo_apellido") or None,
            contrasena=request.form["contrasena"],
            fecha_ingreso=fecha_ingreso,
        )
        flash("Aprendiz agregado correctamente.", "success")
    except Exception as e:
        flash(f"Error al agregar aprendiz: {e}", "danger")
        logger.error("Error crear aprendiz: %s", e)
    return redirect(url_for("fichas.detalle", ficha_id=ficha_id))


# ---------------------------------------------------------------------------
# Editar estado de aprendiz
# ---------------------------------------------------------------------------

@aprendices_routes.post("/<aprendiz_id>/editar")
@login_required
def editar(aprendiz_id):
    aprendiz = aprendices_service.obtener_aprendiz(aprendiz_id)
    ficha_id = aprendiz.ficha_id
    try:
        aprendices_service.editar_aprendiz(aprendiz_id, request.form["estado"])
        flash("Estado actualizado.", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    return redirect(url_for("fichas.detalle", ficha_id=ficha_id))


# ---------------------------------------------------------------------------
# Eliminar aprendiz
# ---------------------------------------------------------------------------

@aprendices_routes.post("/<aprendiz_id>/eliminar")
@login_required
def eliminar(aprendiz_id):
    redirect_ficha = request.form.get("redirect_ficha")
    try:
        aprendices_service.eliminar_aprendiz(aprendiz_id)
        flash("Aprendiz eliminado.", "success")
    except Exception as e:
        flash(f"No se puede eliminar: {e}", "danger")
    if redirect_ficha:
        return redirect(url_for("fichas.detalle", ficha_id=redirect_ficha))
    return redirect(url_for("aprendices.lista"))


# ---------------------------------------------------------------------------
# Carga masiva
# ---------------------------------------------------------------------------

@aprendices_routes.get("/carga-masiva")
@aprendices_routes.get("/carga-masiva/<ficha_id>")
@login_required
def carga_masiva(ficha_id=None):
    resultados = session.pop("carga_masiva_resultado", None)
    return render_template(
        "aprendices/carga_masiva.html",
        fichas=fichas_service.listar_fichas(),
        ficha_id=ficha_id,
        resultados=resultados,
    )


@aprendices_routes.post("/carga-masiva/procesar")
@login_required
def procesar_carga_masiva():
    archivo = request.files.get("archivo")
    ficha_id = request.form.get("ficha_id", "")
    contrasena = request.form.get("contrasena", "")
    fecha_str = request.form.get("fecha_ingreso", "")

    if not archivo or not ficha_id or not contrasena or not fecha_str:
        flash("Todos los campos son obligatorios.", "danger")
        return redirect(url_for("aprendices.carga_masiva"))

    try:
        fecha_ingreso = datetime.datetime.strptime(fecha_str, "%Y-%m-%d")
        resultados = aprendices_service.procesar_carga_masiva(archivo, ficha_id, contrasena, fecha_ingreso)
        flash(
            f"Carga completada: {resultados['creados']} creados, "
            f"{resultados['omitidos']} omitidos, {len(resultados['errores'])} errores.",
            "success" if not resultados["errores"] else "warning",
        )
        session["carga_masiva_resultado"] = resultados
    except Exception as e:
        flash(f"Error al procesar archivo: {e}", "danger")
        logger.error("Error carga masiva: %s", e)

    return redirect(url_for("aprendices.carga_masiva", ficha_id=ficha_id))


@aprendices_routes.get("/carga-masiva/plantilla")
@login_required
def descargar_plantilla():
    contenido = aprendices_service.generar_plantilla_excel()
    return send_file(
        io_module.BytesIO(contenido),
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name="plantilla_aprendices.xlsx",
    )
