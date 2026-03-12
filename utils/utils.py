"""
utils/utils.py
Utilidades generales para bariLMS
"""
from sqlalchemy.inspection import inspect


def serialize_model(obj, depth=1):
    """
    Convierte un modelo SQLAlchemy a diccionario.
    depth controla el nivel de anidamiento de relaciones.
    """
    if obj is None:
        return None

    data = {}
    mapper = inspect(obj)

    # Serializar columnas
    for column in mapper.mapper.column_attrs:
        data[column.key] = getattr(obj, column.key)

    # Serializar relaciones
    if depth > 0:
        for name, relation in mapper.mapper.relationships.items():
            value = getattr(obj, name)
            if value is None:
                data[name] = None
            elif relation.uselist:
                data[name] = [serialize_model(child, depth - 1) for child in value]
            else:
                data[name] = serialize_model(value, depth - 1)

    return data
