"""Controlador aprendiz — Vistas de cursos y competencias."""

from flask import flash, redirect, render_template, url_for
from bari_lms.db import get_db
from bari_lms.middleware.auth import current_user, role_required

def register_routes(app):
    @app.route("/aprendiz/cursos")
    @role_required("Aprendiz")
    def aprendiz_cursos():
        user = current_user()
        db = get_db()
        
        # Buscar el ID del aprendiz a partir de su persona_id
        aprendiz = db.execute(
            "SELECT id, ficha FROM aprendiz WHERE persona_id = ?", (user["id"],)
        ).fetchone()
        
        cursos = []
        if aprendiz and aprendiz["ficha"]:
            ficha_num = aprendiz["ficha"]
            
            # Buscar el curso/ficha al que está matriculado
            ficha = db.execute(
                """
                SELECT f.id, f.numero, f.proyecto_formativo_id,
                       p.nombre AS programa_nombre,
                       pf.nombre AS proyecto_nombre,
                       pf.codigo AS proyecto_codigo,
                       n.nombre AS nivel_nombre
                FROM ficha_formacion f
                JOIN programa_formacion p ON p.id = f.programa_formacion_id
                LEFT JOIN proyecto_formativo pf ON pf.id = f.proyecto_formativo_id
                LEFT JOIN nivel_formacion n ON n.id = p.nivel_formacion_id
                WHERE f.numero = ?
                """,
                (ficha_num,),
            ).fetchone()
            
            if ficha:
                cursos.append(ficha)

        return render_template("aprendiz/cursos.html", user=user, cursos=cursos)
