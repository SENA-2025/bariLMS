# BARÍ LMS — Sistema de Gestión de Formación SENA

> Plataforma web para la gestión de la formación por proyectos del Servicio Nacional de Aprendizaje (SENA), desarrollada como proyecto integrador del programa de Análisis y Desarrollo de Software.

---

## Índice

- [Descripción](#descripción)
- [Tecnologías](#tecnologías)
- [Requisitos previos](#requisitos-previos)
- [Instalación y configuración](#instalación-y-configuración)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Roles y accesos](#roles-y-accesos)
- [Módulos implementados](#módulos-implementados)
- [Base de datos](#base-de-datos)
- [Rutas disponibles](#rutas-disponibles)
- [Equipo de desarrollo](#equipo-de-desarrollo)

---

## Descripción

**BARÍ LMS** es un sistema de gestión de aprendizaje (LMS) institucional diseñado para digitalizar y organizar el proceso formativo por proyectos del SENA. Permite a aprendices, instructores y administradores interactuar con las fichas de formación, fases del proyecto, actividades de aprendizaje, entregas de evidencias y calificaciones desde una única plataforma.

---

## Tecnologías

| Capa | Tecnología |
|---|---|
| Backend | Python 3.x + Flask |
| Base de datos | MariaDB 10.11 (vía DBngin) |
| ORM / Queries | SQL puro con `mysql-connector-python` |
| Seguridad | `werkzeug.security` — hashing bcrypt/scrypt |
| Frontend | Bootstrap 4 (SB Admin 2) + Jinja2 |
| Íconos | Font Awesome 5 |
| Tipografía | Google Fonts — Nunito |

---

## Requisitos previos

- Python 3.10 o superior
- MariaDB o MySQL corriendo localmente (XAMPP, DBngin, etc.)
- pip

---

## Instalación y configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/SENA-2025/bariLMS.git
cd bariLMS
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar la base de datos

Abre `app.py` y ajusta el bloque `db_config` con tus credenciales locales:

```python
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',        # Tu contraseña de MariaDB/MySQL
    'database': 'senalearn',
    'port': 5435           # Puerto de tu instancia (DBngin usa 5435)
}
```

### 4. Crear las tablas

Ejecuta el schema base en tu gestor de BD (TablePlus, phpMyAdmin, etc.):

```
SENALearn.sql
```

Luego ejecuta el script de tablas para la vista del aprendiz:

```
setup_aprendiz.sql
```

### 5. Crear un usuario de prueba

Genera el hash de la contraseña desde la terminal:

```bash
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('tu_password'))"
```

Inserta el usuario en la tabla `usuarios`:

```sql
INSERT INTO usuarios (email, nombre, rol, password_hash, activo)
VALUES ('aprendiz@sena.edu.co', 'Tu Nombre', 'Aprendiz', 'HASH_GENERADO', 1);
```

### 6. Iniciar la aplicación

```bash
python app.py
```

Accede en el navegador: `http://127.0.0.1:5000`

---

## Estructura del proyecto

```
bariLMS/
├── app.py                          ← Backend completo (rutas, queries, lógica)
├── requirements.txt                ← Dependencias Python
├── SENALearn.sql                   ← Schema base de la BD
├── setup_aprendiz.sql              ← Tablas para módulos del aprendiz
├── ARQUITECTURA.md                 ← Documentación técnica de arquitectura
│
├── templates/
│   ├── login.html                  ← Pantalla de inicio de sesión
│   ├── dashboard.html              ← Dashboard base (admin/instructor)
│   ├── 404.html                    ← Página de error personalizada
│   ├── admin_users.html
│   ├── admin_academic.html
│   ├── admin_structure.html
│   │
│   ├── aprendiz/
│   │   ├── base.html               ← Layout base del aprendiz (sidebar + topbar)
│   │   ├── dashboard.html          ← Panel principal del aprendiz
│   │   ├── fichas.html             ← Lista de fichas con buscador
│   │   ├── ficha_detalle.html      ← Detalle, progreso y entrega de evidencias
│   │   ├── fases.html              ← Fases de formación SENA
│   │   ├── calificaciones.html     ← Historial de notas
│   │   └── cambiar_contrasena.html ← Actualización de credenciales
│   │
│   └── instructor/
│       ├── fichas.html
│       ├── fases.html
│       └── change_password.html
│
└── static/
    ├── css/
    │   ├── sb-admin-2.min.css
    │   ├── sena-learn.css          ← Estilos personalizados SENA
    │   ├── aprendiz-fases.css
    │   └── fase.css
    ├── js/
    │   ├── sb-admin-2.min.js
    │   └── aprendiz-fases.js
    ├── img/
    │   └── logo-sena-blanco.png
    └── vendor/
        ├── bootstrap/
        ├── jquery/
        ├── jquery-easing/
        └── fontawesome-free/
```

---

## Roles y accesos

| Rol | Acceso | Slug |
|---|---|---|
| **Administrador** | Gestión de usuarios, estructura institucional y académica | `admin` |
| **Instructor** | Fichas, fases, actividades y calificación de aprendices | `instructor` |
| **Aprendiz** | Dashboard, fichas, fases, evidencias y calificaciones | `aprendiz` |

### Credencial de prueba (aprendiz)

| Campo | Valor |
|---|---|
| Correo | `aprendiz@sena.edu.co` |
| Contraseña | `sena2026` |
| Perfil | Aprendiz |

---

## Módulos implementados

### Vista Aprendiz

| Módulo | Ruta | Descripción |
|---|---|---|
| Dashboard | `/dashboard/aprendiz` | Panel con ficha, programa y accesos rápidos |
| Mis Fichas | `/aprendiz/fichas` | Lista de fichas con búsqueda en tiempo real |
| Detalle de Ficha | `/aprendiz/ficha/<id>` | Fases, actividades y barra de progreso |
| Entrega de Evidencias | `POST /aprendiz/entregar-evidencia` | Envío de URL de PDF por actividad |
| Fases de Formación | `/aprendiz/fases` | Estructura de fases: Análisis, Planeación, Ejecución |
| Calificaciones | `/aprendiz/calificaciones` | Historial de notas con resumen estadístico |
| Cambiar Contraseña | `/aprendiz/cambiar-contrasena` | Actualización segura de credenciales |
| Notificaciones | Campana en topbar | Alertas sin leer con marcado por AJAX |

### Vista Instructor

| Módulo | Ruta | Descripción |
|---|---|---|
| Fichas | `/instructor/fichas` | Fichas asignadas al instructor |
| Fases y Actividades | `/instructor/ficha/<id>/fases` | Árbol dinámico de fases y actividades |
| Calificación | Modal en fases | Calificación 0–100, aprueba con ≥ 75 |
| Cambiar Contraseña | `/instructor/change-password` | Actualización de credenciales |

### Vista Administrador

| Módulo | Descripción |
|---|---|
| Gestión de usuarios | CRUD completo de usuarios por rol |
| Estructura institucional | Regionales, centros, coordinaciones, sedes, ambientes |
| Estructura académica | Programas, fichas, proyectos, fases y actividades |

---

## Base de datos

### Diagrama simplificado

```
usuarios
  └── aprendices ──→ fichas ──→ programas_formacion ──→ niveles
                              └── actividades_proyecto ──→ fases
                                    └── actividades_aprendizaje
                                          └── entrega_evidencia (aprendiz + calificación)

usuarios ──→ notificaciones
```

### Tablas principales

| Tabla | Descripción |
|---|---|
| `usuarios` | Autenticación y roles |
| `aprendices` | Datos del aprendiz vinculados a un usuario |
| `fichas` | Fichas de formación |
| `programas_formacion` | Programas académicos |
| `fases` | Fases del proceso formativo (Análisis, Planeación, Ejecución) |
| `actividades_proyecto` | Actividades agrupadas por fase y ficha |
| `actividades_aprendizaje` | Sub-actividades con guía adjunta |
| `entrega_evidencia` | URL de evidencia + calificación del instructor |
| `notificaciones` | Alertas para el aprendiz |

---

## Rutas disponibles

### Autenticación

| Método | Ruta | Descripción |
|---|---|---|
| GET/POST | `/login` | Inicio de sesión |
| GET/POST | `/logout` | Cierre de sesión |

### Aprendiz

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/dashboard/aprendiz` | Panel principal |
| GET | `/aprendiz/fichas` | Lista de fichas |
| GET | `/aprendiz/ficha/<id>` | Detalle de ficha |
| GET | `/aprendiz/fases` | Fases de formación |
| GET | `/aprendiz/calificaciones` | Historial de calificaciones |
| GET/POST | `/aprendiz/cambiar-contrasena` | Cambio de contraseña |
| POST | `/aprendiz/entregar-evidencia` | Entregar evidencia (URL) |
| POST | `/aprendiz/notificaciones/marcar-leida/<id>` | Marcar notificación leída |

---

## Equipo de desarrollo

| Nombre | Rol en el proyecto | Rama |
|---|---|---|
| Santiago | Vista Aprendiz | `Santiago-Vista_Aprendiz` |
