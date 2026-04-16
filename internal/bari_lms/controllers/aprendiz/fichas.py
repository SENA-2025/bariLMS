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

        # Construir fases → actividades_proyecto → actividades_aprendizaje con URLs
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
                # Actividades de proyecto con su plan de trabajo concertado
                acts_proyecto = db.execute(
                    """
                    SELECT ap.id, ap.nombre,
                           gap.url AS plan_trabajo_url
                    FROM actividad_proyecto ap
                    LEFT JOIN guia_actividad_proyecto gap ON gap.actividad_proyecto_id = ap.id
                    WHERE ap.fase_proyecto_id = ?
                    ORDER BY ap.creado_en ASC
                    """,
                    (fase["id"],),
                ).fetchall()

                actividades_proyecto = []
                for ap in acts_proyecto:
                    # Actividades de aprendizaje con guía y entrega del aprendiz
                    acts_aprendizaje = db.execute(
                        """
                        SELECT aa.id, aa.nombre, aa.descripcion,
                               ga.url AS guia_url,
                               ee.url AS evidencia_url,
                               ee.calificacion
                        FROM actividad_aprendizaje aa
                        LEFT JOIN guia_aprendizaje ga ON ga.actividad_aprendizaje_id = aa.id
                        LEFT JOIN evidencia_aprendizaje ea ON ea.actividad_aprendizaje_id = aa.id
                        LEFT JOIN entrega_evidencia ee ON ee.evidencia_aprendizaje_id = ea.id
                                                      AND ee.usuario_id = ?
                        WHERE aa.actividad_proyecto_id = ?
                        ORDER BY aa.orden ASC, aa.creado_en ASC
                        """,
                        (user["id"], ap["id"]),
                    ).fetchall()

                    actividades_proyecto.append({
                        "id": ap["id"],
                        "nombre": ap["nombre"],
                        "plan_trabajo_url": ap["plan_trabajo_url"],
                        "actividades_aprendizaje": acts_aprendizaje,
                    })

                fases.append({
                    "id": fase["id"],
                    "orden": idx,
                    "fase_nombre": fase["fase_nombre"],
                    "actividades_proyecto": actividades_proyecto,
                })

        # Calcular progreso: actividades de aprendizaje con entrega calificada >= 75
        total = sum(
            len(ap["actividades_aprendizaje"])
            for f in fases
            for ap in f["actividades_proyecto"]
        )
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
