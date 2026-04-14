"""Controladores del módulo aprendiz."""

from bari_lms.controllers.aprendiz import calificaciones, evidencias, fichas, perfil


def register_routes(app):
    fichas.register_routes(app)
    calificaciones.register_routes(app)
    evidencias.register_routes(app)
    perfil.register_routes(app)
