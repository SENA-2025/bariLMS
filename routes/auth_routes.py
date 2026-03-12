"""
routes/auth_routes.py
Blueprint de autenticación: login y logout
"""
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from services.auth_service import DEMO_USERS, get_current_user, validate_login
from logger import logger

auth_routes = Blueprint("auth", __name__)


@auth_routes.route("/")
def home():
    user = get_current_user()
    if user:
        return redirect(url_for("dashboard.dashboard_view", role_slug=user["dashboard_slug"]))
    return redirect(url_for("auth.login"))


@auth_routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        role = request.form.get("role", "")

        user = validate_login(email, password, role)

        if not user:
            flash(
                "Credenciales o perfil incorrectos. Usa uno de los accesos demo listados.",
                "danger",
            )
            return render_template("login.html", demo_users=DEMO_USERS)

        session.clear()
        session["user_email"] = email
        logger.info("Sesión iniciada para: %s", email)
        return redirect(url_for("dashboard.dashboard_view", role_slug=user["dashboard_slug"]))

    if get_current_user():
        return redirect(url_for("auth.home"))

    return render_template("login.html", demo_users=DEMO_USERS)


@auth_routes.post("/logout")
def logout():
    email = session.get("user_email", "desconocido")
    session.clear()
    logger.info("Sesión cerrada para: %s", email)
    return redirect(url_for("auth.login"))
