"""Controlador del dashboard: redirige a la vista del perfil activo."""

from flask import redirect, render_template, url_for

from bari_lms.config import DASHBOARDS
from bari_lms.db import get_db
from bari_lms.middleware.auth import current_user, login_required
from bari_lms.repositories.usuario import get_admin_dashboard_data


def _get_aprendiz_user_info(db, user_id):
    """Retorna info de ficha y programa del aprendiz autenticado."""
    return db.execute(
        """
        SELECT f.numero AS ficha_numero,
               p.nombre AS programa_nombre
        FROM aprendiz a
        JOIN ficha_formacion f ON f.numero = a.ficha
        JOIN programa_formacion p ON p.id = f.programa_formacion_id
        WHERE a.persona_id = ?
        LIMIT 1
        """,
        (user_id,),
    ).fetchone()


def register_routes(app):
    @app.route("/dashboard/<role_slug>")
    @login_required
    def dashboard(role_slug):
        user = current_user()
        config = DASHBOARDS.get(role_slug)

        if config is None:
            return redirect(url_for("home"))

        if user["dashboard_slug"] != role_slug:
            return redirect(url_for("dashboard", role_slug=user["dashboard_slug"]))

        if role_slug == "administrador":
            config = get_admin_dashboard_data()

        if role_slug == "aprendiz":
            db = get_db()
            user_info = _get_aprendiz_user_info(db, user["id"])
            return render_template("aprendiz/dashboard.html", user=user, user_info=user_info)

        return render_template("dashboard.html", dashboard=config, user=user)
