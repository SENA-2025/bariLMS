"""Controlador aprendiz — Registro de módulos y vistas."""

from bari_lms.controllers.aprendiz import cursos, actividades

def register_routes(app):
    cursos.register_routes(app)
    actividades.register_routes(app)
