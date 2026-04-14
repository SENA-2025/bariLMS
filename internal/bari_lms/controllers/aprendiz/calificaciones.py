"""Controlador aprendiz — Calificaciones y entregas."""

from flask import render_template

from bari_lms.db import get_db
from bari_lms.middleware.auth import current_user, role_required


def register_routes(app):

    @app.route("/aprendiz/calificaciones")
    @role_required("Aprendiz")
    def aprendiz_calificaciones():
        user = current_user()
        db = get_db()

        calificaciones = db.execute(
            """
            SELECT fp.nombre AS fase_nombre,
                   ap.nombre AS actividad_proyecto_nombre,
                   aa.nombre AS actividad_aprendizaje_nombre,
                   f.numero AS ficha_numero,
                   ee.url AS url_evidencia,
                   ee.calificacion,
                   ee.observaciones AS retroalimentacion,
                   CASE
                       WHEN ee.calificacion >= 75 THEN 1
                       WHEN ee.calificacion IS NOT NULL THEN 0
                       ELSE NULL
                   END AS aprueba
            FROM entrega_evidencia ee
            JOIN evidencia_aprendizaje ea ON ea.id = ee.evidencia_aprendizaje_id
            JOIN actividad_aprendizaje aa ON aa.id = ea.actividad_aprendizaje_id
            JOIN actividad_proyecto ap ON ap.id = aa.actividad_proyecto_id
            JOIN fase_proyecto fp ON fp.id = ap.fase_proyecto_id
            JOIN ficha_formacion f ON f.proyecto_formativo_id = fp.proyecto_formativo_id
            JOIN ficha_aprendiz fa ON fa.ficha_id = f.id
            JOIN aprendiz a ON a.id = fa.aprendiz_id AND a.persona_id = ?
            WHERE ee.usuario_id = ?
            ORDER BY fp.id ASC, ap.id ASC, aa.id ASC
            """,
            (user["id"], user["id"]),
        ).fetchall()

        total = len(calificaciones)
        aprobadas = sum(1 for c in calificaciones if c["calificacion"] is not None and c["calificacion"] >= 75)
        pendientes = sum(1 for c in calificaciones if c["calificacion"] is None)
        notas = [c["calificacion"] for c in calificaciones if c["calificacion"] is not None]
        promedio = round(sum(notas) / len(notas), 1) if notas else "—"

        resumen = {
            "total": total,
            "aprobadas": aprobadas,
            "pendientes": pendientes,
            "promedio": promedio,
        }

        return render_template(
            "aprendiz/calificaciones.html",
            user=user,
            calificaciones=calificaciones,
            resumen=resumen,
            notificaciones=[],
        )
