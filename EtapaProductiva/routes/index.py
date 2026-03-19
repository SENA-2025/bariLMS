from flask import Blueprint, render_template

index = Blueprint("index", __name__)

@index.route("/", methods=["GET"])
def home():
    dashboard = {
        "title": "Panel de Control",
        "text": "Bienvenido al sistema",
        "menu_heading": "Menú principal",
        "menu": [
            {"label": "Cursos", "icon": "fa-book", "endpoint": "index.home"},
            {"label": "Usuarios", "icon": "fa-users", "endpoint": "index.home"},
        ],
        "metrics": [
            {"label": "Cursos", "value": 10},
            {"label": "Usuarios", "value": 50},
        ],
        "table_headers": ["Nombre", "Estado"],
        "table_rows": [["Curso 1", "Activo"], ["Curso 2", "Inactivo"]],
        "footer": "BARÍ LMS 2026"
    }

    user = {
        "name": "Admin",
        "role": "Administrador",
        "dashboard_slug": "admin"
    }

    return render_template(
        "etapa_Productiva/dashboard.html",
        dashboard=dashboard,
        user=user,
        session_user_email="admin@test.com"
    )