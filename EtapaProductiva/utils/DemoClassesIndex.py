import os

BARILMS_BASE = os.getenv("BARILMS_URL", "http://localhost:5000")

DASHBOARDS = {
    "administrador": {
        "role": "Administrador",
        "area": "Direccionamiento institucional",
        "title": "Tablero del Administrador",
        "text": "Supervisa la operación general de BARÍ LMS, define lineamientos y controla el acceso de los perfiles del LMS.",
        "footer": "BARÍ LMS SENA - Administrador",
        "menu_heading": "Administración",
        "menu": [
            {"icon": "fa-users-cog",      "label": "Usuarios y roles",         "href": f"{BARILMS_BASE}/admin/users"},
            {"icon": "fa-user-friends",    "label": "Gestionar personas",       "href": f"{BARILMS_BASE}/admin/people"},
            {"icon": "fa-sitemap",         "label": "Estructura institucional", "href": f"{BARILMS_BASE}/admin/structure"},
            {"icon": "fa-graduation-cap",  "label": "Gestión académica",        "href": f"{BARILMS_BASE}/admin/academic"},
            {"icon": "fa-chart-pie",       "label": "Indicadores",              "href": f"{BARILMS_BASE}/dashboard/administrador"},
        ],
        "metrics": [
            {"label": "Usuarios activos",   "value": "0", "icon": "fa-users"},
            {"label": "Regionales",         "value": "0", "icon": "fa-map-marked-alt"},
            {"label": "Roles configurados", "value": "0", "icon": "fa-user-shield"},
            {"label": "Centros",            "value": "0", "icon": "fa-building"},
        ],
        "tasks_title": "Frentes prioritarios",
        "tasks": [
            {"title": "Gestión de usuarios",      "text": "Aprobar nuevas cuentas y validar asignación de perfiles."},
            {"title": "Estructura institucional",  "text": "Administrar regionales, centros, coordinaciones, sedes y ambientes."},
            {"title": "Seguimiento",               "text": "Consultar indicadores de uso, permanencia y actividad por centro."},
        ],
        "table_title": "Resumen operativo",
        "table_headers": ["Unidad", "Estado", "Observación"],
        "table_rows": [
            ["Regional Distrito Capital", "98%", "Sin novedades"],
            ["Regional Antioquia",        "94%", "Actualizar instructores"],
            ["Regional Valle",            "91%", "Revisión de permisos"],
        ],
    },
    "instructor": {
        "role": "Instructor",
        "area": "Ejecución formativa",
        "title": "Tablero del Instructor",
        "text": "Organiza resultados de aprendizaje, evidencias, proyectos y seguimiento del avance de cada ficha.",
        "footer": "BARÍ LMS SENA - Instructor",
        "menu_heading": "Formación",
        "menu": [
            {"icon": "fa-book-reader",      "label": "Planeación",         "href": f"{BARILMS_BASE}/dashboard/instructor"},
            {"icon": "fa-clipboard-check",  "label": "Evaluación",         "href": f"{BARILMS_BASE}/dashboard/instructor"},
            {"icon": "fa-key",              "label": "Cambiar contraseña", "href": f"{BARILMS_BASE}/instructor/password"},
        ],
        "metrics": [
            {"label": "Fichas a cargo",         "value": "6",  "icon": "fa-layer-group"},
            {"label": "Proyectos activos",       "value": "18", "icon": "fa-project-diagram"},
            {"label": "Evidencias por revisar",  "value": "43", "icon": "fa-tasks"},
            {"label": "Alertas de asistencia",   "value": "5",  "icon": "fa-user-clock"},
        ],
        "tasks_title": "Acciones docentes",
        "tasks": [
            {"title": "Planeación",   "text": "Programar actividades alineadas al proyecto formativo."},
            {"title": "Seguimiento",  "text": "Retroalimentar evidencias y avances semanales."},
            {"title": "Evaluación",   "text": "Registrar desempeño por resultado de aprendizaje."},
        ],
        "table_title": "Seguimiento de fichas",
        "table_headers": ["Ficha", "Actividad", "Estado"],
        "table_rows": [
            ["Ficha 2675854", "Sprint de prototipo",  "15 entregas pendientes"],
            ["Ficha 2675860", "Sustentación parcial", "Programada"],
            ["Ficha 2675902", "Bitácora de proyecto", "Al día"],
        ],
    },
    "aprendiz": {
        "role": "Aprendiz",
        "area": "Ruta de aprendizaje",
        "title": "Tablero del Aprendiz",
        "text": "Consulta tu avance del proyecto, entregas, evidencias, horario y comunicados del proceso formativo.",
        "footer": "BARÍ LMS SENA - Aprendiz",
        "menu_heading": "Aprendizaje",
        "menu": [
            {"icon": "fa-project-diagram", "label": "Mi proyecto", "href": f"{BARILMS_BASE}/dashboard/aprendiz"},
            {"icon": "fa-file-alt",        "label": "Evidencias",  "href": f"{BARILMS_BASE}/dashboard/aprendiz"},
        ],
        "metrics": [
            {"label": "Avance general",        "value": "72%", "icon": "fa-chart-line"},
            {"label": "Evidencias pendientes", "value": "4",   "icon": "fa-file-upload"},
            {"label": "Resultados aprobados",  "value": "11",  "icon": "fa-check-circle"},
            {"label": "Mensajes nuevos",       "value": "3",   "icon": "fa-comments"},
        ],
        "tasks_title": "Ruta personal",
        "tasks": [
            {"title": "Proyecto formativo", "text": "Consultar entregables y fechas de corte."},
            {"title": "Ruta individual",    "text": "Ver resultados alcanzados y faltantes."},
            {"title": "Comunicación",       "text": "Revisar mensajes de instructor y coordinación."},
        ],
        "table_title": "Próximas entregas",
        "table_headers": ["Actividad", "Fecha", "Estado"],
        "table_rows": [
            ["Bitácora semanal",    "14 de marzo de 2026", "Pendiente"],
            ["Prototipo funcional", "18 de marzo de 2026", "En progreso"],
            ["Autoevaluacion",      "20 de marzo de 2026", "No iniciada"],
        ],
    },
}

dashboard = DASHBOARDS["administrador"]
