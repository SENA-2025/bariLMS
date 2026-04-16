"""Controlador aprendiz — Mis Cursos."""

from flask import flash, redirect, render_template, url_for

from bari_lms.db import get_db
from bari_lms.middleware.auth import current_user, role_required


def register_routes(app):

    @app.route("/aprendiz/cursos")
    @role_required("Aprendiz")
    def aprendiz_cursos():
        user = current_user()
        db = get_db()

        cursos = db.execute(
            """
            SELECT f.id, f.numero,
                   p.nombre  AS programa_nombre,
                   pf.nombre AS proyecto_nombre,
                   pf.codigo AS proyecto_codigo,
                   n.nombre  AS nivel_nombre
            FROM ficha_formacion f
            JOIN programa_formacion p  ON p.id  = f.programa_formacion_id
            LEFT JOIN proyecto_formativo pf ON pf.id = f.proyecto_formativo_id
            LEFT JOIN nivel_formacion n    ON n.id  = p.nivel_formacion_id
            JOIN ficha_aprendiz fa ON fa.ficha_id = f.id
            JOIN aprendiz a        ON a.id        = fa.aprendiz_id
            WHERE a.persona_id = ?
            ORDER BY f.numero ASC
            """,
            (user["id"],),
        ).fetchall()

        return render_template(
            "aprendiz/cursos.html",
            user=user,
            cursos=cursos,
            notificaciones=[],
        )
