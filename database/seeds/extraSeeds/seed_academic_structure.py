import sys
from db import connect
from data import generate_id

def get_level_id(cur, search_term):
    """Fuzzy search for Nivel Formacion to handle encoding issues like Tcnico."""
    pattern = f"%{search_term[0]}%{search_term[-1]}%"
    cur.execute("SELECT id, nombre FROM nivel_formacion WHERE nombre ILIKE %s LIMIT 1", (pattern,))
    row = cur.fetchone()
    if row:
        return str(row[0])
    # Absolute fallback to first available row if search fails
    cur.execute("SELECT id FROM nivel_formacion LIMIT 1")
    fallback = cur.fetchone()
    return str(fallback[0]) if fallback else None

def seed():
    conn = connect()
    cur = conn.cursor()

    try:
        print("--- Starting Full Academic Hierarchy Seed ---")

        # 1. RESOLVE FOUNDATION (Levels and Instructor)
        tec_id = get_level_id(cur, "Tecnico")
        tgl_id = get_level_id(cur, "Tecnolo")
        
        # Using Juan Carlos Pérez as the primary instructor from your screenshots
        inst_id = "019d91e2-ee3d-7571-befd-0a387ccf3636"
        
        # Verify Instructor & Center
        cur.execute("SELECT centro_id FROM instructor WHERE id = %s", (inst_id,))
        inst_data = cur.fetchone()
        if not inst_data:
            print("Target Instructor not found. Aborting.")
            return
        centro_id = str(inst_data[0])

        # 2. INSTITUTIONAL FOUNDATION
        # We reuse your Coordination ID from the SQL
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
            ('019d8e2b-7711-7e61-831d-b8d28e7e5930', 'PF-GASTRO-001', 'FORTALECIMIENTO DE LA CULTURA GASTRONOMICA'),
            ('019d8e2b-7711-7e61-831d-b8d28e7e5931', 'PF-HIGIENE-005', 'PROTOCOLO BIOSEGURIDAD'),
            ('019d8e2b-7711-7e61-831d-b8d28e7e5932', 'PF-SALUD-010', 'RESPUESTA EMERGENCIAS'),
            ('019d8e05-9988-7561-831d-b8d28e7e5913', 'PF-PELUQUERIA-002', 'ESTILO Y COSMETOLOGIA')
        ]
        for pr_id, code, name in projects:
            cur.execute("INSERT INTO proyecto_formativo (id, codigo, nombre) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING", (pr_id, code, name))

        # 6. FICHAS
        fichas = [
            ('2905678', programs[0][0], projects[0][0]),
            ('3006789', programs[1][0], projects[1][0]),
            ('5477667', programs[3][0], projects[3][0]),
            ('4100992', programs[2][0], projects[2][0])
        ]
        for num, p_id, pr_id in fichas:
            cur.execute("""
                INSERT INTO ficha_formacion (id, numero, programa_formacion_id, coordinacion_id, proyecto_formativo_id, instructor_id)
                VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
            """, (generate_id(), num, p_id, coord_id, pr_id, inst_id))

        conn.commit()
        print("--- Full Seed Successful ---")

    except Exception as e:
        conn.rollback()
        print(f"Seed Error: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    seed()