"""Controladores del módulo aprendiz."""

from bari_lms.controllers.aprendiz import actividades, cursos, perfil


def register_routes(app):
    cursos.register_routes(app)
    actividades.register_routes(app)
    perfil.register_routes(app)
