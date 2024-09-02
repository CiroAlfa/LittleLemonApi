# En tu archivo custom_queries.py

from django.db import connection

def get_menu_items_with_limit(limit):
    with connection.cursor() as cursor:
        # Usamos %s como marcador de posición y pasamos el límite como parámetro
        cursor.execute("SELECT * FROM LittleLemonAPI_menuitem LIMIT %s", [limit])
        # Obtenemos todas las filas de la consulta
        rows = cursor.fetchall()
    return rows