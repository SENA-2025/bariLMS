BEGIN;

-- 1. DELETE FICHAS FIRST (Children)
-- Using a subquery on the Program IDs to catch any UUID-based Fichas too.
DELETE FROM ficha_formacion 
WHERE programa_formacion_id IN (
    '019d8dfb-3652-7e61-831d-b8d28e7e5904', 
    '019d8dfb-3652-7e61-831d-b8d28e7e5906', 
    '019d8e05-9988-7561-831d-b8d28e7e5912', 
    '019d8e1a-4422-7e61-831d-b8d28e7e5921'
) OR numero IN ('2905678', '3006789', '5477667', '4100992');

-- 2. DELETE PROGRAMS (Parents of Fichas)
DELETE FROM programa_formacion 
WHERE id IN (
    '019d8dfb-3652-7e61-831d-b8d28e7e5904', 
    '019d8dfb-3652-7e61-831d-b8d28e7e5906', 
    '019d8e05-9988-7561-831d-b8d28e7e5912', 
    '019d8e1a-4422-7e61-831d-b8d28e7e5921'
);

-- 3. DELETE PROJECTS
DELETE FROM proyecto_formativo WHERE id = '019d8e05-9988-7561-831d-b8d28e7e5913';

-- 4. DELETE AREAS (Parents of Programs)
DELETE FROM area WHERE id IN (
    '019d8dfb-3652-7e61-831d-b8d28e7e5902', 
    '019d8dfb-3652-7e61-831d-b8d28e7e5903', 
    '019d8e05-9988-7561-831d-b8d28e7e5911', 
    '019d8e1a-4422-7e61-831d-b8d28e7e5920'
);

-- 5. DELETE NETWORKS (Parents of Areas)
DELETE FROM red_conocimiento WHERE id IN (
    '019d8dfb-3652-7e61-831d-b8d28e7e5901', 
    '019d8e05-9988-7561-831d-b8d28e7e5910'
);

-- 6. DELETE COORDINATION
DELETE FROM coordinacion WHERE id = '019d8dfb-3652-7e61-831d-b8d28e7e5908';

COMMIT;