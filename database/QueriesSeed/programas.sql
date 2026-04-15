BEGIN;

-- ==========================================
-- 1. INSTITUTIONAL FOUNDATION
-- ==========================================
INSERT INTO regional (id, nombre) 
VALUES ('019d8dfb-3652-7e61-831d-b8d28e7e5900', 'REGIONAL DISTRITO CAPITAL') ON CONFLICT DO NOTHING;

INSERT INTO centro (id, regional_id, nombre) 
VALUES ('019d8dbc-dde7-72a6-96af-5f2474b45781', '019d8dfb-3652-7e61-831d-b8d28e7e5900', 'CENTRO DE SERVICIOS FINANCIEROS') ON CONFLICT DO NOTHING;

INSERT INTO coordinacion (id, centro_id, nombre) 
VALUES ('019d8dfb-3652-7e61-831d-b8d28e7e5908', '019d8dbc-dde7-72a6-96af-5f2474b45781', 'COORDINACION DE TURISMO Y SERVICIOS') ON CONFLICT DO NOTHING;

-- ==========================================
-- 2. ACADEMIC HIERARCHY (REDES & AREAS)
-- ==========================================
INSERT INTO red_conocimiento (id, nombre) VALUES 
    ('019d8dfb-3652-7e61-831d-b8d28e7e5901', 'RED DE HOTELERIA Y TURISMO'),
    ('019d8e05-9988-7561-831d-b8d28e7e5910', 'RED DE SERVICIOS PERSONALES') 
ON CONFLICT DO NOTHING;

INSERT INTO area (id, red_conocimiento_id, nombre) VALUES 
    ('019d8dfb-3652-7e61-831d-b8d28e7e5902', '019d8dfb-3652-7e61-831d-b8d28e7e5901', 'COCINA Y GASTRONOMIA'),
    ('019d8dfb-3652-7e61-831d-b8d28e7e5903', '019d8dfb-3652-7e61-831d-b8d28e7e5901', 'LIMPIEZA E HIGIENE'),
    ('019d8e05-9988-7561-831d-b8d28e7e5911', '019d8e05-9988-7561-831d-b8d28e7e5910', 'ESTETICA Y PELUQUERIA'),
    ('019d8e1a-4422-7e61-831d-b8d28e7e5920', '019d8dfb-3652-7e61-831d-b8d28e7e5901', 'SERVICIOS DE SALUD')
ON CONFLICT DO NOTHING;

-- ==========================================
-- 3. PROGRAMS & PROJECTS
-- ==========================================
-- Using safe ASCII names to prevent UnicodeDecodeError
INSERT INTO programa_formacion (id, area_id, nivel_formacion_id, nombre) VALUES 
    ('019d8dfb-3652-7e61-831d-b8d28e7e5904', '019d8dfb-3652-7e61-831d-b8d28e7e5902', '019d8dbc-1259-7183-bb57-c9d1cbc1df70', 'COCINA INTERNACIONAL'),
    ('019d8dfb-3652-7e61-831d-b8d28e7e5906', '019d8dfb-3652-7e61-831d-b8d28e7e5903', '019d8dbc-1259-7183-bb57-c9d1cbc1df70', 'LIMPIEZA HOSPITALARIA'),
    ('019d8e1a-4422-7e61-831d-b8d28e7e5921', '019d8e1a-4422-7e61-831d-b8d28e7e5920', '019d8dbc-1259-7183-bb57-c9d1cbc1df70', 'PRIMEROS AUXILIOS'),
    ('019d8e05-9988-7561-831d-b8d28e7e5912', '019d8e05-9988-7561-831d-b8d28e7e5911', '019d8dbc-1259-7183-bb57-c9d229b2903e', 'PELUQUERIA BASICA');

INSERT INTO proyecto_formativo (id, codigo, nombre)
VALUES ('019d8e05-9988-7561-831d-b8d28e7e5913', 'PF-PELUQUERIA-002', 'COSMETOLOGIA PELUQUERIA Y ESTILO') 
ON CONFLICT DO NOTHING;

-- ==========================================
-- 4. OPERATIONAL DATA (FICHAS)
-- ==========================================
INSERT INTO ficha_formacion (id, numero, programa_formacion_id, coordinacion_id, proyecto_formativo_id, instructor_id) VALUES 
    (gen_random_uuid(), '2905678', '019d8dfb-3652-7e61-831d-b8d28e7e5904', '019d8dfb-3652-7e61-831d-b8d28e7e5908', NULL, '019d8dbc-deb5-72b7-b67c-af6126cff896'),
    (gen_random_uuid(), '3006789', '019d8dfb-3652-7e61-831d-b8d28e7e5906', '019d8dfb-3652-7e61-831d-b8d28e7e5908', NULL, '019d8dbc-deb5-72b7-b67c-af6126cff896'),
    ('019d8e05-9988-7561-831d-b8d28e7e5914', '5477667', '019d8e05-9988-7561-831d-b8d28e7e5912', '019d8dfb-3652-7e61-831d-b8d28e7e5908', '019d8e05-9988-7561-831d-b8d28e7e5913', '019d8dbc-deb5-72b7-b67c-af6126cff896'),
    (gen_random_uuid(), '4100992', '019d8e1a-4422-7e61-831d-b8d28e7e5921', '019d8dfb-3652-7e61-831d-b8d28e7e5908', NULL, '019d8dbc-debc-7015-a67c-39159edf3738');

COMMIT;