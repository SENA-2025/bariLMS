-- ================================================================
--   BARI LMS — Schema Completo para MariaDB / phpMyAdmin
--   Base de datos: bari
--   Origen: PostgreSQL schema.sql + archivos MySQL individuales
--   Charset: utf8mb4
-- ================================================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;
SET SQL_MODE = 'NO_AUTO_VALUE_ON_ZERO';

-- ----------------------------------------------------------------
-- 0. LIMPIEZA PREVIA (permite re-ejecutar sin errores)
-- ----------------------------------------------------------------

DROP TABLE IF EXISTS aprendiz_transversal;
DROP TABLE IF EXISTS transversal_instructor;
DROP TABLE IF EXISTS historial_fichas;
DROP TABLE IF EXISTS ficha_transversal;
DROP TABLE IF EXISTS aprendices;
DROP TABLE IF EXISTS fichas;
DROP TABLE IF EXISTS transversales;
DROP TABLE IF EXISTS instructores;
DROP TABLE IF EXISTS programas_formacion;
DROP TABLE IF EXISTS niveles;
DROP TABLE IF EXISTS modalidades;
DROP TABLE IF EXISTS coordinaciones;
DROP TABLE IF EXISTS ambientes;
DROP TABLE IF EXISTS sedes;
DROP TABLE IF EXISTS centros;
DROP TABLE IF EXISTS regionales;
DROP TABLE IF EXISTS usuario_informacion_social;
DROP TABLE IF EXISTS usuario_informacion_basica;
DROP TABLE IF EXISTS usuario_acudiente;
DROP TABLE IF EXISTS usuario_contacto;
DROP TABLE IF EXISTS usuario_residencia;
DROP TABLE IF EXISTS usuario_documento;
DROP TABLE IF EXISTS usuario_avatar;
DROP TABLE IF EXISTS sesiones_logs;
DROP TABLE IF EXISTS sesiones;
DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS ubicacion_municipios;
DROP TABLE IF EXISTS ubicacion_departamentos;
DROP TABLE IF EXISTS ubicacion_paises;
DROP TABLE IF EXISTS catalogo_libreta_militar;
DROP TABLE IF EXISTS catalogo_eps;
DROP TABLE IF EXISTS catalogo_estado_civil;
DROP TABLE IF EXISTS catalogo_generos;
DROP TABLE IF EXISTS catalogo_parentescos;
DROP TABLE IF EXISTS roles;

SET FOREIGN_KEY_CHECKS = 1;

-- ----------------------------------------------------------------
-- 1. Catálogos
-- ----------------------------------------------------------------

CREATE TABLE catalogo_parentescos (
    parentesco_id   SMALLINT        NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre          VARCHAR(100)    NOT NULL UNIQUE,
    fecha_creacion  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP   NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE catalogo_generos (
    genero_id       SMALLINT        NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre          VARCHAR(100)    NOT NULL UNIQUE,
    fecha_creacion  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP   NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE catalogo_estado_civil (
    estado_civil_id SMALLINT        NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre          VARCHAR(100)    NOT NULL UNIQUE,
    fecha_creacion  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP   NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE catalogo_eps (
    eps_id          SMALLINT        NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre          VARCHAR(150)    NOT NULL UNIQUE,
    fecha_creacion  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP   NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE catalogo_libreta_militar (
    libreta_militar_id SMALLINT     NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre          VARCHAR(100)    NOT NULL UNIQUE,
    fecha_creacion  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP   NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ----------------------------------------------------------------
-- 2. Roles del sistema
-- ----------------------------------------------------------------

CREATE TABLE roles (
    rol_id          TINYINT         NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre          VARCHAR(50)     NOT NULL UNIQUE,
    descripcion     VARCHAR(255)    NULL,
    fecha_creacion  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP   NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO roles (nombre, descripcion) VALUES
    ('Administrador', 'Control total del sistema'),
    ('Administrativo', 'Gestión de fichas, programas y ambientes'),
    ('Instructor', 'Gestión de formación y aprendices'),
    ('Aprendiz', 'Consulta de su proceso formativo');


-- ----------------------------------------------------------------
-- 3. Ubicaciones
-- ----------------------------------------------------------------

CREATE TABLE ubicacion_paises (
    pais_id         SMALLINT        NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre          VARCHAR(100)    NOT NULL UNIQUE,
    fecha_creacion  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP   NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE ubicacion_departamentos (
    departamento_id INT             NOT NULL AUTO_INCREMENT PRIMARY KEY,
    pais_id         SMALLINT        NOT NULL,
    nombre          VARCHAR(100)    NOT NULL,
    fecha_creacion  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP   NULL DEFAULT NULL,
    UNIQUE KEY uq_dep__pais_nombre (pais_id, nombre),
    CONSTRAINT fk_dep__pais FOREIGN KEY (pais_id) REFERENCES ubicacion_paises(pais_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE ubicacion_municipios (
    municipio_id    INT             NOT NULL AUTO_INCREMENT PRIMARY KEY,
    departamento_id INT             NOT NULL,
    nombre          VARCHAR(100)    NOT NULL,
    fecha_creacion  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP   NULL DEFAULT NULL,
    UNIQUE KEY uq_mun__dep_nombre (departamento_id, nombre),
    CONSTRAINT fk_mun__dep FOREIGN KEY (departamento_id) REFERENCES ubicacion_departamentos(departamento_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ----------------------------------------------------------------
-- 4. Usuarios (tabla principal)
-- ----------------------------------------------------------------

CREATE TABLE usuarios (
    usuario_id      CHAR(36)        NOT NULL PRIMARY KEY,

    -- Identificación
    identificacion  VARCHAR(20)     NOT NULL UNIQUE,
    tipo_documento  ENUM('CC','TI','CE','PEP','PPT') NOT NULL,

    -- Autenticación
    correo          VARCHAR(254)    NOT NULL UNIQUE,
    contrasena_hash TEXT            NOT NULL,

    -- Rol
    rol_id          TINYINT         NOT NULL DEFAULT 4,

    -- Estado
    cuenta_activa   TINYINT(1)      NULL DEFAULT NULL COMMENT 'NULL=pendiente, 1=activa, 0=desactivada',
    correo_verificado TINYINT(1)    NOT NULL DEFAULT 0,
    contrasena_cambio_pendiente TINYINT(1) NOT NULL DEFAULT 0,

    -- Nombre básico
    primer_nombre   VARCHAR(100)    NOT NULL,
    segundo_nombre  VARCHAR(100)    NULL DEFAULT NULL,
    primer_apellido VARCHAR(100)    NOT NULL,
    segundo_apellido VARCHAR(100)   NULL DEFAULT NULL,

    -- Auditoría
    creado_por      CHAR(36)        NULL DEFAULT NULL,
    fecha_creacion  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP   NULL DEFAULT NULL,

    CONSTRAINT fk_usuarios__rol FOREIGN KEY (rol_id) REFERENCES roles(rol_id) ON DELETE RESTRICT,
    CONSTRAINT fk_usuarios__creado_por FOREIGN KEY (creado_por) REFERENCES usuarios(usuario_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_usuarios___ident_tipo ON usuarios(identificacion, tipo_documento);


-- ----------------------------------------------------------------
-- 5. Sesiones y logs
-- ----------------------------------------------------------------

CREATE TABLE sesiones (
    sesion_id           CHAR(36)    NOT NULL PRIMARY KEY,
    usuario_id          CHAR(36)    NOT NULL,
    token_actualizacion TEXT        NOT NULL UNIQUE,
    fecha_expiracion    TIMESTAMP   NOT NULL,
    direccion_ip        VARCHAR(45) NOT NULL,
    agente_usuario      TEXT        NOT NULL,
    fecha_creacion      TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_sesiones__usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_sesiones___exp ON sesiones(fecha_expiracion);
CREATE INDEX idx_sesiones___uid ON sesiones(usuario_id);

CREATE TABLE sesiones_logs (
    registro_id     CHAR(36)        NOT NULL PRIMARY KEY,
    sesion_id       CHAR(36)        NOT NULL,
    usuario_id      CHAR(36)        NOT NULL,
    origen_evento   ENUM('USUARIO','SISTEMA','ADMIN') NOT NULL,
    tipo_evento     ENUM('INICIO','CIERRE','EXPIRACION','INVALIDADA','SECUESTRO','TERMINADA','TERMINADAS_MASIVO','CIERRE_GLOBAL') NOT NULL,
    direccion_ip    VARCHAR(45)     NOT NULL,
    agente_usuario  TEXT            NOT NULL,
    fecha_creacion  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_slog__usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_slog___fecha ON sesiones_logs(fecha_creacion);
CREATE INDEX idx_slog___uid   ON sesiones_logs(usuario_id);


-- ----------------------------------------------------------------
-- 6. Detalle de usuario
-- ----------------------------------------------------------------

CREATE TABLE usuario_avatar (
    usuario_id      CHAR(36)        NOT NULL PRIMARY KEY,
    url             TEXT            NOT NULL,
    fecha_creacion  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP   NULL DEFAULT NULL,
    CONSTRAINT fk_avatar__usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE usuario_documento (
    usuario_id              CHAR(36)    NOT NULL PRIMARY KEY,
    pais_expedicion         SMALLINT    NOT NULL,
    departamento_expedicion INT         NULL DEFAULT NULL,
    municipio_expedicion    INT         NULL DEFAULT NULL,
    fecha_expedicion        DATE        NOT NULL,
    fecha_vencimiento       DATE        NULL DEFAULT NULL,
    fecha_creacion          TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion     TIMESTAMP   NULL DEFAULT NULL,
    CONSTRAINT fk_udoc__usuario  FOREIGN KEY (usuario_id)              REFERENCES usuarios(usuario_id) ON DELETE CASCADE,
    CONSTRAINT fk_udoc__pais     FOREIGN KEY (pais_expedicion)          REFERENCES ubicacion_paises(pais_id) ON DELETE RESTRICT,
    CONSTRAINT fk_udoc__dep      FOREIGN KEY (departamento_expedicion)  REFERENCES ubicacion_departamentos(departamento_id) ON DELETE RESTRICT,
    CONSTRAINT fk_udoc__mun      FOREIGN KEY (municipio_expedicion)     REFERENCES ubicacion_municipios(municipio_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE usuario_residencia (
    usuario_id      CHAR(36)        NOT NULL PRIMARY KEY,
    pais            SMALLINT        NOT NULL,
    departamento    INT             NULL DEFAULT NULL,
    municipio       INT             NULL DEFAULT NULL,
    barrio          VARCHAR(150)    NULL DEFAULT NULL,
    direccion       VARCHAR(255)    NOT NULL,
    codigo_postal   VARCHAR(20)     NULL DEFAULT NULL,
    fecha_creacion  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP   NULL DEFAULT NULL,
    CONSTRAINT fk_ures__usuario FOREIGN KEY (usuario_id)  REFERENCES usuarios(usuario_id) ON DELETE CASCADE,
    CONSTRAINT fk_ures__pais    FOREIGN KEY (pais)         REFERENCES ubicacion_paises(pais_id) ON DELETE RESTRICT,
    CONSTRAINT fk_ures__dep     FOREIGN KEY (departamento) REFERENCES ubicacion_departamentos(departamento_id) ON DELETE RESTRICT,
    CONSTRAINT fk_ures__mun     FOREIGN KEY (municipio)    REFERENCES ubicacion_municipios(municipio_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE usuario_contacto (
    usuario_id              CHAR(36)    NOT NULL PRIMARY KEY,
    correo                  VARCHAR(254) NOT NULL UNIQUE,
    prefijo_telefono_movil  SMALLINT    NOT NULL,
    telefono_movil          BIGINT      NOT NULL,
    prefijo_telefono        SMALLINT    NULL DEFAULT NULL,
    telefono                BIGINT      NULL DEFAULT NULL,
    fecha_creacion          TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion     TIMESTAMP   NULL DEFAULT NULL,
    CONSTRAINT fk_ucont__usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE usuario_acudiente (
    usuario_id              CHAR(36)    NOT NULL PRIMARY KEY,
    parentesco              SMALLINT    NOT NULL,
    primer_nombre           VARCHAR(100) NOT NULL,
    segundo_nombre          VARCHAR(100) NULL DEFAULT NULL,
    primer_apellido         VARCHAR(100) NOT NULL,
    segundo_apellido        VARCHAR(100) NULL DEFAULT NULL,
    fecha_nacimiento        DATE        NOT NULL,
    prefijo_telefono_movil  SMALLINT    NOT NULL,
    telefono_movil          BIGINT      NOT NULL,
    prefijo_telefono        SMALLINT    NULL DEFAULT NULL,
    telefono                BIGINT      NULL DEFAULT NULL,
    fecha_creacion          TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion     TIMESTAMP   NULL DEFAULT NULL,
    CONSTRAINT fk_uacu__usuario    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE,
    CONSTRAINT fk_uacu__parentesco FOREIGN KEY (parentesco) REFERENCES catalogo_parentescos(parentesco_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE usuario_informacion_basica (
    usuario_id              CHAR(36)    NOT NULL PRIMARY KEY,
    primer_nombre           VARCHAR(100) NOT NULL,
    segundo_nombre          VARCHAR(100) NULL DEFAULT NULL,
    primer_apellido         VARCHAR(100) NOT NULL,
    segundo_apellido        VARCHAR(100) NULL DEFAULT NULL,
    genero                  SMALLINT    NOT NULL,
    fecha_nacimiento        DATE        NOT NULL,
    pais_nacimiento         SMALLINT    NOT NULL,
    departamento_nacimiento INT         NULL DEFAULT NULL,
    municipio_nacimiento    INT         NULL DEFAULT NULL,
    libreta_militar         SMALLINT    NOT NULL,
    eps                     SMALLINT    NULL DEFAULT NULL,
    fecha_creacion          TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion     TIMESTAMP   NULL DEFAULT NULL,
    CONSTRAINT fk_uib__usuario  FOREIGN KEY (usuario_id)             REFERENCES usuarios(usuario_id) ON DELETE CASCADE,
    CONSTRAINT fk_uib__genero   FOREIGN KEY (genero)                  REFERENCES catalogo_generos(genero_id) ON DELETE RESTRICT,
    CONSTRAINT fk_uib__pais_nac FOREIGN KEY (pais_nacimiento)         REFERENCES ubicacion_paises(pais_id) ON DELETE RESTRICT,
    CONSTRAINT fk_uib__dep_nac  FOREIGN KEY (departamento_nacimiento) REFERENCES ubicacion_departamentos(departamento_id) ON DELETE RESTRICT,
    CONSTRAINT fk_uib__mun_nac  FOREIGN KEY (municipio_nacimiento)    REFERENCES ubicacion_municipios(municipio_id) ON DELETE RESTRICT,
    CONSTRAINT fk_uib__libreta  FOREIGN KEY (libreta_militar)         REFERENCES catalogo_libreta_militar(libreta_militar_id) ON DELETE RESTRICT,
    CONSTRAINT fk_uib__eps      FOREIGN KEY (eps)                     REFERENCES catalogo_eps(eps_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE usuario_informacion_social (
    usuario_id      CHAR(36)        NOT NULL PRIMARY KEY,
    estrato         TINYINT         NOT NULL,
    estado_civil    SMALLINT        NOT NULL,
    tipo_sangre     ENUM('A+','A-','B+','B-','O+','O-','AB+','AB-') NOT NULL,
    fecha_creacion  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP   NULL DEFAULT NULL,
    CONSTRAINT fk_uis__usuario     FOREIGN KEY (usuario_id)  REFERENCES usuarios(usuario_id) ON DELETE CASCADE,
    CONSTRAINT fk_uis__estado_civil FOREIGN KEY (estado_civil) REFERENCES catalogo_estado_civil(estado_civil_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ----------------------------------------------------------------
-- 7. Estructura SENA
-- ----------------------------------------------------------------

CREATE TABLE regionales (
    regional_id     CHAR(36)        NOT NULL PRIMARY KEY,
    nombre          VARCHAR(100)    NOT NULL UNIQUE,
    abreviatura     VARCHAR(10)     NOT NULL UNIQUE,
    fecha_creacion  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP   NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE centros (
    centro_id       CHAR(36)        NOT NULL PRIMARY KEY,
    regional_id     CHAR(36)        NOT NULL,
    nombre          VARCHAR(255)    NOT NULL,
    fecha_creacion  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP   NULL DEFAULT NULL,
    UNIQUE KEY uq_centros__reg_nombre (regional_id, nombre),
    CONSTRAINT fk_centros__regional FOREIGN KEY (regional_id) REFERENCES regionales(regional_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE sedes (
    sede_id         CHAR(36)        NOT NULL PRIMARY KEY,
    centro_id       CHAR(36)        NOT NULL,
    nombre          VARCHAR(255)    NOT NULL,
    barrio          VARCHAR(255)    NULL DEFAULT NULL,
    direccion       VARCHAR(255)    NOT NULL,
    codigo_postal   VARCHAR(20)     NULL DEFAULT NULL,
    fecha_creacion  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP   NULL DEFAULT NULL,
    UNIQUE KEY uq_sedes__centro_nombre (centro_id, nombre),
    CONSTRAINT fk_sedes__centro FOREIGN KEY (centro_id) REFERENCES centros(centro_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE ambientes (
    ambiente_id     CHAR(36)        NOT NULL PRIMARY KEY,
    sede_id         CHAR(36)        NOT NULL,
    nombre          VARCHAR(255)    NOT NULL,
    fecha_creacion  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP   NULL DEFAULT NULL,
    UNIQUE KEY uq_ambientes__sede_nombre (sede_id, nombre),
    CONSTRAINT fk_ambientes__sede FOREIGN KEY (sede_id) REFERENCES sedes(sede_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE coordinaciones (
    coordinacion_id CHAR(36)        NOT NULL PRIMARY KEY,
    centro_id       CHAR(36)        NOT NULL,
    nombre          VARCHAR(255)    NOT NULL,
    fecha_creacion  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP   NULL DEFAULT NULL,
    UNIQUE KEY uq_coord__centro_nombre (centro_id, nombre),
    CONSTRAINT fk_coord__centro FOREIGN KEY (centro_id) REFERENCES centros(centro_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ----------------------------------------------------------------
-- 8. Formación
-- ----------------------------------------------------------------

CREATE TABLE modalidades (
    modalidad_id    CHAR(36)        NOT NULL PRIMARY KEY,
    nombre          VARCHAR(255)    NOT NULL UNIQUE,
    fecha_creacion  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP   NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE niveles (
    nivel_id        CHAR(36)        NOT NULL PRIMARY KEY,
    nombre          VARCHAR(255)    NOT NULL UNIQUE,
    fecha_creacion  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP   NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE programas_formacion (
    programa_id     CHAR(36)        NOT NULL PRIMARY KEY,
    centro_id       CHAR(36)        NOT NULL,
    nivel_id        CHAR(36)        NOT NULL,
    modalidad_id    CHAR(36)        NOT NULL,
    nombre          VARCHAR(255)    NOT NULL,
    codigo          VARCHAR(100)    NOT NULL UNIQUE,
    fecha_creacion  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP   NULL DEFAULT NULL,
    UNIQUE KEY uq_prog__centro_nivel_nombre (centro_id, nivel_id, nombre),
    CONSTRAINT fk_prog__centro    FOREIGN KEY (centro_id)   REFERENCES centros(centro_id) ON DELETE RESTRICT,
    CONSTRAINT fk_prog__nivel     FOREIGN KEY (nivel_id)    REFERENCES niveles(nivel_id) ON DELETE RESTRICT,
    CONSTRAINT fk_prog__modalidad FOREIGN KEY (modalidad_id) REFERENCES modalidades(modalidad_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ----------------------------------------------------------------
-- 9. Personal
-- ----------------------------------------------------------------

CREATE TABLE instructores (
    instructor_id   CHAR(36)        NOT NULL PRIMARY KEY,
    usuario_id      CHAR(36)        NOT NULL,
    coordinacion_id CHAR(36)        NOT NULL,
    fecha_creacion  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP   NULL DEFAULT NULL,
    CONSTRAINT fk_instr__usuario      FOREIGN KEY (usuario_id)      REFERENCES usuarios(usuario_id) ON DELETE RESTRICT,
    CONSTRAINT fk_instr__coordinacion FOREIGN KEY (coordinacion_id) REFERENCES coordinaciones(coordinacion_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ----------------------------------------------------------------
-- 10. Académico
-- ----------------------------------------------------------------

CREATE TABLE transversales (
    transversal_id  CHAR(36)        NOT NULL PRIMARY KEY,
    nombre          VARCHAR(255)    NOT NULL,
    fecha_creacion  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP   NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE fichas (
    ficha_id                CHAR(36)    NOT NULL PRIMARY KEY,
    programa_id             CHAR(36)    NOT NULL,
    coordinacion_id         CHAR(36)    NOT NULL,
    ambiente_id             CHAR(36)    NOT NULL,
    instructor_lider_id     CHAR(36)    NOT NULL,
    fecha_inicio            TIMESTAMP   NOT NULL,
    fecha_etapa_productiva  TIMESTAMP   NOT NULL,
    fecha_fin               TIMESTAMP   NOT NULL,
    codigo                  BIGINT UNSIGNED NOT NULL UNIQUE,
    fecha_creacion          TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion     TIMESTAMP   NULL DEFAULT NULL,
    CONSTRAINT fk_fichas__programa         FOREIGN KEY (programa_id)         REFERENCES programas_formacion(programa_id) ON DELETE RESTRICT,
    CONSTRAINT fk_fichas__coordinacion     FOREIGN KEY (coordinacion_id)     REFERENCES coordinaciones(coordinacion_id) ON DELETE RESTRICT,
    CONSTRAINT fk_fichas__ambiente         FOREIGN KEY (ambiente_id)         REFERENCES ambientes(ambiente_id) ON DELETE RESTRICT,
    CONSTRAINT fk_fichas__instructor_lider FOREIGN KEY (instructor_lider_id) REFERENCES instructores(instructor_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE aprendices (
    aprendiz_id     CHAR(36)        NOT NULL PRIMARY KEY,
    usuario_id      CHAR(36)        NOT NULL,
    ficha_id        CHAR(36)        NOT NULL,
    estado          ENUM('Activo','Inactivo','Suspendido','Retirado') NOT NULL,
    fecha_ingreso   TIMESTAMP       NOT NULL,
    fecha_retiro    TIMESTAMP       NULL DEFAULT NULL,
    fecha_creacion  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP   NULL DEFAULT NULL,
    CONSTRAINT fk_apr__usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE RESTRICT,
    CONSTRAINT fk_apr__ficha   FOREIGN KEY (ficha_id)   REFERENCES fichas(ficha_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE ficha_transversal (
    ficha_transversal_id CHAR(36)   NOT NULL PRIMARY KEY,
    ficha_id        CHAR(36)        NOT NULL,
    transversal_id  CHAR(36)        NOT NULL,
    UNIQUE KEY uq_ficha_transversal (ficha_id, transversal_id),
    CONSTRAINT fk_ft__ficha       FOREIGN KEY (ficha_id)       REFERENCES fichas(ficha_id) ON DELETE CASCADE,
    CONSTRAINT fk_ft__transversal FOREIGN KEY (transversal_id) REFERENCES transversales(transversal_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE historial_fichas (
    historial_id    CHAR(36)        NOT NULL PRIMARY KEY,
    aprendiz_id     CHAR(36)        NOT NULL,
    ficha_origen    CHAR(36)        NOT NULL,
    ficha_destino   CHAR(36)        NOT NULL,
    fecha_cambio    TIMESTAMP       NOT NULL,
    CONSTRAINT fk_hf__aprendiz FOREIGN KEY (aprendiz_id) REFERENCES aprendices(aprendiz_id) ON DELETE RESTRICT,
    CONSTRAINT fk_hf__origen   FOREIGN KEY (ficha_origen)  REFERENCES fichas(ficha_id) ON DELETE RESTRICT,
    CONSTRAINT fk_hf__destino  FOREIGN KEY (ficha_destino) REFERENCES fichas(ficha_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE transversal_instructor (
    transversal_instructor_id CHAR(36) NOT NULL PRIMARY KEY,
    transversal_id  CHAR(36)        NOT NULL,
    instructor_id   CHAR(36)        NOT NULL,
    fecha_asignacion TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_fin       TIMESTAMP       NULL DEFAULT NULL,
    CONSTRAINT fk_ti__transversal FOREIGN KEY (transversal_id) REFERENCES transversales(transversal_id) ON DELETE CASCADE,
    CONSTRAINT fk_ti__instructor  FOREIGN KEY (instructor_id)  REFERENCES instructores(instructor_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE aprendiz_transversal (
    aprendiz_transversal_id CHAR(36) NOT NULL PRIMARY KEY,
    aprendiz_id     CHAR(36)        NOT NULL,
    transversal_id  CHAR(36)        NOT NULL,
    estado          ENUM('Activo','Inactivo','Suspendido','Retirado') NOT NULL,
    fecha_creacion  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP   NULL DEFAULT NULL,
    CONSTRAINT fk_at__aprendiz    FOREIGN KEY (aprendiz_id)   REFERENCES aprendices(aprendiz_id) ON DELETE RESTRICT,
    CONSTRAINT fk_at__transversal FOREIGN KEY (transversal_id) REFERENCES transversales(transversal_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ----------------------------------------------------------------
-- 11. Datos iniciales de catálogos
-- ----------------------------------------------------------------

INSERT INTO catalogo_parentescos (nombre) VALUES
    ('Padre'), ('Madre'), ('Abuelo/a'), ('Hermano/a'),
    ('Tío/a'), ('Tutor legal'), ('Otro');

INSERT INTO catalogo_generos (nombre) VALUES
    ('Masculino'), ('Femenino'), ('No binario'), ('Prefiero no decir');

INSERT INTO catalogo_estado_civil (nombre) VALUES
    ('Soltero/a'), ('Casado/a'), ('Unión libre'), ('Divorciado/a'),
    ('Viudo/a'), ('Separado/a');

INSERT INTO catalogo_libreta_militar (nombre) VALUES
    ('Primera clase'), ('Segunda clase'), ('No aplica');

INSERT INTO catalogo_eps (nombre) VALUES
    ('Sura'), ('Sanitas'), ('Compensar'), ('Famisanar'), ('Nueva EPS'),
    ('Salud Total'), ('Coomeva'), ('Aliansalud'), ('Medimás'), ('Otra');

INSERT INTO ubicacion_paises (nombre) VALUES ('Colombia');

-- ================================================================
--   FIN DEL SCRIPT
-- ================================================================
