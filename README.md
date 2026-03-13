# BARÍ LMS · Sistema de Gestión de Formación SENA

> Plataforma web para la gestión de fichas, instructores, aprendices y proyectos formativos del SENA.
> Desarrollada en **Python / Flask** con base de datos **MariaDB**.

---

## Requisitos previos

Antes de comenzar, asegúrate de tener instaladas las siguientes herramientas en tu computador:

| Herramienta | Versión mínima | Para qué sirve | Descarga |
|-------------|---------------|----------------|----------|
| **Python** | 3.11 o superior | Ejecutar la aplicación | [python.org](https://www.python.org/downloads/) |
| **XAMPP** | Cualquiera reciente | Provee MariaDB + phpMyAdmin | [apachefriends.org](https://www.apachefriends.org/es/index.html) |
| **Git** *(opcional)* | Cualquiera | Clonar el repositorio | [git-scm.com](https://git-scm.com/) |

> **Nota:** Si ya tienes otro servidor MariaDB o MySQL instalado (WAMP, Laragon, etc.), también funciona. Lo importante es tener acceso a **phpMyAdmin** o al cliente de base de datos.

---

## Paso 1 — Obtener el proyecto

Copia la carpeta del proyecto en tu computador. Debe quedar con esta estructura:

```
Bari Python/
├── bariLMS/              ← Aplicación Flask
│   ├── app.py
│   ├── run.py
│   ├── requirements.txt
│   ├── seed_demo.py      ← Script de datos de demostración
│   ├── .env
│   └── ...
└── database/
    └── bari_schema_setup.sql   ← Script de base de datos
```

---

## Paso 2 — Configurar la base de datos

### 2.1 Iniciar XAMPP

1. Abre el **Panel de Control de XAMPP**
2. Haz clic en **Start** para los módulos **Apache** y **MySQL**
3. Ambos deben quedar en verde

![XAMPP corriendo Apache y MySQL](https://i.imgur.com/placeholder.png)

### 2.2 Crear la base de datos

1. Abre tu navegador y ve a: **http://localhost/phpmyadmin**
2. En el panel izquierdo haz clic en **Nueva** (o **New**)
3. En el campo *Nombre de la base de datos* escribe exactamente:

   ```
   bari
   ```

4. En *Cotejamiento* selecciona: `utf8mb4_unicode_ci`
5. Haz clic en **Crear**

### 2.3 Importar el schema

1. Con la base de datos `bari` seleccionada en el panel izquierdo
2. Haz clic en la pestaña **Importar**
3. Haz clic en **Seleccionar archivo** y busca:

   ```
   database/bari_schema_setup.sql
   ```

4. Haz clic en **Importar** (botón al final de la página)
5. Deberías ver el mensaje: *"Se han ejecutado correctamente X consultas"*

> ✅ Si todo salió bien, en el panel izquierdo verás la base de datos `bari` con **40 tablas** creadas.

---

## Paso 3 — Configurar el entorno Python

Abre una terminal (símbolo del sistema o PowerShell) y navega hasta la carpeta de la aplicación:

```bash
cd "ruta\a\tu\carpeta\Bari Python\bariLMS"
```

### 3.1 Crear entorno virtual *(recomendado)*

```bash
python -m venv venv
```

Activar el entorno virtual:

```bash
# Windows (CMD)
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# macOS / Linux
source venv/bin/activate
```

Sabrás que está activo porque verás `(venv)` al inicio de la línea de la terminal.

### 3.2 Instalar dependencias

```bash
pip install -r requirements.txt
```

Esto instala automáticamente: Flask, SQLAlchemy, PyMySQL, openpyxl y demás librerías necesarias.

---

## Paso 4 — Verificar la configuración

Abre el archivo **`.env`** que está dentro de la carpeta `bariLMS` y comprueba que la conexión apunta a tu servidor local:

```env
DATABASE_URL=mysql+pymysql://root:@127.0.0.1:3306/bari
SECRET_KEY=bari-lms-dev-secret-key-2026
FLASK_ENV=development
FLASK_DEBUG=true
```

> **Si tu MariaDB tiene contraseña**, cambia la línea a:
> ```
> DATABASE_URL=mysql+pymysql://root:TU_CONTRASEÑA@127.0.0.1:3306/bari
> ```

---

## Paso 5 — Cargar datos de demostración *(opcional)*

Si quieres ver el sistema con datos de ejemplo para explorar todas las funcionalidades, ejecuta:

```bash
python seed_demo.py
```

Esto carga automáticamente:

- 4 Regionales y 4 Centros de Formación
- 5 Programas de Formación (ADSI, Sistemas, Gestión Administrativa, etc.)
- 5 Instructores
- 5 Fichas de formación
- 33 Aprendices distribuidos en las fichas
- Proyectos Formativos con Fases y Actividades
- Transversales asignadas

> ⚠️ Este paso borra cualquier dato previo y carga los datos de demo desde cero.

---

## Paso 6 — Ejecutar la aplicación

```bash
python run.py
```

Deberías ver algo así en la terminal:

```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

Abre tu navegador y ve a:

```
http://127.0.0.1:5000
```

---

## Acceso al sistema

### Usuarios de demostración

| Perfil | Correo | Contraseña |
|--------|--------|------------|
| **Administrador** | `admin@senalearn.edu.co` | `Admin123*` |
| **Administrativo** | `administrativo@senalearn.edu.co` | `Adminvo123*` |
| **Instructor** | `instructor@senalearn.edu.co` | `Instructor123*` |
| **Aprendiz** | `aprendiz@senalearn.edu.co` | `Aprendiz123*` |

> Recuerda seleccionar el perfil correcto en el desplegable del formulario de login.

---

## Solución de problemas frecuentes

### ❌ Error: `Can't connect to MySQL server`
- Verifica que **MySQL esté corriendo** en el Panel de XAMPP (debe estar en verde)
- Confirma que el puerto en `.env` es `3306`

### ❌ Error: `Access denied for user 'root'`
- Tu instalación de MariaDB tiene contraseña. Agrégala en el archivo `.env`:
  ```
  DATABASE_URL=mysql+pymysql://root:tu_contraseña@127.0.0.1:3306/bari
  ```

### ❌ Error al importar el SQL en phpMyAdmin
- Asegúrate de haber seleccionado la base de datos `bari` antes de importar
- Verifica que el cotejamiento sea `utf8mb4_unicode_ci`

### ❌ Error: `ModuleNotFoundError`
- Asegúrate de haber activado el entorno virtual y ejecutado `pip install -r requirements.txt`

### ❌ La página carga pero no muestra datos
- Ejecuta el script de datos: `python seed_demo.py`

---

## Estructura del proyecto

```
bariLMS/
├── app.py                    ← Fábrica de la aplicación Flask
├── run.py                    ← Punto de entrada para ejecutar
├── config.py                 ← Configuración por entorno
├── .env                      ← Variables de entorno (conexión DB, clave secreta)
├── requirements.txt          ← Dependencias Python
├── seed_demo.py              ← Datos de demostración
├── database_mariadb.sql      ← Schema completo de la base de datos
│
├── models/
│   └── models.py             ← Todos los modelos de datos (40 tablas)
│
├── routes/                   ← Rutas (controladores) por módulo
│   ├── auth_routes.py
│   ├── dashboard_routes.py
│   ├── sena_routes.py        ← Regionales, Centros, Sedes, Ambientes, Coordinaciones
│   ├── formacion_routes.py   ← Modalidades, Niveles, Programas
│   ├── instructores_routes.py
│   ├── fichas_routes.py      ← Fichas + Proyecto Formativo completo
│   └── aprendices_routes.py  ← Aprendices + Carga masiva Excel
│
├── services/                 ← Lógica de negocio por módulo
│   ├── auth_service.py
│   ├── sena_service.py
│   ├── formacion_service.py
│   ├── instructores_service.py
│   ├── fichas_service.py
│   └── aprendices_service.py
│
└── templates/                ← Vistas HTML (SB Admin 2 / Bootstrap 4)
    ├── base.html
    ├── login.html
    ├── dashboard.html
    ├── sena/
    ├── formacion/
    ├── instructores/
    ├── fichas/
    └── aprendices/
```

---

## Módulos del sistema

| Módulo | Funcionalidad |
|--------|--------------|
| **Estructura SENA** | Crear y gestionar Regionales, Centros, Sedes, Ambientes y Coordinaciones |
| **Formación** | Gestionar Modalidades, Niveles y Programas de Formación |
| **Instructores** | Registro y asignación de instructores a coordinaciones |
| **Fichas** | Creación de fichas, asignación de instructores, proyecto formativo completo (fases, actividades de proyecto, actividades de aprendizaje) |
| **Aprendices** | Gestión individual y **carga masiva desde Excel/CSV** |
| **Administración** | Gestión de usuarios y roles del sistema |

---

*BARÍ LMS · SENA Colombia · 2026*
