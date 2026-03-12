"""
routes/dashboard_routes.py
Blueprint de dashboards por rol
"""
from flask import Blueprint, redirect, render_template, url_for
from services.auth_service import get_current_user, login_required
from logger import logger

dashboard_routes = Blueprint("dashboard", __name__)

# Datos de cada dashboard por rol
DASHBOARDS = {
    "administrador": {
        "role": "Administrador",
        "icon": "fa-user-shield",
        "area": "Direccionamiento institucional",
        "title": "Tablero del Administrador",
        "text": "Supervisa la operacion general de BARÍ LMS, define lineamientos y controla el acceso de los perfiles del LMS.",
        "footer": "BARÍ LMS SENA - Administrador",
        "menu_heading": "Administracion",
        "menu": [
            {"icon": "fa-users-cog", "label": "Usuarios y roles"},
            {"icon": "fa-chart-pie", "label": "Indicadores"},
        ],
        "metrics": [
            {"label": "Usuarios activos", "value": "1,284", "icon": "fa-users"},
            {"label": "Centros vinculados", "value": "14", "icon": "fa-building"},
            {"label": "Roles configurados", "value": "4", "icon": "fa-user-shield"},
            {"label": "Sesiones hoy", "value": "326", "icon": "fa-sign-in-alt"},
        ],
        "tasks_title": "Frentes prioritarios",
        "tasks": [
            {"title": "Gestion de usuarios", "text": "Aprobar nuevas cuentas y validar asignacion de perfiles."},
            {"title": "Configuracion LMS", "text": "Definir parametros base, regionales y politicas institucionales."},
            {"title": "Seguimiento", "text": "Consultar indicadores de uso, permanencia y actividad por centro."},
        ],
        "table_title": "Resumen operativo",
        "table_headers": ["Unidad", "Estado", "Observacion"],
        "table_rows": [
            ["Regional Distrito Capital", "98%", "Sin novedades"],
            ["Regional Antioquia", "94%", "Actualizar instructores"],
            ["Regional Valle", "91%", "Revision de permisos"],
        ],
    },
    "administrativo": {
        "role": "Administrativo",
        "icon": "fa-clipboard-check",
        "area": "Apoyo academico y operativo",
        "title": "Tablero Administrativo",
        "text": "Consolida fichas, programas, ambientes y apoyo documental para el despliegue de la formacion por proyectos.",
        "footer": "BARÍ LMS SENA - Administrativo",
        "menu_heading": "Operacion",
        "menu": [
            {"icon": "fa-folder-open", "label": "Fichas y programas"},
            {"icon": "fa-school", "label": "Ambientes y sedes"},
        ],
        "metrics": [
            {"label": "Fichas activas", "value": "86", "icon": "fa-id-badge"},
            {"label": "Programas", "value": "27", "icon": "fa-graduation-cap"},
            {"label": "Ambientes", "value": "49", "icon": "fa-door-open"},
            {"label": "Solicitudes", "value": "12", "icon": "fa-clipboard-list"},
        ],
        "tasks_title": "Pendientes",
        "tasks": [
            {"title": "Matricula", "text": "Consolidar aprendices por ficha y programa."},
            {"title": "Ambientes", "text": "Validar capacidad y disponibilidad por sede."},
            {"title": "Soporte documental", "text": "Publicar formatos y circulares internas."},
        ],
        "table_title": "Control academico",
        "table_headers": ["Ficha", "Programa", "Estado"],
        "table_rows": [
            ["ADSI 2675854", "Analisis y Desarrollo", "Completa"],
            ["SST 2675921", "Seguridad y Salud", "Pendiente soporte"],
            ["Cocina 2676018", "Tecnico en Cocina", "Actualizada"],
        ],
    },
    "instructor": {
        "role": "Instructor",
        "icon": "fa-chalkboard-teacher",
        "area": "Ejecucion formativa",
        "title": "Tablero del Instructor",
        "text": "Organiza resultados de aprendizaje, evidencias, proyectos y seguimiento del avance de cada ficha.",
        "footer": "BARÍ LMS SENA - Instructor",
        "menu_heading": "Formacion",
        "menu": [
            {"icon": "fa-book-reader", "label": "Planeacion"},
            {"icon": "fa-clipboard-check", "label": "Evaluacion"},
        ],
        "metrics": [
            {"label": "Fichas a cargo", "value": "6", "icon": "fa-layer-group"},
            {"label": "Proyectos activos", "value": "18", "icon": "fa-project-diagram"},
            {"label": "Evidencias por revisar", "value": "43", "icon": "fa-tasks"},
            {"label": "Alertas de asistencia", "value": "5", "icon": "fa-user-clock"},
        ],
        "tasks_title": "Acciones docentes",
        "tasks": [
            {"title": "Planeacion", "text": "Programar actividades alineadas al proyecto formativo."},
            {"title": "Seguimiento", "text": "Retroalimentar evidencias y avances semanales."},
            {"title": "Evaluacion", "text": "Registrar desempeno por resultado de aprendizaje."},
        ],
        "table_title": "Seguimiento de fichas",
        "table_headers": ["Ficha", "Actividad", "Estado"],
        "table_rows": [
            ["Ficha 2675854", "Sprint de prototipo", "15 entregas pendientes"],
            ["Ficha 2675860", "Sustentacion parcial", "Programada"],
            ["Ficha 2675902", "Bitacora de proyecto", "Al dia"],
        ],
    },
    "aprendiz": {
        "role": "Aprendiz",
        "icon": "fa-user-graduate",
        "area": "Ruta de aprendizaje",
        "title": "Tablero del Aprendiz",
        "text": "Consulta tu avance del proyecto, entregas, evidencias, horario y comunicados del proceso formativo.",
        "footer": "BARÍ LMS SENA - Aprendiz",
        "menu_heading": "Aprendizaje",
        "menu": [
            {"icon": "fa-project-diagram", "label": "Mi proyecto"},
            {"icon": "fa-file-alt", "label": "Evidencias"},
        ],
        "metrics": [
            {"label": "Avance general", "value": "72%", "icon": "fa-chart-line"},
            {"label": "Evidencias pendientes", "value": "4", "icon": "fa-file-upload"},
            {"label": "Resultados aprobados", "value": "11", "icon": "fa-check-circle"},
            {"label": "Mensajes nuevos", "value": "3", "icon": "fa-comments"},
        ],
        "tasks_title": "Ruta personal",
        "tasks": [
            {"title": "Proyecto formativo", "text": "Consultar entregables y fechas de corte."},
            {"title": "Ruta individual", "text": "Ver resultados alcanzados y faltantes."},
            {"title": "Comunicacion", "text": "Revisar mensajes de instructor y coordinacion."},
        ],
        "table_title": "Proximas entregas",
        "table_headers": ["Actividad", "Fecha", "Estado"],
        "table_rows": [
            ["Bitacora semanal", "14 de marzo de 2026", "Pendiente"],
            ["Prototipo funcional", "18 de marzo de 2026", "En progreso"],
            ["Autoevaluacion", "20 de marzo de 2026", "No iniciada"],
        ],
    },
}


@dashboard_routes.context_processor
def inject_session_user():
    from flask import session as flask_session
    return {
        "session_user": get_current_user(),
        "session_user_email": flask_session.get("user_email", ""),
    }


@dashboard_routes.route("/dashboard/<role_slug>")
@login_required
def dashboard_view(role_slug):
    user = get_current_user()
    dash_config = DASHBOARDS.get(role_slug)

    if dash_config is None:
        logger.warning("Dashboard no encontrado para slug: %s", role_slug)
        return redirect(url_for("auth.home"))

    if user["dashboard_slug"] != role_slug:
        logger.warning(
            "Acceso no autorizado al dashboard '%s' por usuario con rol '%s'",
            role_slug,
            user["role"],
        )
        return redirect(url_for("dashboard.dashboard_view", role_slug=user["dashboard_slug"]))

    return render_template("dashboard.html", dashboard=dash_config, user=user)
