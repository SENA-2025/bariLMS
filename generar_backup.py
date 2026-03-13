"""
generar_backup.py
Genera el archivo bari_schema_setup.sql para que los compañeros importen en phpMyAdmin.
Incluye schema completo + datos de catálogos base.
Ejecutar: python generar_backup.py
"""
import re
import pymysql

conn = pymysql.connect(
    host="127.0.0.1", port=3306, user="root", password="", database="bari",
    charset="utf8mb4",
)
cur = conn.cursor()

# Leer schema original
with open("database_mariadb.sql", "r", encoding="utf-8") as f:
    schema_sql = f.read()

lines = []
lines.append("-- ================================================================")
lines.append("--   BARI LMS - Script de Configuración para Compañeros")
lines.append("--   Crea el schema completo + datos de catálogos base")
lines.append("--   Cómo usarlo:")
lines.append("--     1. Abrir phpMyAdmin")
lines.append("--     2. Crear base de datos: bari  (charset utf8mb4)")
lines.append("--     3. Importar este archivo")
lines.append("--     4. Ejecutar: python seed_demo.py  (para datos de demo)")
lines.append("-- ================================================================")
lines.append("")

# Incluir el schema completo tal cual
lines.append(schema_sql)

with open("../database/bari_schema_setup.sql", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

conn.close()
print("OK: database/bari_schema_setup.sql generado correctamente.")
print("    Los compañeros importan ese archivo en phpMyAdmin y luego ejecutan seed_demo.py")
