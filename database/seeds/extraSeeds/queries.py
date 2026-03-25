from enum import Enum

class SeedQueries(Enum):
    # --- Catalogs ---
    INSERT_TIPO_DOC = """
        INSERT INTO tipo_documento (id, codigo, nombre)
        VALUES (%s, %s, %s) ON CONFLICT (codigo) DO NOTHING
    """
    
    INSERT_SEXO = """
        INSERT INTO sexo (id, codigo, nombre)
        VALUES (%s, %s, %s) ON CONFLICT (codigo) DO NOTHING
    """

    INSERT_NIVEL_FORMACION = """
        INSERT INTO nivel_formacion (id, nombre)
        VALUES (%s, %s) ON CONFLICT (nombre) DO NOTHING
    """

    # --- Institutional Structure ---
    INSERT_REGIONAL = """
        INSERT INTO regional (id, nombre)
        VALUES (%s, %s) ON CONFLICT (nombre) DO NOTHING
    """

    INSERT_CENTRO = """
        INSERT INTO centro (id, regional_id, nombre)
        VALUES (%s, %s, %s) ON CONFLICT (nombre) DO NOTHING
    """

    INSERT_COORDINACION = """
        INSERT INTO coordinacion (id, centro_id, nombre)
        VALUES (%s, %s, %s) ON CONFLICT (nombre) DO NOTHING
    """

    # --- Knowledge Area & Programs ---
    INSERT_RED = """
        INSERT INTO red_conocimiento (id, nombre)
        VALUES (%s, %s) ON CONFLICT (nombre) DO NOTHING
    """

    INSERT_AREA = """
        INSERT INTO area (id, red_conocimiento_id, nombre)
        VALUES (%s, %s, %s) ON CONFLICT (nombre) DO NOTHING
    """

    INSERT_PROGRAMA = """
        INSERT INTO programa_formacion (id, area_id, nivel_formacion_id, nombre)
        VALUES (%s, %s, %s, %s) ON CONFLICT (nombre) DO NOTHING
    """

    # --- Projects & Phases ---
    INSERT_PROYECTO = """
        INSERT INTO proyecto_formativo (id, codigo, nombre)
        VALUES (%s, %s, %s) ON CONFLICT (codigo) DO NOTHING
    """

    INSERT_FASE = """
        INSERT INTO fase_proyecto (id, proyecto_formativo_id, nombre)
        VALUES (%s, %s, %s) ON CONFLICT DO NOTHING
    """

    # --- Users & Instructors ---
    INSERT_USUARIO = """
        INSERT INTO usuario (id, correo, contrasena_hash, nombre, activo)
        VALUES (%s, %s, %s, %s, TRUE) ON CONFLICT (correo) DO NOTHING
    """

    INSERT_PERSONA = """
        INSERT INTO persona (id, tipo_documento_id, numero_documento, nombres, apellidos, sexo_id)
        VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
    """

    INSERT_INSTRUCTOR = """
        INSERT INTO instructor (id, persona_id, centro_id, area_id)
        VALUES (%s, %s, %s, %s) ON CONFLICT (persona_id) DO NOTHING
    """

    INSERT_PERFIL_LINK = """
        INSERT INTO usuario_perfil (id, usuario_id, perfil_id)
        VALUES (%s, %s, %s) ON CONFLICT (usuario_id, perfil_id) DO NOTHING
    """

    INSERT_FICHA = """
        INSERT INTO ficha_formacion 
        (id, numero, programa_formacion_id, coordinacion_id, proyecto_formativo_id, instructor_id)
        VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (numero) DO NOTHING
    """
    INSERT_EMPRESA = """
        INSERT INTO empresa (id, razon_social, nit, sector, correo, telefono)
        VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (nit) DO NOTHING
    """


    # --- Apprentice Specific ---

    INSERT_APRENDIZ = """
        INSERT INTO aprendiz (id, persona_id, regional_id)
        VALUES (%s, %s, %s) ON CONFLICT (persona_id) DO NOTHING
    """


    # --- Enrollment (Ficha-Aprendiz) ---

    INSERT_FICHA_APRENDIZ = """
        INSERT INTO ficha_aprendiz (
            id, ficha_id, aprendiz_id, 
            en_etapa_lectiva, etapa_lectiva_concluida, en_etapa_productiva
        )
        VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
    """
    
    # (razon_social, nit, sector, correo, telefono)
    DATA_EMPRESAS = [
        ("TechSoft SAS", "9005123456", "Tecnología", "contacto@techsoft.com.co", "6075551234"),
        ("Innovatech Ltda", "8002345678", "Consultoría TIC", "info@innovatech.com.co", "6075559876"),
    ]

    # (correo, nombre_full, doc, tipo_doc, nombres, apellidos, sexo, ficha_num, lectiva, concluida, productiva)
    DATA_APRENDICES = [
        ("ana.gomez@aprendiz.sena.edu.co", "Ana Sofía Gómez Herrera", "1090123456", "cc", "ANA SOFÍA", "GÓMEZ HERRERA", "f", "2900001", True, False, False),
        ("luis.torres@aprendiz.sena.edu.co", "Luis Eduardo Torres Prado", "1090234567", "cc", "LUIS EDUARDO", "TORRES PRADO", "m", "2900001", False, True, True),
        ("sofia.mendez@aprendiz.sena.edu.co", "Sofía Alejandra Méndez Ríos", "1025345678", "ti", "SOFÍA ALEJANDRA", "MÉNDEZ RÍOS", "f", "2900002", True, False, False),
        ("andres.ruiz@aprendiz.sena.edu.co", "Andrés Felipe Ruiz Castillo", "1025456789", "ti", "ANDRÉS FELIPE", "RUIZ CASTILLO", "m", "2900002", False, True, True),
        ("camila.vargas@aprendiz.sena.edu.co", "Camila Andrea Vargas Soto", "1090567890", "cc", "CAMILA ANDREA", "VARGAS SOTO", "f", "2900003", True, False, False),
        ("miguel.castro@aprendiz.sena.edu.co", "Miguel Ángel Castro Jiménez", "1090678901", "cc", "MIGUEL ÁNGEL", "CASTRO JIMÉNEZ", "m", "2900003", False, True, False),
    ]

    def execute(self, cur, params):
        """
        Executes the query associated with the enum member.
        Returns True if a row was actually inserted.
        """
        cur.execute(self.value, params)
        return cur.rowcount > 0