"""
models/models.py
Modelos SQLAlchemy para bariLMS - SENA (MariaDB / MySQL)
PKs: CHAR(36) con UUID generado en Python para coincidir con el schema MariaDB.
"""
import uuid
import datetime
from sqlalchemy import (
    String, Text, DateTime, ForeignKey, SmallInteger,
    Integer, BigInteger, Boolean, Date, Enum as SAEnum, UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app import db


def _uuid():
    return str(uuid.uuid4())


# ---------------------------------------------------------------------------
# Catálogos
# ---------------------------------------------------------------------------

class CatalogoParentesco(db.Model):
    __tablename__ = "catalogo_parentescos"
    parentesco_id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    fecha_actualizacion: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)


class CatalogoGenero(db.Model):
    __tablename__ = "catalogo_generos"
    genero_id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    fecha_actualizacion: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)


class CatalogoEstadoCivil(db.Model):
    __tablename__ = "catalogo_estado_civil"
    estado_civil_id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    fecha_actualizacion: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)


class CatalogoEps(db.Model):
    __tablename__ = "catalogo_eps"
    eps_id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    fecha_actualizacion: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)


class CatalogoLibretaMilitar(db.Model):
    __tablename__ = "catalogo_libreta_militar"
    libreta_militar_id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    fecha_actualizacion: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)


# ---------------------------------------------------------------------------
# Roles
# ---------------------------------------------------------------------------

class Rol(db.Model):
    __tablename__ = "roles"
    rol_id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    descripcion: Mapped[str | None] = mapped_column(String(255), nullable=True)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    fecha_actualizacion: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)

    usuarios: Mapped[list["Usuario"]] = relationship("Usuario", back_populates="rol_obj")


# ---------------------------------------------------------------------------
# Ubicaciones
# ---------------------------------------------------------------------------

class UbicacionPais(db.Model):
    __tablename__ = "ubicacion_paises"
    pais_id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    fecha_actualizacion: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)

    departamentos: Mapped[list["UbicacionDepartamento"]] = relationship(back_populates="pais")


class UbicacionDepartamento(db.Model):
    __tablename__ = "ubicacion_departamentos"
    departamento_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pais_id: Mapped[int] = mapped_column(SmallInteger, ForeignKey("ubicacion_paises.pais_id"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    fecha_actualizacion: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)

    pais: Mapped["UbicacionPais"] = relationship(back_populates="departamentos")
    municipios: Mapped[list["UbicacionMunicipio"]] = relationship(back_populates="departamento")


class UbicacionMunicipio(db.Model):
    __tablename__ = "ubicacion_municipios"
    municipio_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    departamento_id: Mapped[int] = mapped_column(Integer, ForeignKey("ubicacion_departamentos.departamento_id"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    fecha_actualizacion: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)

    departamento: Mapped["UbicacionDepartamento"] = relationship(back_populates="municipios")


# ---------------------------------------------------------------------------
# Usuarios
# ---------------------------------------------------------------------------

class Usuario(db.Model):
    __tablename__ = "usuarios"

    usuario_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    identificacion: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    tipo_documento: Mapped[str] = mapped_column(
        SAEnum("CC", "TI", "CE", "PEP", "PPT", name="tipo_doc_enum"), nullable=False
    )
    correo: Mapped[str] = mapped_column(String(254), nullable=False, unique=True)
    contrasena_hash: Mapped[str] = mapped_column(Text, nullable=False)
    rol_id: Mapped[int] = mapped_column(SmallInteger, ForeignKey("roles.rol_id"), nullable=False, default=4)
    cuenta_activa: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=None)
    correo_verificado: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    contrasena_cambio_pendiente: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    primer_nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    segundo_nombre: Mapped[str | None] = mapped_column(String(100), nullable=True)
    primer_apellido: Mapped[str] = mapped_column(String(100), nullable=False)
    segundo_apellido: Mapped[str | None] = mapped_column(String(100), nullable=True)
    creado_por: Mapped[str | None] = mapped_column(String(36), ForeignKey("usuarios.usuario_id"), nullable=True)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    fecha_actualizacion: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)

    rol_obj: Mapped["Rol"] = relationship("Rol", back_populates="usuarios")
    instructor: Mapped["Instructor | None"] = relationship("Instructor", back_populates="usuario", uselist=False)
    aprendiz: Mapped["Aprendiz | None"] = relationship("Aprendiz", back_populates="usuario", uselist=False)

    @property
    def nombre_completo(self):
        partes = [self.primer_nombre]
        if self.segundo_nombre:
            partes.append(self.segundo_nombre)
        partes.append(self.primer_apellido)
        if self.segundo_apellido:
            partes.append(self.segundo_apellido)
        return " ".join(partes)

    def to_dict(self):
        return {
            "usuario_id": self.usuario_id,
            "nombre_completo": self.nombre_completo,
            "correo": self.correo,
            "rol": self.rol_obj.nombre if self.rol_obj else None,
            "cuenta_activa": self.cuenta_activa,
        }

    def __repr__(self):
        return f"<Usuario {self.nombre_completo}>"


# ---------------------------------------------------------------------------
# Estructura SENA
# ---------------------------------------------------------------------------

class Regional(db.Model):
    __tablename__ = "regionales"

    regional_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    abreviatura: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    fecha_actualizacion: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)

    centros: Mapped[list["Centro"]] = relationship("Centro", back_populates="regional")

    def __repr__(self):
        return f"<Regional {self.nombre}>"


class Centro(db.Model):
    __tablename__ = "centros"

    centro_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    regional_id: Mapped[str] = mapped_column(String(36), ForeignKey("regionales.regional_id"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    fecha_actualizacion: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)

    __table_args__ = (UniqueConstraint("regional_id", "nombre", name="uq_centros__reg_nombre"),)

    regional: Mapped["Regional"] = relationship("Regional", back_populates="centros")
    sedes: Mapped[list["Sede"]] = relationship("Sede", back_populates="centro")
    coordinaciones: Mapped[list["Coordinacion"]] = relationship("Coordinacion", back_populates="centro")
    programas: Mapped[list["ProgramaFormacion"]] = relationship("ProgramaFormacion", back_populates="centro")

    def __repr__(self):
        return f"<Centro {self.nombre}>"


class Sede(db.Model):
    __tablename__ = "sedes"

    sede_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    centro_id: Mapped[str] = mapped_column(String(36), ForeignKey("centros.centro_id"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    barrio: Mapped[str | None] = mapped_column(String(255), nullable=True)
    direccion: Mapped[str] = mapped_column(String(255), nullable=False)
    codigo_postal: Mapped[str | None] = mapped_column(String(20), nullable=True)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    fecha_actualizacion: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)

    __table_args__ = (UniqueConstraint("centro_id", "nombre", name="uq_sedes__centro_nombre"),)

    centro: Mapped["Centro"] = relationship("Centro", back_populates="sedes")
    ambientes: Mapped[list["Ambiente"]] = relationship("Ambiente", back_populates="sede")

    def __repr__(self):
        return f"<Sede {self.nombre}>"


class Ambiente(db.Model):
    __tablename__ = "ambientes"

    ambiente_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    sede_id: Mapped[str] = mapped_column(String(36), ForeignKey("sedes.sede_id"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    fecha_actualizacion: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)

    __table_args__ = (UniqueConstraint("sede_id", "nombre", name="uq_ambientes__sede_nombre"),)

    sede: Mapped["Sede"] = relationship("Sede", back_populates="ambientes")
    fichas: Mapped[list["Ficha"]] = relationship("Ficha", back_populates="ambiente")

    def __repr__(self):
        return f"<Ambiente {self.nombre}>"


class Coordinacion(db.Model):
    __tablename__ = "coordinaciones"

    coordinacion_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    centro_id: Mapped[str] = mapped_column(String(36), ForeignKey("centros.centro_id"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    fecha_actualizacion: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)

    __table_args__ = (UniqueConstraint("centro_id", "nombre", name="uq_coord__centro_nombre"),)

    centro: Mapped["Centro"] = relationship("Centro", back_populates="coordinaciones")
    instructores: Mapped[list["Instructor"]] = relationship("Instructor", back_populates="coordinacion")
    fichas: Mapped[list["Ficha"]] = relationship("Ficha", back_populates="coordinacion")

    def __repr__(self):
        return f"<Coordinacion {self.nombre}>"


# ---------------------------------------------------------------------------
# Formación
# ---------------------------------------------------------------------------

class Modalidad(db.Model):
    __tablename__ = "modalidades"

    modalidad_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    fecha_actualizacion: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)

    programas: Mapped[list["ProgramaFormacion"]] = relationship("ProgramaFormacion", back_populates="modalidad")

    def __repr__(self):
        return f"<Modalidad {self.nombre}>"


class Nivel(db.Model):
    __tablename__ = "niveles"

    nivel_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    fecha_actualizacion: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)

    programas: Mapped[list["ProgramaFormacion"]] = relationship("ProgramaFormacion", back_populates="nivel")

    def __repr__(self):
        return f"<Nivel {self.nombre}>"


class ProgramaFormacion(db.Model):
    __tablename__ = "programas_formacion"

    programa_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    centro_id: Mapped[str] = mapped_column(String(36), ForeignKey("centros.centro_id"), nullable=False)
    nivel_id: Mapped[str] = mapped_column(String(36), ForeignKey("niveles.nivel_id"), nullable=False)
    modalidad_id: Mapped[str] = mapped_column(String(36), ForeignKey("modalidades.modalidad_id"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    codigo: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    fecha_actualizacion: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)

    centro: Mapped["Centro"] = relationship("Centro", back_populates="programas")
    nivel: Mapped["Nivel"] = relationship("Nivel", back_populates="programas")
    modalidad: Mapped["Modalidad"] = relationship("Modalidad", back_populates="programas")
    fichas: Mapped[list["Ficha"]] = relationship("Ficha", back_populates="programa")

    def __repr__(self):
        return f"<ProgramaFormacion {self.nombre} ({self.codigo})>"


# ---------------------------------------------------------------------------
# Personal
# ---------------------------------------------------------------------------

class Instructor(db.Model):
    __tablename__ = "instructores"

    instructor_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    usuario_id: Mapped[str] = mapped_column(String(36), ForeignKey("usuarios.usuario_id"), nullable=False)
    coordinacion_id: Mapped[str] = mapped_column(String(36), ForeignKey("coordinaciones.coordinacion_id"), nullable=False)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    fecha_actualizacion: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)

    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="instructor")
    coordinacion: Mapped["Coordinacion"] = relationship("Coordinacion", back_populates="instructores")
    fichas_lider: Mapped[list["Ficha"]] = relationship("Ficha", back_populates="instructor_lider", foreign_keys="Ficha.instructor_lider_id")
    fichas_asignadas: Mapped[list["FichaInstructor"]] = relationship("FichaInstructor", back_populates="instructor")

    @property
    def nombre_completo(self):
        return self.usuario.nombre_completo if self.usuario else ""

    def __repr__(self):
        return f"<Instructor {self.nombre_completo}>"


# ---------------------------------------------------------------------------
# Académico
# ---------------------------------------------------------------------------

class Transversal(db.Model):
    __tablename__ = "transversales"

    transversal_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    fecha_actualizacion: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)

    fichas: Mapped[list["FichaTransversal"]] = relationship("FichaTransversal", back_populates="transversal")
    instructores: Mapped[list["TransversalInstructor"]] = relationship("TransversalInstructor", back_populates="transversal")

    def __repr__(self):
        return f"<Transversal {self.nombre}>"


class Ficha(db.Model):
    __tablename__ = "fichas"

    ficha_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    programa_id: Mapped[str] = mapped_column(String(36), ForeignKey("programas_formacion.programa_id"), nullable=False)
    coordinacion_id: Mapped[str] = mapped_column(String(36), ForeignKey("coordinaciones.coordinacion_id"), nullable=False)
    ambiente_id: Mapped[str] = mapped_column(String(36), ForeignKey("ambientes.ambiente_id"), nullable=False)
    instructor_lider_id: Mapped[str] = mapped_column(String(36), ForeignKey("instructores.instructor_id"), nullable=False)
    fecha_inicio: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    fecha_etapa_productiva: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    fecha_fin: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    codigo: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    fecha_actualizacion: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)

    programa: Mapped["ProgramaFormacion"] = relationship("ProgramaFormacion", back_populates="fichas")
    coordinacion: Mapped["Coordinacion"] = relationship("Coordinacion", back_populates="fichas")
    ambiente: Mapped["Ambiente"] = relationship("Ambiente", back_populates="fichas")
    instructor_lider: Mapped["Instructor"] = relationship("Instructor", back_populates="fichas_lider", foreign_keys=[instructor_lider_id])
    aprendices: Mapped[list["Aprendiz"]] = relationship("Aprendiz", back_populates="ficha")
    transversales: Mapped[list["FichaTransversal"]] = relationship("FichaTransversal", back_populates="ficha")
    instructores_asignados: Mapped[list["FichaInstructor"]] = relationship("FichaInstructor", back_populates="ficha")
    proyecto_formativo: Mapped["ProyectoFormativo | None"] = relationship("ProyectoFormativo", back_populates="ficha", uselist=False)

    def __repr__(self):
        return f"<Ficha {self.codigo}>"


class Aprendiz(db.Model):
    __tablename__ = "aprendices"

    aprendiz_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    usuario_id: Mapped[str] = mapped_column(String(36), ForeignKey("usuarios.usuario_id"), nullable=False)
    ficha_id: Mapped[str] = mapped_column(String(36), ForeignKey("fichas.ficha_id"), nullable=False)
    estado: Mapped[str] = mapped_column(
        SAEnum("Activo", "Inactivo", "Suspendido", "Retirado", name="estado_aprendiz_enum"),
        nullable=False, default="Activo"
    )
    fecha_ingreso: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    fecha_retiro: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    fecha_actualizacion: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)

    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="aprendiz")
    ficha: Mapped["Ficha"] = relationship("Ficha", back_populates="aprendices")

    @property
    def nombre_completo(self):
        return self.usuario.nombre_completo if self.usuario else ""

    def __repr__(self):
        return f"<Aprendiz {self.nombre_completo}>"


class FichaTransversal(db.Model):
    __tablename__ = "ficha_transversal"
    __table_args__ = (UniqueConstraint("ficha_id", "transversal_id", name="uq_ficha_transversal"),)

    ficha_transversal_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    ficha_id: Mapped[str] = mapped_column(String(36), ForeignKey("fichas.ficha_id"), nullable=False)
    transversal_id: Mapped[str] = mapped_column(String(36), ForeignKey("transversales.transversal_id"), nullable=False)

    ficha: Mapped["Ficha"] = relationship("Ficha", back_populates="transversales")
    transversal: Mapped["Transversal"] = relationship("Transversal", back_populates="fichas")


class HistorialFicha(db.Model):
    __tablename__ = "historial_fichas"

    historial_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    aprendiz_id: Mapped[str] = mapped_column(String(36), ForeignKey("aprendices.aprendiz_id"), nullable=False)
    ficha_origen: Mapped[str] = mapped_column(String(36), ForeignKey("fichas.ficha_id"), nullable=False)
    ficha_destino: Mapped[str] = mapped_column(String(36), ForeignKey("fichas.ficha_id"), nullable=False)
    fecha_cambio: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)


class TransversalInstructor(db.Model):
    __tablename__ = "transversal_instructor"

    transversal_instructor_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    transversal_id: Mapped[str] = mapped_column(String(36), ForeignKey("transversales.transversal_id"), nullable=False)
    instructor_id: Mapped[str] = mapped_column(String(36), ForeignKey("instructores.instructor_id"), nullable=False)
    fecha_asignacion: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    fecha_fin: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)

    transversal: Mapped["Transversal"] = relationship("Transversal", back_populates="instructores")


class FichaInstructor(db.Model):
    __tablename__ = "ficha_instructor"
    __table_args__ = (UniqueConstraint("ficha_id", "instructor_id", name="uq_ficha_instructor"),)

    ficha_instructor_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    ficha_id: Mapped[str] = mapped_column(String(36), ForeignKey("fichas.ficha_id"), nullable=False)
    instructor_id: Mapped[str] = mapped_column(String(36), ForeignKey("instructores.instructor_id"), nullable=False)
    fecha_asignacion: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())

    ficha: Mapped["Ficha"] = relationship("Ficha", back_populates="instructores_asignados")
    instructor: Mapped["Instructor"] = relationship("Instructor", back_populates="fichas_asignadas")


# ---------------------------------------------------------------------------
# Proyectos Formativos
# ---------------------------------------------------------------------------

class ProyectoFormativo(db.Model):
    __tablename__ = "proyectos_formativos"

    proyecto_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    ficha_id: Mapped[str] = mapped_column(String(36), ForeignKey("fichas.ficha_id"), nullable=False, unique=True)
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    fecha_actualizacion: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)

    ficha: Mapped["Ficha"] = relationship("Ficha", back_populates="proyecto_formativo")
    fases: Mapped[list["Fase"]] = relationship("Fase", back_populates="proyecto", order_by="Fase.orden")

    def __repr__(self):
        return f"<ProyectoFormativo {self.titulo}>"


class Fase(db.Model):
    __tablename__ = "fases"

    fase_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    proyecto_id: Mapped[str] = mapped_column(String(36), ForeignKey("proyectos_formativos.proyecto_id"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    orden: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    fecha_actualizacion: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)

    proyecto: Mapped["ProyectoFormativo"] = relationship("ProyectoFormativo", back_populates="fases")
    actividades_proyecto: Mapped[list["ActividadProyecto"]] = relationship("ActividadProyecto", back_populates="fase", order_by="ActividadProyecto.orden")

    def __repr__(self):
        return f"<Fase {self.nombre}>"


class ActividadProyecto(db.Model):
    __tablename__ = "actividades_proyecto"

    actividad_proyecto_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    fase_id: Mapped[str] = mapped_column(String(36), ForeignKey("fases.fase_id"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    orden: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    fecha_actualizacion: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)

    fase: Mapped["Fase"] = relationship("Fase", back_populates="actividades_proyecto")
    actividades_aprendizaje: Mapped[list["ActividadAprendizaje"]] = relationship("ActividadAprendizaje", back_populates="actividad_proyecto", order_by="ActividadAprendizaje.orden")

    def __repr__(self):
        return f"<ActividadProyecto {self.nombre}>"


class ActividadAprendizaje(db.Model):
    __tablename__ = "actividades_aprendizaje"

    actividad_aprendizaje_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    actividad_proyecto_id: Mapped[str] = mapped_column(String(36), ForeignKey("actividades_proyecto.actividad_proyecto_id"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    orden: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    fecha_actualizacion: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)

    actividad_proyecto: Mapped["ActividadProyecto"] = relationship("ActividadProyecto", back_populates="actividades_aprendizaje")

    def __repr__(self):
        return f"<ActividadAprendizaje {self.nombre}>"
