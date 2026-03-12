"""
models/models.py
Modelos de datos para bariLMS - SENA
"""
from enum import Enum as PyEnum
import datetime
from sqlalchemy import String, DateTime, ForeignKey, Enum as SQLEnum, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Importar db desde app (import local para evitar circularidad)
from app import db


class RolUsuario(PyEnum):
    ADMINISTRADOR = "Administrador"
    ADMINISTRATIVO = "Administrativo"
    INSTRUCTOR = "Instructor"
    APRENDIZ = "Aprendiz"


class EstadoFicha(PyEnum):
    EN_EJECUCION = "En ejecucion"
    FINALIZADA = "Finalizada"
    POR_INICIAR = "Por iniciar"


class Usuario(db.Model):
    """Tabla base de usuarios del sistema."""
    __tablename__ = "usuarios"
    __table_args__ = {"extend_existing": True}

    usuario_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    apellido: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    rol: Mapped[RolUsuario] = mapped_column(SQLEnum(RolUsuario), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    creado_en: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    def to_dict(self):
        return {
            "usuario_id": self.usuario_id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "rol": self.rol.value,
            "activo": self.activo,
        }

    def __repr__(self):
        return f"Usuario({self.nombre} {self.apellido} - {self.rol.value})"
