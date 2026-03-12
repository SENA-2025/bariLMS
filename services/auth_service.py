"""
services/auth_service.py
Lógica de autenticación para bariLMS
"""
from functools import wraps
from flask import session, redirect, url_for
from logger import logger

# Usuarios demo mientras no hay base de datos configurada
DEMO_USERS = {
    "admin@senalearn.edu.co": {
        "password": "Admin123*",
        "role": "Administrador",
        "name": "Laura Moreno",
        "dashboard_slug": "administrador",
    },
    "administrativo@senalearn.edu.co": {
        "password": "Adminvo123*",
        "role": "Administrativo",
        "name": "Carlos Ruiz",
        "dashboard_slug": "administrativo",
    },
    "instructor@senalearn.edu.co": {
        "password": "Instructor123*",
        "role": "Instructor",
        "name": "Diana Beltran",
        "dashboard_slug": "instructor",
    },
    "aprendiz@senalearn.edu.co": {
        "password": "Aprendiz123*",
        "role": "Aprendiz",
        "name": "Miguel Torres",
        "dashboard_slug": "aprendiz",
    },
}


def get_current_user():
    """Retorna el usuario de la sesión activa o None."""
    email = session.get("user_email")
    if not email:
        return None
    user = DEMO_USERS.get(email)
    if user:
        logger.debug("Usuario en sesión: %s (%s)", email, user["role"])
    return user


def validate_login(email: str, password: str, role: str):
    """
    Valida las credenciales del usuario.
    Retorna el usuario si es válido, None si no.
    """
    user = DEMO_USERS.get(email)
    if not user:
        logger.warning("Intento de login con email no registrado: %s", email)
        return None

    if user["password"] != password or user["role"] != role:
        logger.warning("Credenciales inválidas para: %s", email)
        return None

    logger.info("Login exitoso: %s (%s)", email, role)
    return user


def login_required(view):
    """Decorador que protege rutas que requieren autenticación."""
    @wraps(view)
    def wrapped_view(**kwargs):
        user = get_current_user()
        if user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view
