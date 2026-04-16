import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "internal"))

from bari_lms.services.security import hash_password
from db import connect, resolve_id
from queries import SeedQueries
from data import generate_id, SEED_PASSWORD


def get_level_id(cur, search_term):
    """Fuzzy search for Nivel Formacion to handle encoding issues like Tcnico."""
    pattern = f"%{search_term[0]}%{search_term[-1]}%"
    cur.execute("SELECT id, nombre FROM nivel_formacion WHERE nombre ILIKE %s LIMIT 1", (pattern,))
    row = cur.fetchone()
    if row:
        return str(row[0])
    cur.execute("SELECT id FROM nivel_formacion LIMIT 1")
    fallback = cur.fetchone()
    return str(fallback[0]) if fallback else None


def get_instructor_id(cur, correo):
    """Look up instructor.id by user email."""
    cur.execute("""
        SELECT i.id FROM instructor i
        JOIN usuario u ON u.id = i.persona_id
        WHERE u.correo = %s
        LIMIT 1
    """, (correo,))
    row = cur.fetchone()
    return str(row[0]) if row else None


# Aprendices for each new ficha — all in productiva_en_curso.
# (ficha_numero, correo, full_name, doc, tipo_doc, nombres, apellidos, sexo)
APRENDICES_NUEVOS = [
    # ── Ficha 2905678 (COCINA INTERNACIONAL — María López) ────────────────────
    ("2905678", "rosa.garcia@aprendiz.sena.edu.co",    "Rosa García Pineda",           "1092100001", "cc", "ROSA",       "GARCÍA PINEDA",         "f"),
    ("2905678", "hector.zapata@aprendiz.sena.edu.co",  "Héctor Zapata Romero",         "1092100002", "cc", "HÉCTOR",     "ZAPATA ROMERO",         "m"),
    ("2905678", "catalina.pena@aprendiz.sena.edu.co",  "Catalina Peña Vargas",         "1092100003", "cc", "CATALINA",   "PEÑA VARGAS",           "f"),
    # ── Ficha 3006789 (LIMPIEZA HOSPITALARIA — Carlos Rodríguez) ─────────────
    ("3006789", "luz.vasquez@aprendiz.sena.edu.co",    "Luz Marina Vásquez Contreras", "1092200001", "cc", "LUZ MARINA", "VÁSQUEZ CONTRERAS",     "f"),
    ("3006789", "gabriel.mora@aprendiz.sena.edu.co",   "Gabriel Andrés Mora Quintero", "1092200002", "cc", "GABRIEL ANDRÉS", "MORA QUINTERO",     "m"),
    ("3006789", "nathalia.reyes@aprendiz.sena.edu.co", "Nathalia Reyes Cáceres",       "1092200003", "cc", "NATHALIA",   "REYES CÁCERES",         "f"),
    # ── Ficha 5477667 (PELUQUERIA BASICA — Adriana Suárez) ───────────────────
    ("5477667", "viviana.acosta@aprendiz.sena.edu.co", "Viviana Acosta Muñoz",         "1092300001", "cc", "VIVIANA",    "ACOSTA MUÑOZ",          "f"),
    ("5477667", "edgar.rojas@aprendiz.sena.edu.co",    "Edgar Rojas Soto",             "1092300002", "cc", "EDGAR",      "ROJAS SOTO",            "m"),
    ("5477667", "melissa.pedraza@aprendiz.sena.edu.co","Melissa Pedraza Cárdenas",     "1092300003", "cc", "MELISSA",    "PEDRAZA CÁRDENAS",      "f"),
    # ── Ficha 4100992 (PRIMEROS AUXILIOS — Ricardo Mendoza) ──────────────────
    ("4100992", "oscar.ibanez@aprendiz.sena.edu.co",   "Óscar Ibáñez Fuentes",         "1092400001", "cc", "ÓSCAR",      "IBÁÑEZ FUENTES",        "m"),
    ("4100992", "carolina.luna@aprendiz.sena.edu.co",  "Carolina Luna Herrera",        "1092400002", "cc", "CAROLINA",   "LUNA HERRERA",          "f"),
    ("4100992", "yesid.gutierrez@aprendiz.sena.edu.co","Yesid Gutiérrez Páez",         "1092400003", "cc", "YESID",      "GUTIÉRREZ PÁEZ",        "m"),
]


def seed():
    conn = connect()
    cur = conn.cursor()

    try:
        print("--- Starting Full Academic Hierarchy Seed ---")

        # 1. RESOLVE FOUNDATION
        tec_id = get_level_id(cur, "Tecnico")
        tgl_id = get_level_id(cur, "Tecnolo")

        # Look up instructors by email
        inst_maria    = get_instructor_id(cur, "maria.lopez@sena.edu.co")
        inst_carlos   = get_instructor_id(cur, "carlos.rodriguez@sena.edu.co")
        inst_adriana  = get_instructor_id(cur, "adriana.suarez@sena.edu.co")
        inst_ricardo  = get_instructor_id(cur, "ricardo.mendoza@sena.edu.co")

        missing = [e for e, i in [
            ("maria.lopez",     inst_maria),
            ("carlos.rodriguez",inst_carlos),
            ("adriana.suarez",  inst_adriana),
            ("ricardo.mendoza", inst_ricardo),
        ] if not i]
        if missing:
            print(f"Instructors not found: {missing}. Run instructores.py first. Aborting.")
            return

        # Get centro_id from any instructor (all share same centro)
        cur.execute("SELECT centro_id FROM instructor WHERE id = %s", (inst_maria,))
        centro_id = str(cur.fetchone()[0])

        # 2. COORDINATION
        coord_id = '019d8dfb-3652-7e61-831d-b8d28e7e5908'
        cur.execute("""
            INSERT INTO coordinacion (id, centro_id, nombre)
            VALUES (%s, %s, 'COORDINACION DE TURISMO Y SERVICIOS')
            ON CONFLICT (id) DO NOTHING
        """, (coord_id, centro_id))

        # 3. REDES & AREAS
        redes = [
            ('019d8dfb-3652-7e61-831d-b8d28e7e5901', 'RED DE HOTELERIA Y TURISMO'),
            ('019d8e05-9988-7561-831d-b8d28e7e5910', 'RED DE SERVICIOS PERSONALES')
        ]
        for r_id, name in redes:
            cur.execute("INSERT INTO red_conocimiento (id, nombre) VALUES (%s, %s) ON CONFLICT DO NOTHING", (r_id, name))

        areas = [
            ('019d8dfb-3652-7e61-831d-b8d28e7e5902', redes[0][0], 'COCINA Y GASTRONOMIA'),
            ('019d8dfb-3652-7e61-831d-b8d28e7e5903', redes[0][0], 'LIMPIEZA E HIGIENE'),
            ('019d8e05-9988-7561-831d-b8d28e7e5911', redes[1][0], 'ESTETICA Y PELUQUERIA'),
            ('019d8e1a-4422-7e61-831d-b8d28e7e5920', redes[0][0], 'SERVICIOS DE SALUD')
        ]
        for a_id, r_id, name in areas:
            cur.execute("INSERT INTO area (id, red_conocimiento_id, nombre) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING", (a_id, r_id, name))

        # 4. PROGRAMS
        programs = [
            ('019d8dfb-3652-7e61-831d-b8d28e7e5904', areas[0][0], tec_id, 'COCINA INTERNACIONAL'),
            ('019d8dfb-3652-7e61-831d-b8d28e7e5906', areas[1][0], tec_id, 'LIMPIEZA HOSPITALARIA'),
            ('019d8e1a-4422-7e61-831d-b8d28e7e5921', areas[3][0], tec_id, 'PRIMEROS AUXILIOS'),
            ('019d8e05-9988-7561-831d-b8d28e7e5912', areas[2][0], tgl_id, 'PELUQUERIA BASICA')
        ]
        for p_id, a_id, n_id, name in programs:
            cur.execute("INSERT INTO programa_formacion (id, area_id, nivel_formacion_id, nombre) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING", (p_id, a_id, n_id, name))

        # 5. PROJECTS
        projects = [
            ('019d8e2b-7711-7e61-831d-b8d28e7e5930', 'PF-GASTRO-001',     'FORTALECIMIENTO DE LA CULTURA GASTRONOMICA'),
            ('019d8e2b-7711-7e61-831d-b8d28e7e5931', 'PF-HIGIENE-005',    'PROTOCOLO BIOSEGURIDAD'),
            ('019d8e2b-7711-7e61-831d-b8d28e7e5932', 'PF-SALUD-010',      'RESPUESTA EMERGENCIAS'),
            ('019d8e05-9988-7561-831d-b8d28e7e5913', 'PF-PELUQUERIA-002', 'ESTILO Y COSMETOLOGIA')
        ]
        for pr_id, code, name in projects:
            cur.execute("INSERT INTO proyecto_formativo (id, codigo, nombre) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING", (pr_id, code, name))

        # 6. FICHAS — each assigned to a different instructor
        fichas = [
            ('2905678', programs[0][0], projects[0][0], inst_maria),    # COCINA INTERNACIONAL → María López
            ('3006789', programs[1][0], projects[1][0], inst_carlos),   # LIMPIEZA HOSPITALARIA → Carlos Rodríguez
            ('5477667', programs[3][0], projects[3][0], inst_adriana),  # PELUQUERIA BASICA → Adriana Suárez
            ('4100992', programs[2][0], projects[2][0], inst_ricardo),  # PRIMEROS AUXILIOS → Ricardo Mendoza
        ]
        for num, p_id, pr_id, inst_id in fichas:
            cur.execute("""
                INSERT INTO ficha_formacion (id, numero, programa_formacion_id, coordinacion_id, proyecto_formativo_id, instructor_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (numero) DO UPDATE SET instructor_id = EXCLUDED.instructor_id
            """, (generate_id(), num, p_id, coord_id, pr_id, inst_id))
        print("   [OK] Fichas inserted")

        # 7. APRENDICES — all in productiva_en_curso
        print("--- Seeding Aprendices for new fichas ---")
        pw_hash     = hash_password(SEED_PASSWORD)
        regional_id = resolve_id(cur, "regional", "nombre", "Regional Norte de Santander")
        perfil_id   = resolve_id(cur, "perfil", "nombre", "Aprendiz")

        tipo_cc_id = resolve_id(cur, "tipo_documento", "codigo", "cc")
        sexo_m_id  = resolve_id(cur, "sexo", "codigo", "m")
        sexo_f_id  = resolve_id(cur, "sexo", "codigo", "f")

        for f_num, correo, full_name, doc, tipo_doc_cod, nombres, apellidos, sexo_cod in APRENDICES_NUEVOS:
            print(f"  > {correo}")

            tipo_doc_id = resolve_id(cur, "tipo_documento", "codigo", tipo_doc_cod)
            sexo_id     = resolve_id(cur, "sexo", "codigo", sexo_cod)

            # A. Usuario
            u_id   = generate_id()
            is_new = SeedQueries.INSERT_USUARIO.execute(cur, (u_id, correo, pw_hash, full_name))
            u_id   = resolve_id(cur, "usuario", "correo", correo)

            # B. Persona
            SeedQueries.INSERT_PERSONA.execute(cur, (u_id, tipo_doc_id, doc, nombres, apellidos, sexo_id))

            # C. Aprendiz entity
            SeedQueries.INSERT_APRENDIZ.execute(cur, (generate_id(), u_id, regional_id))
            apr_id = resolve_id(cur, "aprendiz", "persona_id", u_id)

            # D. Profile link
            if perfil_id:
                SeedQueries.INSERT_PERFIL_LINK.execute(cur, (generate_id(), u_id, perfil_id))

            # E. Ficha enrollment — productiva_en_curso
            ficha_id = resolve_id(cur, "ficha_formacion", "numero", f_num)
            if ficha_id and apr_id:
                SeedQueries.INSERT_FICHA_APRENDIZ.execute(cur, (
                    generate_id(), ficha_id, apr_id, "productiva_en_curso",
                ))

            print(f"    {'[NEW]' if is_new else '[EXISTING]'}")

        conn.commit()
        print("--- Full Seed Successful ---")
        print("\n-- Instructor -> Ficha mapping --")
        print("  2905678 (COCINA INTERNACIONAL)  -> maria.lopez@sena.edu.co")
        print("  3006789 (LIMPIEZA HOSPITALARIA) -> carlos.rodriguez@sena.edu.co")
        print("  5477667 (PELUQUERIA BASICA)     -> adriana.suarez@sena.edu.co")
        print("  4100992 (PRIMEROS AUXILIOS)     -> ricardo.mendoza@sena.edu.co")

    except Exception as e:
        conn.rollback()
        print(f"Seed Error: {e}")
        raise
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    seed()
