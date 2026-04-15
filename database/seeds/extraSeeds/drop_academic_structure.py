"""
drop_academic_structure.py — Full hierarchy cleanup.
Fixed version using individual deletes to bypass adapter syntax errors ($1).
"""

from db import connect

APRENDICES_CORREOS = [
    # Ficha 2905678
    "rosa.garcia@aprendiz.sena.edu.co",
    "hector.zapata@aprendiz.sena.edu.co",
    "catalina.pena@aprendiz.sena.edu.co",
    # Ficha 3006789
    "luz.vasquez@aprendiz.sena.edu.co",
    "gabriel.mora@aprendiz.sena.edu.co",
    "nathalia.reyes@aprendiz.sena.edu.co",
    # Ficha 5477667
    "viviana.acosta@aprendiz.sena.edu.co",
    "edgar.rojas@aprendiz.sena.edu.co",
    "melissa.pedraza@aprendiz.sena.edu.co",
    # Ficha 4100992
    "oscar.ibanez@aprendiz.sena.edu.co",
    "carolina.luna@aprendiz.sena.edu.co",
    "yesid.gutierrez@aprendiz.sena.edu.co",
]


def cleanup():
    conn = connect()
    cur = conn.cursor()

    try:
        print("--- Starting Full Cleanup of Seeded Data ---")

        # 0. DELETE APRENDICES (must go before fichas due to RESTRICT FK)
        for correo in APRENDICES_CORREOS:
            # Resolve usuario id
            cur.execute("SELECT id FROM usuario WHERE correo = %s", (correo,))
            row = cur.fetchone()
            if not row:
                continue
            u_id = str(row[0])

            # Resolve aprendiz id
            cur.execute("SELECT id FROM aprendiz WHERE persona_id = %s", (u_id,))
            row = cur.fetchone()
            if row:
                apr_id = str(row[0])
                cur.execute("DELETE FROM ficha_aprendiz WHERE aprendiz_id = %s", (apr_id,))
                cur.execute("DELETE FROM aprendiz WHERE id = %s", (apr_id,))

            cur.execute("DELETE FROM usuario_perfil WHERE usuario_id = %s", (u_id,))
            cur.execute("DELETE FROM persona WHERE id = %s", (u_id,))
            cur.execute("DELETE FROM usuario WHERE id = %s", (u_id,))

        print(f"   [OK] Deleted {len(APRENDICES_CORREOS)} Aprendices")

        # 1. DELETE FICHAS
        fichas_to_drop = ['2905678', '3006789', '5477667', '4100992']
        for num in fichas_to_drop:
            cur.execute("DELETE FROM ficha_formacion WHERE numero = %s", (num,))
        print(f"   [OK] Deleted Fichas: {fichas_to_drop}")

        # 2. DELETE PROJECTS
        project_ids = [
            '019d8e2b-7711-7e61-831d-b8d28e7e5930',
            '019d8e2b-7711-7e61-831d-b8d28e7e5931',
            '019d8e2b-7711-7e61-831d-b8d28e7e5932',
            '019d8e05-9988-7561-831d-b8d28e7e5913'
        ]
        for pr_id in project_ids:
            cur.execute("DELETE FROM proyecto_formativo WHERE id = %s", (pr_id,))
        print("   [OK] Deleted 4 Proyectos Formativos")

        # 3. DELETE PROGRAMS
        program_ids = [
            '019d8dfb-3652-7e61-831d-b8d28e7e5904',
            '019d8dfb-3652-7e61-831d-b8d28e7e5906',
            '019d8e1a-4422-7e61-831d-b8d28e7e5921',
            '019d8e05-9988-7561-831d-b8d28e7e5912'
        ]
        for p_id in program_ids:
            cur.execute("DELETE FROM programa_formacion WHERE id = %s", (p_id,))
        print("   [OK] Deleted 4 Programas de Formación")

        # 4. DELETE AREAS
        area_ids = [
            '019d8dfb-3652-7e61-831d-b8d28e7e5902',
            '019d8dfb-3652-7e61-831d-b8d28e7e5903',
            '019d8e05-9988-7561-831d-b8d28e7e5911',
            '019d8e1a-4422-7e61-831d-b8d28e7e5920'
        ]
        for a_id in area_ids:
            cur.execute("DELETE FROM area WHERE id = %s", (a_id,))
        print("   [OK] Deleted 4 Areas")

        # 5. DELETE KNOWLEDGE NETWORKS
        red_ids = [
            '019d8dfb-3652-7e61-831d-b8d28e7e5901',
            '019d8e05-9988-7561-831d-b8d28e7e5910'
        ]
        for r_id in red_ids:
            cur.execute("DELETE FROM red_conocimiento WHERE id = %s", (r_id,))
        print("   [OK] Deleted 2 Redes de Conocimiento")

        # 6. DELETE COORDINATION
        cur.execute("DELETE FROM coordinacion WHERE id = '019d8dfb-3652-7e61-831d-b8d28e7e5908'")
        print("   [OK] Deleted Coordination: Turismo y Servicios")

        conn.commit()
        print("\n--- Full Cleanup Successful ---")

    except Exception as e:
        conn.rollback()
        print(f"\n[!] Cleanup failed: {e}")
        raise
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    cleanup()
