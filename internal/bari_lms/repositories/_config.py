"""Configuración de entidades del repositorio: metadatos de tablas y dominios."""

ENTITY_CONFIG = {
    # --- ESTRUCTURA INSTITUCIONAL ---
    "regional": {
        "table": "regional",
        "label": "Regional",
        "parent_key": None,
        "fields": ["nombre"],
        "required": ["nombre"],
        "context_key": "regional_id",
        "cascades": [("centro", "regional_id"), ("aprendiz", "regional_id")],
    },
    "centro": {
        "table": "centro",
        "label": "Centro de formación",
        "parent_key": "regional_id",
        "fields": ["regional_id", "nombre"],
        "required": ["regional_id", "nombre"],
        "context_key": "centro_id",
        "cascades": [
            ("coordinacion", "centro_id"), 
            ("sede", "centro_id"), 
            ("instructor", "centro_id"), 
            ("administrativo_persona", "centro_id")
        ],
    },
    "coordinacion": {
        "table": "coordinacion",
        "label": "Coordinación",
        "parent_key": "centro_id",
        "fields": ["centro_id", "nombre"],
        "required": ["centro_id", "nombre"],
        "context_key": "coordinacion_id",
        "cascades": [("ficha", "coordinacion_id")],
    },
    "sede": {
        "table": "sede",
        "label": "Sede",
        "parent_key": "centro_id",
        "fields": ["centro_id", "nombre"],
        "required": ["centro_id", "nombre"],
        "context_key": "sede_id",
        "cascades": [("ambiente", "sede_id")],
    },
    "ambiente": {
        "table": "ambiente",
        "label": "Ambiente",
        "parent_key": "sede_id",
        "fields": ["sede_id", "nombre", "capacidad"],
        "required": ["sede_id", "nombre"],
        "context_key": "sede_id",
    },

    # --- ESTRUCTURA ACADÉMICA ---
    "red": {
        "table": "red_conocimiento",
        "label": "Red de conocimiento",
        "parent_key": None,
        "fields": ["nombre"],
        "required": ["nombre"],
        "context_key": "red_id",
        "cascades": [("area", "red_conocimiento_id")],
    },
    "area": {
        "table": "area",
        "label": "Area",
        "parent_key": "red_id",
        "fields": ["red_conocimiento_id", "nombre"],
        "required": ["red_conocimiento_id", "nombre"],
        "context_key": "area_id",
        "select_aliases": {"red_conocimiento_id": "red_id"},
        "form_to_db": {"red_id": "red_conocimiento_id"},
        "cascades": [("programa", "area_id"), ("instructor", "area_id")],
    },
    "nivel": {
        "table": "nivel_formacion",
        "label": "Nivel de formación",
        "parent_key": None,
        "fields": ["nombre"],
        "required": ["nombre"],
        "context_key": "nivel_id",
        "cascades": [("programa", "nivel_formacion_id")],
    },
    "programa": {
        "table": "programa_formacion",
        "label": "Programa de formación",
        "parent_key": "area_id",
        "fields": ["area_id", "nivel_formacion_id", "nombre"],
        "required": ["area_id", "nivel_formacion_id", "nombre"],
        "context_key": "programa_id",
        "select_aliases": {"nivel_formacion_id": "nivel_id"},
        "form_to_db": {"nivel_id": "nivel_formacion_id"},
        "cascades": [("ficha", "programa_formacion_id")],
    },
    "ficha": {
        "table": "ficha_formacion",
        "label": "Ficha de formación",
        "parent_key": "programa_id",
        "fields": ["numero", "programa_formacion_id", "proyecto_formativo_id", "coordinacion_id", "instructor_id"],
        "required": ["numero", "programa_formacion_id", "proyecto_formativo_id", "coordinacion_id"],
        "context_key": "programa_id",
        "select_aliases": {"programa_formacion_id": "programa_id"},
        "form_to_db": {"programa_id": "programa_formacion_id"},
        # Added cascades for Etapa Productiva and Attendance
        "cascades": [
            ("asistencia_aprendiz", "ficha_id"), 
            ("ficha_aprendiz", "ficha_id"),  # <--- CRITICAL FIX
            ("ficha_instructor", "ficha_id")
        ],
    },

    # --- ETAPA PRODUCTIVA MODULE ---
    "ficha_aprendiz": {
        "table": "ficha_aprendiz",
        "label": "Inscripción de Aprendiz",
        "cascades": [("contrato_aprendizaje", "ficha_aprendiz_id")], # <--- CRITICAL FIX
    },
    "contrato_aprendizaje": {
        "table": "contrato_aprendizaje",
        "label": "Contrato de Aprendizaje",
    },
    "empresa": {
        "table": "empresa",
        "label": "Empresa",
        "fields": ["razon_social", "nit", "sector", "correo", "telefono", "direccion"],
        "cascades": [("contrato_aprendizaje", "empresa_id")],
    },

    # --- CONTENIDO DE PROYECTO ---
    "proyecto_formativo": {
        "table": "proyecto_formativo",
        "label": "Proyecto formativo",
        "parent_key": None,
        "fields": ["codigo", "nombre"],
        "required": ["codigo", "nombre"],
        "context_key": "proyecto_formativo_id",
        "cascades": [("fase_proyecto", "proyecto_formativo_id"), ("ficha", "proyecto_formativo_id")],
    },
    "fase_proyecto": {
        "table": "fase_proyecto",
        "label": "Fase del proyecto",
        "parent_key": "proyecto_formativo_id",
        "fields": ["proyecto_formativo_id", "nombre"],
        "required": ["proyecto_formativo_id", "nombre"],
        "context_key": "fase_id",
        "cascades": [("actividad_proyecto", "fase_proyecto_id")],
    },
    "actividad_proyecto": {
        "table": "actividad_proyecto",
        "label": "Actividad del proyecto",
        "parent_key": "fase_id",
        "fields": ["fase_proyecto_id", "nombre"],
        "required": ["fase_proyecto_id", "nombre"],
        "context_key": "fase_id",
        "select_aliases": {"fase_proyecto_id": "fid"},
        "form_to_db": {"fase_id": "fase_proyecto_id"},
        "cascades": [("actividad_aprendizaje", "actividad_proyecto_id"), ("guia_actividad_proyecto", "actividad_proyecto_id")],
    },
    "actividad_aprendizaje": {
        "table": "actividad_aprendizaje",
        "label": "Actividad de aprendizaje",
        "parent_key": "actividad_proyecto_id",
        "fields": ["actividad_proyecto_id", "nombre"],
        "required": ["actividad_proyecto_id", "nombre"],
        "context_key": "actividad_proyecto_id",
        "cascades": [("guia_aprendizaje", "actividad_aprendizaje_id"), ("evidencia_aprendizaje", "actividad_aprendizaje_id"), ("seccion_actividad", "actividad_aprendizaje_id")],
    },
    "guia_aprendizaje": { "table": "guia_aprendizaje" },
    "evidencia_aprendizaje": { 
        "table": "evidencia_aprendizaje",
        "cascades": [("entrega_evidencia", "evidencia_aprendizaje_id")]
    },
    "seccion_actividad": {
        "table": "seccion_actividad",
        "cascades": [("sub_seccion_actividad", "seccion_id")]
    },
    "sub_seccion_actividad": { "table": "sub_seccion_actividad" },
    "guia_actividad_proyecto": { "table": "guia_actividad_proyecto" },
    "entrega_evidencia": { "table": "entrega_evidencia" },

    # --- PERSONAS Y ROLES ---
    "instructor": {
        "table": "instructor",
        "label": "Instructor",
        "parent_key": "centro_id",
        "fields": ["centro_id", "area_id"],
        "persona_form_fields": ["documento", "nombres", "apellidos", "correo"],
        "required": ["centro_id", "documento", "nombres", "apellidos"],
        "join": "JOIN persona pe ON pe.id = instructor.persona_id",
        "extra_select": "pe.nombres, pe.apellidos, pe.numero_documento AS documento, pe.correo_personal AS email, instructor.persona_id",
        "cascades": [("ficha", "instructor_id"), ("ficha_instructor", "instructor_id")],
    },
    "aprendiz": {
        "table": "aprendiz",
        "label": "Aprendiz",
        "parent_key": "regional_id",
        "fields": ["regional_id", "ficha"],
        "persona_form_fields": ["documento", "nombres", "apellidos", "correo"],
        "required": ["regional_id", "documento", "nombres", "apellidos"],
        "join": "JOIN persona pe ON pe.id = aprendiz.persona_id",
        "extra_select": "pe.nombres, pe.apellidos, pe.numero_documento AS documento, pe.correo_personal AS email, aprendiz.persona_id",
        "cascades": [("ficha_aprendiz", "aprendiz_id"), ("asistencia_aprendiz", "aprendiz_id")],
    },
    "administrativo_persona": {
        "table": "personal_administrativo",
        "label": "Personal administrativo",
        "parent_key": "centro_id",
        "fields": ["centro_id", "cargo"],
        "persona_form_fields": ["documento", "nombres", "apellidos", "correo"],
        "required": ["centro_id", "cargo", "documento", "nombres", "apellidos"],
        "join": "JOIN persona pe ON pe.id = personal_administrativo.persona_id",
        "extra_select": "pe.nombres, pe.apellidos, pe.numero_documento AS documento, pe.correo_personal AS email, personal_administrativo.persona_id",
    },
    "asistencia_aprendiz": { "table": "asistencia_aprendiz" },
    "ficha_instructor": { "table": "ficha_instructor_competencia" },
}

STRUCTURE_ENTITIES = {"regional", "centro", "coordinacion", "sede", "ambiente"}
PEOPLE_ENTITIES = {"instructor", "aprendiz", "administrativo_persona"}
ACADEMIC_ENTITIES = {
    "red", "area", "nivel", "programa", "ficha",
    "proyecto_formativo", "fase_proyecto", "actividad_proyecto", "actividad_aprendizaje",
}

PERSON_USER_CONFIG = {
    "instructor": {
        "role": "Instructor",
        "email_prefix": "instructor",
        "table": "instructor",
    },
    "aprendiz": {
        "role": "Aprendiz",
        "email_prefix": "aprendiz",
        "table": "aprendiz",
    },
    "administrativo_persona": {
        "role": "Administrativo",
        "email_prefix": "administrativo",
        "table": "personal_administrativo",
    },
}
