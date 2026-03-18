# bariLMS — Mapeo de Arquitectura

> Generado el 2026-03-16

---

## Estructura de archivos

```
bariLMS/
├── app.py                          ← TODO el backend (~1956 líneas)
├── requirements.txt                ← Solo Flask >= 3.0
├── SENALearn.sql                   ← Schema SQL de referencia
├── ARQUITECTURA.md                 ← Este documento
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   ├── admin_users.html
│   ├── admin_structure.html
│   ├── admin_academic.html
│   └── instructor_change_password.html
└── static/
    ├── css/
    │   ├── sb-admin-2.min.css
    │   └── sena-learn.css
    ├── js/
    │   └── sb-admin-2.min.js
    ├── img/
    │   ├── logo-sena-blanco.png
    │   └── (ilustraciones undraw)
    └── vendor/
        └── bootstrap/
```

---

## Patrón arquitectónico

**Monolítico MVC-like** — sin blueprints, sin módulos separados. Todo el backend vive en `app.py`.

- **Model:** SQLite con SQL puro (`sqlite3`). Sin ORM.
- **View:** Jinja2 en `templates/`. Bootstrap 4 (SB Admin 2).
- **Controller:** Funciones de ruta en `app.py`.
- **Config:** Diccionarios `ENTITY_CONFIG`, `DASHBOARDS`, `ROLE_TO_SLUG` en `app.py`.

El HTML **no** está en `app.py`. Los estilos **no** están en `app.py`. El Python solo hace `render_template(...)`.

---

## Base de datos

**Motor:** SQLite — archivo `bari_lms.db` (generado al iniciar la app).
**Foreign keys:** habilitadas con `PRAGMA foreign_keys = ON`.
**Cascadas:** configuradas por tabla.

### Diagrama de tablas

```
Estructura institucional:
  regional
    └── centro
          ├── coordinacion
          │     ├── instructor ──→ usuario
          │     └── aprendiz
          └── sede
                └── ambiente

Estructura académica:
  red_conocimiento
    └── area
          └── programa_formacion ──→ nivel_formacion
                └── ficha_formacion ──→ coordinacion
                                    ──→ instructor
                                    ──→ proyecto_formativo
                                          └── fase_proyecto
                                                └── actividad_proyecto
                                                      └── actividad_aprendizaje
```

### Detalle de tablas

#### `usuario`
| Campo | Tipo | Notas |
|-------|------|-------|
| id | INTEGER PK | |
| correo | TEXT UNIQUE | |
| contrasena_hash | TEXT | Werkzeug |
| rol | TEXT | Administrador / Administrativo / Instructor / Aprendiz |
| nombre | TEXT | |
| activo | INTEGER | 0/1 |
| creado_en | TEXT | TIMESTAMP |

#### `regional`
| Campo | Tipo |
|-------|------|
| id | INTEGER PK |
| nombre | TEXT UNIQUE |

#### `centro`
| Campo | Tipo |
|-------|------|
| id | INTEGER PK |
| id_regional | FK → regional.id CASCADE |
| nombre | TEXT |

#### `coordinacion`
| Campo | Tipo |
|-------|------|
| id | INTEGER PK |
| id_centro | FK → centro.id CASCADE |
| nombre | TEXT |

#### `sede`
| Campo | Tipo |
|-------|------|
| id | INTEGER PK |
| id_centro | FK → centro.id CASCADE |
| nombre | TEXT |

#### `ambiente`
| Campo | Tipo |
|-------|------|
| id | INTEGER PK |
| id_sede | FK → sede.id CASCADE |
| nombre | TEXT |
| capacidad | INTEGER |

#### `instructor`
| Campo | Tipo |
|-------|------|
| id | INTEGER PK |
| id_coordinacion | FK → coordinacion.id CASCADE |
| id_area | FK → area.id |
| documento | TEXT |
| nombres | TEXT |
| apellidos | TEXT |
| correo | TEXT |
| id_usuario | FK → usuario.id |

#### `aprendiz`
| Campo | Tipo |
|-------|------|
| id | INTEGER PK |
| id_coordinacion | FK → coordinacion.id CASCADE |
| documento | TEXT |
| nombres | TEXT |
| apellidos | TEXT |
| ficha | TEXT |

#### `red_conocimiento`
| Campo | Tipo |
|-------|------|
| id | INTEGER PK |
| nombre | TEXT UNIQUE |

#### `area`
| Campo | Tipo |
|-------|------|
| id | INTEGER PK |
| id_red_conocimiento | FK → red_conocimiento.id CASCADE |
| nombre | TEXT |

#### `nivel_formacion`
| Campo | Tipo | Defaults |
|-------|------|---------|
| id | INTEGER PK | |
| nombre | TEXT UNIQUE | Técnico, Tecnólogo, Operario, Auxiliar, Curso |

#### `programa_formacion`
| Campo | Tipo |
|-------|------|
| id | INTEGER PK |
| id_area | FK → area.id CASCADE |
| id_nivel_formacion | FK → nivel_formacion.id CASCADE |
| nombre | TEXT |

#### `ficha_formacion`
| Campo | Tipo |
|-------|------|
| id | INTEGER PK |
| numero | TEXT UNIQUE |
| id_programa_formacion | FK → programa_formacion.id CASCADE |
| id_proyecto_formativo | FK → proyecto_formativo.id SET NULL |
| id_coordinacion | FK → coordinacion.id CASCADE |
| id_instructor | FK → instructor.id SET NULL |

#### `proyecto_formativo`
| Campo | Tipo |
|-------|------|
| id | INTEGER PK |
| codigo | TEXT UNIQUE |
| nombre | TEXT |

#### `fase_proyecto`
| Campo | Tipo |
|-------|------|
| id | INTEGER PK |
| id_proyecto_formativo | FK → proyecto_formativo.id CASCADE |
| nombre | TEXT |

#### `actividad_proyecto`
| Campo | Tipo |
|-------|------|
| id | INTEGER PK |
| id_fase_proyecto | FK → fase_proyecto.id CASCADE |
| nombre | TEXT |

#### `actividad_aprendizaje`
| Campo | Tipo |
|-------|------|
| id | INTEGER PK |
| id_actividad_proyecto | FK → actividad_proyecto.id CASCADE |
| nombre | TEXT |

---

## Rutas

### Autenticación

| Ruta | Método | Rol requerido | Función | Descripción |
|------|--------|---------------|---------|-------------|
| `/` | GET | — | `home()` | Redirige a dashboard o login |
| `/login` | GET, POST | — | `login()` | Autenticación por sesión |
| `/logout` | POST | — | `logout()` | Cierra sesión |

### Dashboard

| Ruta | Método | Rol requerido | Función |
|------|--------|---------------|---------|
| `/dashboard/<role_slug>` | GET | Autenticado | `dashboard(role_slug)` |

Slugs válidos: `administrador`, `administrativo`, `instructor`, `aprendiz`.

### Admin — Gestión de usuarios

| Ruta | Método | Función |
|------|--------|---------|
| `/admin/users` | GET | `admin_users()` |
| `/admin/users/create` | POST | `admin_users_create()` |
| `/admin/users/<id>/edit` | GET | `admin_users_edit(user_id)` |
| `/admin/users/<id>/update` | POST | `admin_users_update(user_id)` |
| `/admin/users/<id>/delete` | POST | `admin_users_delete(user_id)` |

Rol requerido: `Administrador`.

### Admin — Estructura institucional

| Ruta | Método | Función |
|------|--------|---------|
| `/admin/structure` | GET | `admin_structure()` |
| `/admin/structure/<entity>/create` | POST | `admin_structure_create(entity)` |
| `/admin/structure/<entity>/<id>/edit` | GET | `admin_structure_edit(entity, item_id)` |
| `/admin/structure/<entity>/<id>/update` | POST | `admin_structure_update(entity, item_id)` |
| `/admin/structure/<entity>/<id>/delete` | POST | `admin_structure_delete(entity, item_id)` |

Rol requerido: `Administrador`.

Entidades `<entity>` válidas:

| Valor | Entidad |
|-------|---------|
| `regional` | Regionales |
| `centro` | Centros de formación |
| `coordinacion` | Coordinaciones |
| `sede` | Sedes |
| `instructor` | Instructores |
| `aprendiz` | Aprendices |
| `ambiente` | Ambientes de formación |

### Admin — Estructura académica

| Ruta | Método | Función |
|------|--------|---------|
| `/admin/academic` | GET | `admin_academic()` |
| `/admin/academic/<entity>/create` | POST | `admin_academic_create(entity)` |
| `/admin/academic/<entity>/<id>/edit` | GET | `admin_academic_edit(entity, item_id)` |
| `/admin/academic/<entity>/<id>/update` | POST | `admin_academic_update(entity, item_id)` |
| `/admin/academic/<entity>/<id>/delete` | POST | `admin_academic_delete(entity, item_id)` |

Rol requerido: `Administrador`.

Entidades `<entity>` válidas:

| Valor | Entidad |
|-------|---------|
| `red` | Redes de conocimiento |
| `area` | Áreas de conocimiento |
| `nivel` | Niveles de formación |
| `programa` | Programas de formación |
| `ficha` | Fichas de formación |
| `proyecto_formativo` | Proyectos formativos |
| `fase_proyecto` | Fases de proyecto |
| `actividad_proyecto` | Actividades de proyecto |
| `actividad_aprendizaje` | Actividades de aprendizaje |

### Instructor

| Ruta | Método | Rol requerido | Función |
|------|--------|---------------|---------|
| `/instructor/password` | GET, POST | `Instructor` | `instructor_change_password()` |

---

## Middlewares y decoradores

```python
@login_required          # Verifica que haya sesión activa
@role_required("Rol")    # Verifica rol del usuario autenticado
@app.before_request      # Carga contexto antes de cada petición
@app.teardown_appcontext # Cierra conexión DB al finalizar
```

---

## Flujo de una petición

```
Cliente (browser)
    │
    ▼
Flask Router
    │
    ▼
@login_required / @role_required
    │  (falla → redirect /login)
    ▼
Función de ruta
    ├── get_db()
    ├── SQL query (get_entities / insert_entity / etc.)
    └── render_template("plantilla.html", datos=...)
              │
              ▼
        Jinja2 → HTML
              │
              ▼
        Cliente
```

---

## Helpers principales en app.py

### Base de datos
| Función | Descripción |
|---------|-------------|
| `get_db()` | Conexión SQLite con row factory |
| `close_db()` | Cierra la conexión |
| `initialize_database()` | Crea tablas y seedea datos por defecto |

### CRUD genérico
| Función | Descripción |
|---------|-------------|
| `get_entity(entity, item_id)` | Obtiene un registro por ID |
| `get_entities(entity, where, params, order_by)` | Consulta múltiples registros |
| `insert_entity(entity, data)` | Inserta un registro |
| `update_entity(entity, item_id, data)` | Actualiza un registro |
| `delete_entity(entity, item_id)` | Elimina un registro |

### Autenticación
| Función | Descripción |
|---------|-------------|
| `current_user()` | Usuario autenticado desde sesión |
| `get_user_by_email(email)` | Busca usuario por correo |
| `get_user_by_id(user_id)` | Busca usuario por ID |

### Sincronización instructor ↔ usuario
| Función | Descripción |
|---------|-------------|
| `create_linked_instructor_user(instructor_id, data)` | Crea usuario vinculado al instructor |
| `sync_instructor_user(instructor_id, data)` | Actualiza datos del usuario vinculado |
| `delete_linked_instructor_user(instructor_id)` | Elimina usuario vinculado |

### Validación y contexto
| Función | Descripción |
|---------|-------------|
| `validate_entity_payload(entity, data)` | Valida campos de estructura institucional |
| `validate_academic_payload(entity, data)` | Valida campos de estructura académica |
| `entity_form_data(entity, form)` | Extrae datos del formulario |
| `normalize_structure_context(args)` | Parsea estado de navegación institucional |
| `normalize_academic_context(args)` | Parsea estado de navegación académica |
| `structure_redirect_args(form_data, overrides)` | Construye parámetros de redirect |
| `academic_redirect_args(form_data, overrides)` | Construye parámetros de redirect |

---

## Diseño central: ENTITY_CONFIG

El corazón del CRUD genérico es el diccionario `ENTITY_CONFIG` en `app.py`. Define por cada entidad:
- Tabla SQL
- Campos y sus tipos
- Relaciones (claves foráneas)
- Cláusula SELECT personalizada

Las funciones genéricas (`get_entities`, `insert_entity`, etc.) leen este diccionario para operar sobre cualquier entidad sin duplicar código. Es un mini-ORM casero.

---

## Dependencias

### Backend
```
Flask >= 3.0, < 4.0
werkzeug       (incluido con Flask — hashing de contraseñas)
sqlite3        (stdlib Python)
os, functools  (stdlib Python)
```

### Frontend
```
Bootstrap 4 (SB Admin 2)
Font Awesome
Google Fonts
jQuery (incluido en SB Admin 2)
```

---

## Usuarios por defecto (seed)

| Correo | Contraseña | Rol |
|--------|------------|-----|
| admin@senalearn.edu.co | Admin123* | Administrador |
| administrativo@senalearn.edu.co | Adminvo123* | Administrativo |
| instructor@senalearn.edu.co | Instructor123* | Instructor |
| aprendiz@senalearn.edu.co | Aprendiz123* | Aprendiz |

---

## Configuración

| Variable | Valor por defecto | Descripción |
|----------|------------------|-------------|
| `SECRET_KEY` | `"bari-lms-dev-key"` | Secreto de sesión Flask |
| `DATABASE` | `"bari_lms.db"` | Ruta del archivo SQLite |

Se pueden sobreescribir con variables de entorno.
