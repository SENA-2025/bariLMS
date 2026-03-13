"""
seed_demo.py
Datos de demostración para bariLMS – presentación a directivas SENA.
Ejecutar: python seed_demo.py
"""
import uuid
import datetime
import pymysql
from werkzeug.security import generate_password_hash

# ─── Conexión ────────────────────────────────────────────────────────────────
conn = pymysql.connect(
    host="127.0.0.1", port=3306, user="root", password="", database="bari",
    autocommit=False, charset="utf8mb4",
)
cur = conn.cursor()


def uid():
    return str(uuid.uuid4())


def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def fecha(year, month, day):
    return f"{year}-{month:02d}-{day:02d} 00:00:00"


print("🔄  Limpiando datos previos...")
# Limpiar en orden inverso de FK
for tabla in [
    "actividades_aprendizaje", "actividades_proyecto", "fases", "proyectos_formativos",
    "ficha_instructor", "aprendiz_transversal", "transversal_instructor", "ficha_transversal",
    "historial_fichas", "aprendices", "fichas", "transversales",
    "instructores", "programas_formacion", "coordinaciones", "ambientes",
    "sedes", "centros", "regionales", "modalidades", "niveles",
    "sesiones_logs", "sesiones", "usuarios",
]:
    cur.execute(f"DELETE FROM {tabla}")

conn.commit()
print("✅  Limpieza completada.\n")

# ─── REGIONALES ──────────────────────────────────────────────────────────────
print("📌  Insertando Regionales...")
R_DC  = uid(); R_ANT = uid(); R_VAL = uid(); R_SAL = uid()
regionales = [
    (R_DC,  "Regional Distrito Capital",   "DC"),
    (R_ANT, "Regional Antioquia",           "ANT"),
    (R_VAL, "Regional Valle del Cauca",    "VCA"),
    (R_SAL, "Regional Santander",          "SANT"),
]
cur.executemany(
    "INSERT INTO regionales (regional_id, nombre, abreviatura) VALUES (%s,%s,%s)",
    regionales,
)

# ─── CENTROS ─────────────────────────────────────────────────────────────────
print("🏢  Insertando Centros...")
C_CGMLT = uid(); C_CDM = uid(); C_CSF = uid(); C_CGA = uid()
centros = [
    (C_CGMLT, R_DC,  "Centro de Gestión de Mercados, Logística y TI"),
    (C_CDM,   R_DC,  "Centro de Diseño y Metrología"),
    (C_CSF,   R_DC,  "Centro de Servicios Financieros"),
    (C_CGA,   R_ANT, "Centro de Gestión Administrativa"),
]
cur.executemany(
    "INSERT INTO centros (centro_id, regional_id, nombre) VALUES (%s,%s,%s)",
    centros,
)

# ─── SEDES ───────────────────────────────────────────────────────────────────
print("📍  Insertando Sedes...")
S1 = uid(); S2 = uid(); S3 = uid()
sedes = [
    (S1, C_CGMLT, "Sede Principal Paloquemao", "Paloquemao",    "Carrera 23 No 18-22", "111611"),
    (S2, C_CGMLT, "Sede Chapinero",            "Chapinero",     "Calle 54 No 13-38",   "110231"),
    (S3, C_CSF,   "Sede Centro",               "La Candelaria", "Calle 13 No 9-71",    "111711"),
]
cur.executemany(
    "INSERT INTO sedes (sede_id, centro_id, nombre, barrio, direccion, codigo_postal) VALUES (%s,%s,%s,%s,%s,%s)",
    sedes,
)

# ─── AMBIENTES ───────────────────────────────────────────────────────────────
print("🏫  Insertando Ambientes...")
A1=uid(); A2=uid(); A3=uid(); A4=uid(); A5=uid()
ambientes = [
    (A1, S1, "Aula 101 - Sistemas"),
    (A2, S1, "Laboratorio de Redes"),
    (A3, S1, "Sala de Conferencias A"),
    (A4, S2, "Aula 201 - Multiusos"),
    (A5, S3, "Aula 301 - Financiero"),
]
cur.executemany(
    "INSERT INTO ambientes (ambiente_id, sede_id, nombre) VALUES (%s,%s,%s)",
    ambientes,
)

# ─── COORDINACIONES ──────────────────────────────────────────────────────────
print("🗂️  Insertando Coordinaciones...")
COORD1=uid(); COORD2=uid(); COORD3=uid()
coordinaciones = [
    (COORD1, C_CGMLT, "Coordinación Académica TIC"),
    (COORD2, C_CGMLT, "Coordinación Académica Servicios"),
    (COORD3, C_CSF,   "Coordinación Académica Finanzas"),
]
cur.executemany(
    "INSERT INTO coordinaciones (coordinacion_id, centro_id, nombre) VALUES (%s,%s,%s)",
    coordinaciones,
)

# ─── MODALIDADES ─────────────────────────────────────────────────────────────
print("📚  Insertando Modalidades...")
MOD1=uid(); MOD2=uid(); MOD3=uid()
modalidades = [
    (MOD1, "Presencial"),
    (MOD2, "Virtual"),
    (MOD3, "A distancia (Metodología)"),
]
cur.executemany(
    "INSERT INTO modalidades (modalidad_id, nombre) VALUES (%s,%s)",
    modalidades,
)

# ─── NIVELES ─────────────────────────────────────────────────────────────────
print("🎓  Insertando Niveles...")
NIV_TEC=uid(); NIV_TECNO=uid(); NIV_CC=uid()
niveles = [
    (NIV_TEC,   "Técnico"),
    (NIV_TECNO, "Tecnólogo"),
    (NIV_CC,    "Curso Corto Complementario"),
]
cur.executemany(
    "INSERT INTO niveles (nivel_id, nombre) VALUES (%s,%s)",
    niveles,
)

# ─── PROGRAMAS DE FORMACIÓN ──────────────────────────────────────────────────
print("📋  Insertando Programas de Formación...")
PF_ADSI=uid(); PF_CONT=uid(); PF_GA=uid(); PF_SIS=uid(); PF_SST=uid(); PF_CC1=uid()
programas = [
    (PF_ADSI, C_CGMLT, NIV_TECNO, MOD1, "Análisis y Desarrollo de Software",                  "228118"),
    (PF_CONT, C_CSF,   NIV_TEC,   MOD1, "Contabilización de Operaciones Comerciales",          "133312"),
    (PF_GA,   C_CGMLT, NIV_TEC,   MOD1, "Gestión Administrativa",                              "122121"),
    (PF_SIS,  C_CGMLT, NIV_TECNO, MOD2, "Sistemas de Información",                             "228120"),
    (PF_SST,  C_CGMLT, NIV_TECNO, MOD1, "Control Ambiental y Gestión del Riesgo",              "261115"),
    (PF_CC1,  C_CGMLT, NIV_CC,    MOD1, "Excel Avanzado y Herramientas de Productividad",      "230101025"),
]
cur.executemany(
    "INSERT INTO programas_formacion (programa_id, centro_id, nivel_id, modalidad_id, nombre, codigo) VALUES (%s,%s,%s,%s,%s,%s)",
    programas,
)

# ─── ROL IDs ─────────────────────────────────────────────────────────────────
cur.execute("SELECT rol_id FROM roles WHERE nombre='Instructor'")
ROL_INSTR = cur.fetchone()[0]
cur.execute("SELECT rol_id FROM roles WHERE nombre='Aprendiz'")
ROL_APR   = cur.fetchone()[0]
cur.execute("SELECT rol_id FROM roles WHERE nombre='Administrador'")
ROL_ADMIN = cur.fetchone()[0]

# ─── USUARIOS INSTRUCTORES ───────────────────────────────────────────────────
print("👨‍🏫  Insertando Instructores...")
hashed_pass = generate_password_hash("Sena2026*")

# (usuario_id, ident, tipo, correo, nombre1, nombre2, apellido1, apellido2)
instr_usuarios = [
    (uid(), "79554321", "CC", "diana.beltran@senalearn.edu.co",    "DIANA",    "PATRICIA", "BELTRAN",   "TORRES"),
    (uid(), "52871643", "CC", "carlos.ruiz@senalearn.edu.co",      "CARLOS",   "ANDRES",   "RUIZ",      "MOLINA"),
    (uid(), "1015234567","CC","jorge.medina@senalearn.edu.co",     "JORGE",    "ALBERTO",  "MEDINA",    "CASTRO"),
    (uid(), "43876521", "CC", "patricia.gomez@senalearn.edu.co",   "PATRICIA", None,       "GOMEZ",     "VARGAS"),
    (uid(), "79332198", "CC", "luis.hernandez@senalearn.edu.co",   "LUIS",     "FERNANDO", "HERNANDEZ", "SIERRA"),
]
for uid_i, ident, tipo, correo, n1, n2, a1, a2 in instr_usuarios:
    cur.execute(
        """INSERT INTO usuarios
           (usuario_id, identificacion, tipo_documento, correo, contrasena_hash,
            rol_id, cuenta_activa, correo_verificado, primer_nombre, segundo_nombre,
            primer_apellido, segundo_apellido)
           VALUES (%s,%s,%s,%s,%s,%s,1,1,%s,%s,%s,%s)""",
        (uid_i, ident, tipo, correo, hashed_pass, ROL_INSTR, n1, n2, a1, a2),
    )

# Crear registros en instructores
cur.execute("SELECT usuario_id FROM usuarios WHERE correo='diana.beltran@senalearn.edu.co'")
U_DIANA = cur.fetchone()[0]
cur.execute("SELECT usuario_id FROM usuarios WHERE correo='carlos.ruiz@senalearn.edu.co'")
U_CARLOS = cur.fetchone()[0]
cur.execute("SELECT usuario_id FROM usuarios WHERE correo='jorge.medina@senalearn.edu.co'")
U_JORGE = cur.fetchone()[0]
cur.execute("SELECT usuario_id FROM usuarios WHERE correo='patricia.gomez@senalearn.edu.co'")
U_PATRICIA = cur.fetchone()[0]
cur.execute("SELECT usuario_id FROM usuarios WHERE correo='luis.hernandez@senalearn.edu.co'")
U_LUIS = cur.fetchone()[0]

I_DIANA=uid(); I_CARLOS=uid(); I_JORGE=uid(); I_PATRICIA=uid(); I_LUIS=uid()
instructores_rows = [
    (I_DIANA,    U_DIANA,    COORD1),
    (I_CARLOS,   U_CARLOS,   COORD1),
    (I_JORGE,    U_JORGE,    COORD2),
    (I_PATRICIA, U_PATRICIA, COORD2),
    (I_LUIS,     U_LUIS,     COORD3),
]
cur.executemany(
    "INSERT INTO instructores (instructor_id, usuario_id, coordinacion_id) VALUES (%s,%s,%s)",
    instructores_rows,
)

# ─── FICHAS ──────────────────────────────────────────────────────────────────
print("🗒️  Insertando Fichas...")
F1=uid(); F2=uid(); F3=uid(); F4=uid(); F5=uid()
fichas = [
    (F1, PF_ADSI, COORD1, A1, I_DIANA,    fecha(2024,1,15), fecha(2025,1,20), fecha(2025,7,15), 2675854),
    (F2, PF_ADSI, COORD1, A2, I_CARLOS,   fecha(2024,3,4),  fecha(2025,3,10), fecha(2025,9,30), 2678902),
    (F3, PF_GA,   COORD2, A4, I_JORGE,    fecha(2024,2,1),  fecha(2024,8,15), fecha(2025,2,28), 2671234),
    (F4, PF_CONT, COORD3, A5, I_PATRICIA, fecha(2024,4,8),  fecha(2025,4,15), fecha(2025,10,8), 2683761),
    (F5, PF_SIS,  COORD1, A1, I_LUIS,     fecha(2025,1,20), fecha(2026,1,25), fecha(2026,7,20), 2690045),
]
cur.executemany(
    """INSERT INTO fichas
       (ficha_id, programa_id, coordinacion_id, ambiente_id, instructor_lider_id,
        fecha_inicio, fecha_etapa_productiva, fecha_fin, codigo)
       VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
    fichas,
)

# Instructor adicional en ficha 1
cur.execute(
    "INSERT INTO ficha_instructor (ficha_instructor_id, ficha_id, instructor_id) VALUES (%s,%s,%s)",
    (uid(), F1, I_CARLOS),
)

# ─── APRENDICES ──────────────────────────────────────────────────────────────
print("👨‍🎓  Insertando Aprendices...")

aprendices_data = [
    # Ficha 1 - ADSI 2675854
    ("1014234567","CC","JUAN",     "CARLOS",  "PEREZ",    "GARCIA",   "juan.perez@correo.com",       F1, "Activo",    "2024-01-15"),
    ("1025345678","CC","MARIA",    "PAULA",   "GARCIA",   "LOPEZ",    "maria.garcia@correo.com",     F1, "Activo",    "2024-01-15"),
    ("1036456789","CC","ANDRES",   None,      "MARTINEZ", "HERRERA",  "andres.martinez@correo.com",  F1, "Activo",    "2024-01-15"),
    ("1047567890","TI","LAURA",    "SOFIA",   "RODRIGUEZ","JIMENEZ",  "laura.rodriguez@correo.com",  F1, "Activo",    "2024-01-15"),
    ("1058678901","CC","DANIEL",   "ESTEBAN", "LOPEZ",    "BERMUDEZ", "daniel.lopez@correo.com",     F1, "Activo",    "2024-01-15"),
    ("1069789012","CC","VALENTINA",None,      "HERNANDEZ","MORA",     "valentina.h@correo.com",      F1, "Activo",    "2024-01-15"),
    ("1070890123","CC","SEBASTIAN","ANDRES",  "TORRES",   "VARGAS",   "sebastian.torres@correo.com", F1, "Activo",    "2024-01-15"),
    ("1081901234","CC","CAMILA",   "ANDREA",  "VARGAS",   "CASTRO",   "camila.vargas@correo.com",    F1, "Suspendido","2024-01-15"),
    ("1092012345","CC","NICOLAS",  None,      "CASTRO",   "REYES",    "nicolas.castro@correo.com",   F1, "Activo",    "2024-01-15"),
    ("1003123456","CC","SARA",     "LUCIA",   "MORENO",   "PINEDA",   "sara.moreno@correo.com",      F1, "Activo",    "2024-01-15"),
    # Ficha 2 - ADSI 2678902
    ("1114234567","CC","FELIPE",   "JOSE",    "ROJAS",    "SUAREZ",   "felipe.rojas@correo.com",     F2, "Activo",    "2024-03-04"),
    ("1125345678","CC","ISABELA",  "MARIA",   "SUAREZ",   "MENDEZ",   "isabela.suarez@correo.com",   F2, "Activo",    "2024-03-04"),
    ("1136456789","CC","DAVID",    "CAMILO",  "MENDEZ",   "RIOS",     "david.mendez@correo.com",     F2, "Activo",    "2024-03-04"),
    ("1147567890","TI","SANTIAGO", None,      "RIOS",     "PENA",     "santiago.rios@correo.com",    F2, "Activo",    "2024-03-04"),
    ("1158678901","CC","NATALIA",  "ALEJAND", "PENA",     "GUERRERO", "natalia.pena@correo.com",     F2, "Activo",    "2024-03-04"),
    ("1169789012","CC","JUAN",     "PABLO",   "GUERRERO", "ORTIZ",    "juan.guerrero@correo.com",    F2, "Retirado",  "2024-03-04"),
    ("1170890123","CC","MANUELA",  "CATALIN", "ORTIZ",    "SILVA",    "manuela.ortiz@correo.com",    F2, "Activo",    "2024-03-04"),
    ("1181901234","CC","JULIAN",   None,      "SILVA",    "ACOSTA",   "julian.silva@correo.com",     F2, "Activo",    "2024-03-04"),
    # Ficha 3 - Gestión Admin 2671234
    ("1214234567","CC","PAOLA",    "CRISTINA","ACOSTA",   "DELGADO",  "paola.acosta@correo.com",     F3, "Activo",    "2024-02-01"),
    ("1225345678","CC","ROBERTO",  "CARLOS",  "DELGADO",  "NUNEZ",    "roberto.delgado@correo.com",  F3, "Activo",    "2024-02-01"),
    ("1236456789","TI","ANDREA",   "PAOLA",   "NUNEZ",    "CANO",     "andrea.nunez@correo.com",     F3, "Activo",    "2024-02-01"),
    ("1247567890","CC","CRISTIAN", None,      "CANO",     "ESPINOZA", "cristian.cano@correo.com",    F3, "Activo",    "2024-02-01"),
    ("1258678901","CC","LUISA",    "FERNANDA","ESPINOZA",  "PARDO",   "luisa.espinoza@correo.com",   F3, "Activo",    "2024-02-01"),
    # Ficha 4 - Contabilidad 2683761
    ("1314234567","CC","MIGUEL",   "ANGEL",   "PARDO",    "BERMEJO",  "miguel.pardo@correo.com",     F4, "Activo",    "2024-04-08"),
    ("1325345678","CC","CAROLINA", "MARCELA", "BERMEJO",  "FUENTES",  "carolina.bermejo@correo.com", F4, "Activo",    "2024-04-08"),
    ("1336456789","CC","PABLO",    None,      "FUENTES",  "LEAL",     "pablo.fuentes@correo.com",    F4, "Activo",    "2024-04-08"),
    ("1347567890","TI","MARIANA",  "ISABEL",  "LEAL",     "CORTES",   "mariana.leal@correo.com",     F4, "Activo",    "2024-04-08"),
    ("1358678901","CC","ESTEBAN",  "MAURICIO","CORTES",   "PALACIOS", "esteban.cortes@correo.com",   F4, "Inactivo",  "2024-04-08"),
    # Ficha 5 - Sistemas 2690045
    ("1414234567","CC","VALERIA",  "SOFIA",   "PALACIOS", "ARAGON",   "valeria.palacios@correo.com", F5, "Activo",    "2025-01-20"),
    ("1425345678","CC","THOMAS",   None,      "ARAGON",   "VIDAL",    "thomas.aragon@correo.com",    F5, "Activo",    "2025-01-20"),
    ("1436456789","CC","NATALY",   "ANDREA",  "VIDAL",    "OSPINA",   "nataly.vidal@correo.com",     F5, "Activo",    "2025-01-20"),
    ("1447567890","TI","JORGE",    "LUIS",    "OSPINA",   "FAJARDO",  "jorge.ospina@correo.com",     F5, "Activo",    "2025-01-20"),
    ("1458678901","CC","ALEJANDRA",None,      "FAJARDO",  "CALDERON", "alejandra.fajardo@correo.com",F5, "Activo",    "2025-01-20"),
]

for ident, tipo, n1, n2, a1, a2, correo, ficha_id, estado, fecha_ing in aprendices_data:
    u_id = uid()
    cur.execute(
        """INSERT INTO usuarios
           (usuario_id, identificacion, tipo_documento, correo, contrasena_hash,
            rol_id, cuenta_activa, correo_verificado, primer_nombre, segundo_nombre,
            primer_apellido, segundo_apellido)
           VALUES (%s,%s,%s,%s,%s,%s,1,1,%s,%s,%s,%s)""",
        (u_id, ident, tipo, correo, hashed_pass, ROL_APR, n1, n2, a1, a2),
    )
    a_id = uid()
    cur.execute(
        """INSERT INTO aprendices
           (aprendiz_id, usuario_id, ficha_id, estado, fecha_ingreso)
           VALUES (%s,%s,%s,%s,%s)""",
        (a_id, u_id, ficha_id, estado, fecha_ing + " 07:00:00"),
    )

# ─── PROYECTOS FORMATIVOS ────────────────────────────────────────────────────
print("📐  Insertando Proyectos Formativos y Fases...")

# Proyecto de la Ficha 1 (ADSI)
PROY1 = uid()
cur.execute(
    "INSERT INTO proyectos_formativos (proyecto_id, ficha_id, titulo, descripcion) VALUES (%s,%s,%s,%s)",
    (PROY1, F1,
     "Sistema de Gestión de Inventarios para PyMEs",
     "Desarrollar un sistema web que permita a las pequeñas y medianas empresas gestionar "
     "sus inventarios de manera eficiente, incluyendo módulos de entradas, salidas, alertas y reportes."),
)

FASE1_1=uid(); FASE1_2=uid(); FASE1_3=uid(); FASE1_4=uid()
fases_p1 = [
    (FASE1_1, PROY1, "Análisis",          1, "Levantamiento de requerimientos y análisis del sistema."),
    (FASE1_2, PROY1, "Planeación",        2, "Diseño de arquitectura, base de datos y prototipado."),
    (FASE1_3, PROY1, "Ejecución",         3, "Desarrollo del sistema y pruebas unitarias."),
    (FASE1_4, PROY1, "Evaluación",        4, "Pruebas de integración, despliegue y documentación final."),
]
cur.executemany(
    "INSERT INTO fases (fase_id, proyecto_id, nombre, orden, descripcion) VALUES (%s,%s,%s,%s,%s)",
    fases_p1,
)

# Actividades de proyecto en fase 1 y 2
actps = [
    (uid(), FASE1_1, "Identificación de necesidades del cliente",       1, None),
    (uid(), FASE1_1, "Documentación de requerimientos funcionales",     2, None),
    (uid(), FASE1_1, "Diagrama de casos de uso",                        3, None),
    (uid(), FASE1_2, "Diseño de base de datos relacional",              1, None),
    (uid(), FASE1_2, "Wireframes y prototipo de interfaz",              2, None),
    (uid(), FASE1_3, "Desarrollo del módulo de autenticación",          1, None),
    (uid(), FASE1_3, "Desarrollo del módulo de inventario",             2, None),
    (uid(), FASE1_3, "Desarrollo del módulo de reportes",               3, None),
    (uid(), FASE1_4, "Pruebas de aceptación con el cliente",            1, None),
    (uid(), FASE1_4, "Despliegue en servidor de producción",            2, None),
]
act_p_ids = {}
for ap in actps:
    cur.execute(
        "INSERT INTO actividades_proyecto (actividad_proyecto_id, fase_id, nombre, orden, descripcion) VALUES (%s,%s,%s,%s,%s)",
        ap,
    )
    act_p_ids[ap[2]] = ap[0]  # nombre → id

# Actividades de aprendizaje para 3 actividades de proyecto
aprendizaje_rows = [
    (uid(), act_p_ids["Identificación de necesidades del cliente"],  "Entrevista con stakeholders",                  1),
    (uid(), act_p_ids["Identificación de necesidades del cliente"],  "Análisis de procesos actuales",                2),
    (uid(), act_p_ids["Documentación de requerimientos funcionales"],"Elaborar documento SRS",                       1),
    (uid(), act_p_ids["Documentación de requerimientos funcionales"],"Revisión y aprobación de requerimientos",      2),
    (uid(), act_p_ids["Diseño de base de datos relacional"],         "Modelo Entidad-Relación (MER)",                1),
    (uid(), act_p_ids["Diseño de base de datos relacional"],         "Normalización hasta 3FN",                     2),
    (uid(), act_p_ids["Diseño de base de datos relacional"],         "Script DDL de creación de tablas",            3),
]
cur.executemany(
    "INSERT INTO actividades_aprendizaje (actividad_aprendizaje_id, actividad_proyecto_id, nombre, orden) VALUES (%s,%s,%s,%s)",
    aprendizaje_rows,
)

# Proyecto de la Ficha 5 (Sistemas)
PROY5 = uid()
cur.execute(
    "INSERT INTO proyectos_formativos (proyecto_id, ficha_id, titulo, descripcion) VALUES (%s,%s,%s,%s)",
    (PROY5, F5,
     "Plataforma E-commerce para Artesanos Colombianos",
     "Diseñar e implementar una plataforma de comercio electrónico que permita a artesanos "
     "colombianos ofrecer y vender sus productos a nivel nacional e internacional."),
)

FASE5_1=uid(); FASE5_2=uid(); FASE5_3=uid()
cur.executemany(
    "INSERT INTO fases (fase_id, proyecto_id, nombre, orden, descripcion) VALUES (%s,%s,%s,%s,%s)",
    [
        (FASE5_1, PROY5, "Análisis y Diseño",  1, "Estudio de mercado y diseño UX/UI de la plataforma."),
        (FASE5_2, PROY5, "Desarrollo",          2, "Implementación del frontend y backend de la plataforma."),
        (FASE5_3, PROY5, "Pruebas y Lanzamiento", 3, "Testing, optimización y lanzamiento en producción."),
    ],
)

# ─── TRANSVERSALES ───────────────────────────────────────────────────────────
print("🔀  Insertando Transversales...")
TV1=uid(); TV2=uid(); TV3=uid()
cur.executemany(
    "INSERT INTO transversales (transversal_id, nombre) VALUES (%s,%s)",
    [
        (TV1, "Ética y Valores"),
        (TV2, "Comunicación Asertiva"),
        (TV3, "Emprendimiento e Innovación"),
    ],
)

# Asignar transversales a fichas
for ficha_id in [F1, F2, F3]:
    cur.executemany(
        "INSERT INTO ficha_transversal (ficha_transversal_id, ficha_id, transversal_id) VALUES (%s,%s,%s)",
        [(uid(), ficha_id, TV1), (uid(), ficha_id, TV2), (uid(), ficha_id, TV3)],
    )

# Asignar instructores a transversales
cur.executemany(
    "INSERT INTO transversal_instructor (transversal_instructor_id, transversal_id, instructor_id) VALUES (%s,%s,%s)",
    [(uid(), TV1, I_DIANA), (uid(), TV2, I_CARLOS), (uid(), TV3, I_JORGE)],
)

# ─── USUARIO ADMINISTRADOR ───────────────────────────────────────────────────
print("👑  Insertando usuario Administrador...")
cur.execute(
    """INSERT INTO usuarios
       (usuario_id, identificacion, tipo_documento, correo, contrasena_hash,
        rol_id, cuenta_activa, correo_verificado, primer_nombre, primer_apellido)
       VALUES (%s,'52001234','CC','laura.moreno@senalearn.edu.co',%s,%s,1,1,'LAURA','MORENO')""",
    (uid(), generate_password_hash("Admin2026*"), ROL_ADMIN),
)

conn.commit()
conn.close()

print("\n" + "="*60)
print("✅  DATOS DE DEMOSTRACIÓN INSERTADOS CORRECTAMENTE")
print("="*60)
print(f"  Regionales:          {len(regionales)}")
print(f"  Centros:             {len(centros)}")
print(f"  Sedes:               {len(sedes)}")
print(f"  Ambientes:           {len(ambientes)}")
print(f"  Coordinaciones:      {len(coordinaciones)}")
print(f"  Modalidades:         {len(modalidades)}")
print(f"  Niveles:             {len(niveles)}")
print(f"  Programas form.:     {len(programas)}")
print(f"  Instructores:        {len(instructores_rows)}")
print(f"  Fichas:              {len(fichas)}")
print(f"  Aprendices:          {len(aprendices_data)}")
print(f"  Proyectos formativos: 2")
print(f"  Transversales:       3")
print("="*60)
print("\n  Contraseña para TODOS los usuarios demo: Sena2026*")
print("  Admin:  laura.moreno@senalearn.edu.co  / Admin2026*")
