"""Controlador aprendiz — Entrega de evidencias."""

import uuid

from flask import flash, jsonify, redirect, request, url_for

from bari_lms.db import get_db
from bari_lms.middleware.auth import current_user, role_required


def register_routes(app):

    @app.post("/aprendiz/entregar-evidencia")
    @role_required("Aprendiz")
    def aprendiz_entregar_evidencia():
        user = current_user()
        db = get_db()

        actividad_id = request.form.get("actividad_aprendizaje_id", "").strip()
        ficha_id = request.form.get("ficha_id", "").strip()
        url_evidencia = request.form.get("url_evidencia", "").strip()

        if not actividad_id or not url_evidencia:
            flash("Faltan datos para registrar la entrega.", "danger")
            return redirect(url_for("aprendiz_ficha_detalle", ficha_id=ficha_id) if ficha_id else url_for("aprendiz_fichas"))

        # Obtener o crear la evidencia_aprendizaje para esta actividad
        evidencia = db.execute(
            "SELECT id FROM evidencia_aprendizaje WHERE actividad_aprendizaje_id = ?",
            (actividad_id,),
        ).fetchone()

        if evidencia is None:
            evidencia = db.execute(
                "INSERT INTO evidencia_aprendizaje (id, actividad_aprendizaje_id) VALUES (?, ?) RETURNING id",
                (str(uuid.uuid7()), actividad_id),
            ).fetchone()
            db.commit()

        evidencia_id = evidencia["id"]

        # Verificar si ya existe una entrega de este aprendiz
        existing = db.execute(
            "SELECT id FROM entrega_evidencia WHERE evidencia_aprendizaje_id = ? AND usuario_id = ?",
            (evidencia_id, user["id"]),
        ).fetchone()

        if existing:
            db.execute(
                "UPDATE entrega_evidencia SET url = ? WHERE id = ?",
                (url_evidencia, existing["id"]),
            )
            flash("Entrega actualizada correctamente.", "success")
        else:
            db.execute(
                "INSERT INTO entrega_evidencia (id, evidencia_aprendizaje_id, usuario_id, url) VALUES (?, ?, ?, ?)",
                (str(uuid.uuid7()), evidencia_id, user["id"], url_evidencia),
            )
            flash("Evidencia entregada correctamente.", "success")

        db.commit()

        if ficha_id:
            return redirect(url_for("aprendiz_ficha_detalle", ficha_id=ficha_id))
        return redirect(url_for("aprendiz_fichas"))

    @app.post("/aprendiz/notificaciones/marcar-leida/<int:notif_id>")
    @role_required("Aprendiz")
    def aprendiz_marcar_notificacion_leida(notif_id):
        return jsonify({"ok": True})
