"""Controlador aprendiz — Fichas y fases de formación."""

from flask import flash, redirect, render_template, url_for

from bari_lms.db import get_db
from bari_lms.middleware.auth import current_user, role_required


def _get_aprendiz_fichas(db, user_id):
    return db.execute(
        """
        SELECT f.id, f.numero,
               p.nombre AS programa_nombre,
               pf.nombre AS proyecto_nombre
        FROM ficha_formacion f
        JOIN programa_formacion p ON p.id = f.programa_formacion_id
        LEFT JOIN proyecto_formativo pf ON pf.id = f.proyecto_formativo_id
        JOIN ficha_aprendiz fa ON fa.ficha_id = f.id
        JOIN aprendiz a ON a.id = fa.aprendiz_id
        WHERE a.persona_id = ?
        ORDER BY f.numero ASC
        """,
        (user_id,),
    ).fetchall()


def register_routes(app):

    @app.route("/aprendiz/fichas")
    @role_required("Aprendiz")
    def aprendiz_fichas():
        user = current_user()
        db = get_db()
        fichas = _get_aprendiz_fichas(db, user["id"])
        return render_template(
            "aprendiz/fichas.html",
            user=user,
            fichas=fichas,
            notificaciones=[],
        )

    @app.route("/aprendiz/ficha/<ficha_id>")
    @role_required("Aprendiz")
    def aprendiz_ficha_detalle(ficha_id):
        user = current_user()
        db = get_db()

        # Verificar que el aprendiz pertenece a la ficha
        ficha = db.execute(
            """
            SELECT f.id, f.numero,
                   p.nombre AS programa_nombre,
                   pf.nombre AS proyecto_nombre,
                   pf.id AS proyecto_id,
                   n.nombre AS nivel_nombre
            FROM ficha_formacion f
            JOIN programa_formacion p ON p.id = f.programa_formacion_id
            LEFT JOIN proyecto_formativo pf ON pf.id = f.proyecto_formativo_id
            LEFT JOIN nivel_formacion n ON n.id = p.nivel_formacion_id
            JOIN ficha_aprendiz fa ON fa.ficha_id = f.id
            JOIN aprendiz a ON a.id = fa.aprendiz_id
            WHERE f.id = ? AND a.persona_id = ?
            """,
            (ficha_id, user["id"]),
        ).fetchone()

        if ficha is None:
            flash("No tienes acceso a esta ficha.", "danger")
            return redirect(url_for("aprendiz_fichas"))

        # Construir fases con actividades (a través del proyecto formativo)
        fases = []
        if ficha["proyecto_id"]:
            fases_raw = db.execute(
                """
                SELECT fp.id, fp.nombre AS fase_nombre
                FROM fase_proyecto fp
                WHERE fp.proyecto_formativo_id = ?
                ORDER BY fp.id ASC
                """,
                (ficha["proyecto_id"],),
            ).fetchall()

            for idx, fase in enumerate(fases_raw, start=1):
                actividades_raw = db.execute(
                    """
                    SELECT aa.id, aa.nombre,
                           NULL::text AS codigo
                    FROM actividad_aprendizaje aa
                    JOIN actividad_proyecto ap ON ap.id = aa.actividad_proyecto_id
                    WHERE ap.fase_proyecto_id = ?
                    ORDER BY ap.id ASC, aa.id ASC
                    """,
                    (fase["id"],),
                ).fetchall()

                fases.append({
                    "id": fase["id"],
                    "orden": idx,
                    "fase_nombre": fase["fase_nombre"],
                    "actividades": actividades_raw,
                })

        # Calcular progreso: actividades con entrega calificada >= 75
        total = sum(len(f["actividades"]) for f in fases)
        aprobadas = 0
        if total > 0:
            row = db.execute(
                """
                SELECT COUNT(DISTINCT aa.id) AS cnt
                FROM actividad_aprendizaje aa
                JOIN actividad_proyecto ap ON ap.id = aa.actividad_proyecto_id
                JOIN fase_proyecto fp ON fp.id = ap.fase_proyecto_id
                JOIN evidencia_aprendizaje ea ON ea.actividad_aprendizaje_id = aa.id
                JOIN entrega_evidencia ee ON ee.evidencia_aprendizaje_id = ea.id
                WHERE fp.proyecto_formativo_id = ?
                  AND ee.usuario_id = ?
                  AND ee.calificacion >= 75
                """,
                (ficha["proyecto_id"], user["id"]),
            ).fetchone()
            aprobadas = row["cnt"] if row else 0

        porcentaje = round((aprobadas / total) * 100) if total > 0 else 0

        return render_template(
            "aprendiz/ficha_detalle.html",
            user=user,
            ficha=ficha,
            fases=fases,
            total=total,
            aprobadas=aprobadas,
            porcentaje=porcentaje,
            notificaciones=[],
        )

    @app.route("/aprendiz/fases")
    @role_required("Aprendiz")
    def aprendiz_fases():
        user = current_user()
        db = get_db()
        fichas = _get_aprendiz_fichas(db, user["id"])
        ficha = fichas[0] if fichas else None
        return render_template(
            "aprendiz/fases.html",
            user=user,
            ficha=ficha,
            notificaciones=[],
        )
