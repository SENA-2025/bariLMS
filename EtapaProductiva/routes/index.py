import copy
import os

from flask import Blueprint, flash, redirect, render_template, request, url_for

from shared_auth.sso import make_token
from utils.DemoClassesIndex import DASHBOARDS
from utils.DemoAuth import DemoAuth

index = Blueprint("index", __name__)

_BARILMS_BASE = os.getenv("BARILMS_URL", "http://localhost:5000")


def _sso_url(email: str, path: str) -> str:
    return f"{_BARILMS_BASE}/sso?token={make_token(email)}&next={path}"


# ── Home / dashboard ─────────────────────────────────────────────

@index.route("/", methods=["GET"])
def home():
    user = DemoAuth.current_user()
    if user is None:
        return redirect(url_for("index.login"))

    slug = user.get("dashboard_slug", "administrador")
    dashboard = copy.deepcopy(DASHBOARDS.get(slug, DASHBOARDS["administrador"]))

    for item in dashboard.get("menu", []):
        item["href"] = _sso_url(user["email"], item["href"].replace(_BARILMS_BASE, ""))

    return render_template(
        "etapa_Productiva/dashboard.html",
        dashboard=dashboard,
        user=user,
        session_user_email=user["email"],
    )


# ── Auth ─────────────────────────────────────────────────────────

@index.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        role = request.form.get("role", "")

        user = DemoAuth.validate_login(email, password, role)
        if user is None:
            flash("Credenciales o perfil incorrectos. Usa uno de los accesos demo.", "danger")
            return render_template("login.html", demo_users=DemoAuth.DEMO_USERS)

        DemoAuth.login_user(user)
        return redirect(url_for("index.home"))

    if DemoAuth.current_user():
        return redirect(url_for("index.home"))

    return render_template("login.html", demo_users=DemoAuth.DEMO_USERS)
