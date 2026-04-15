BEGIN;

-- ==========================================
-- 1. PROYECTOS FORMATIVOS ADICIONALES
-- ==========================================
-- Creamos proyectos para Gastronomia, Limpieza y Salud
INSERT INTO proyecto_formativo (id, codigo, nombre) VALUES 
    ('019d8e2b-7711-7e61-831d-b8d28e7e5930', 'PF-GASTRO-001', 'FORTALECIMIENTO DE LA CULTURA GASTRONOMICA LOCAL'),
    ('019d8e2b-7711-7e61-831d-b8d28e7e5931', 'PF-HIGIENE-005', 'IMPLEMENTACION DE PROTOCOLOS DE BIOSEGURIDAD'),
    ('019d8e2b-7711-7e61-831d-b8d28e7e5932', 'PF-SALUD-010', 'RESPUESTA INTEGRAL A EMERGENCIAS MEDICAS')
ON CONFLICT DO NOTHING;

-- Proyecto de Peluqueria (ya definido en el ejemplo anterior)
INSERT INTO proyecto_formativo (id, codigo, nombre)
VALUES ('019d8e05-9988-7561-831d-b8d28e7e5913', 'PF-PELUQUERIA-002', 'COSMETOLOGIA PELUQUERIA Y ESTILO') 
ON CONFLICT DO NOTHING;

-- ==========================================
-- 2. ACTUALIZACION DE FICHAS CON SUS PROYECTOS
-- ==========================================
-- Insertamos las fichas vinculandolas a los programas y a los nuevos proyectos
INSERT INTO ficha_formacion (id, numero, programa_formacion_id, coordinacion_id, proyecto_formativo_id, instructor_id) VALUES 
    -- Ficha Gastronomia + Proyecto GASTRO
    (gen_random_uuid(), '2905678', '019d8dfb-3652-7e61-831d-b8d28e7e5904', '019d8dfb-3652-7e61-831d-b8d28e7e5908', '019d8e2b-7711-7e61-831d-b8d28e7e5930', '019d8dbc-deb5-72b7-b67c-af6126cff896'),
    
    -- Ficha Limpieza + Proyecto HIGIENE
    (gen_random_uuid(), '3006789', '019d8dfb-3652-7e61-831d-b8d28e7e5906', '019d8dfb-3652-7e61-831d-b8d28e7e5908', '019d8e2b-7711-7e61-831d-b8d28e7e5931', '019d8dbc-deb5-72b7-b67c-af6126cff896'),
    
    -- Ficha Peluqueria + Proyecto ESTILO
    ('019d8e05-9988-7561-831d-b8d28e7e5914', '5477667', '019d8