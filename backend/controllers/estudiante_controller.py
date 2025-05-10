from utils.db import get_db_connection

def obtener_estudiantes():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id_estudiante, nombre, correo FROM estudiantes;')
    rows = cur.fetchall()
    estudiantes = [{'id': row[0], 'nombre': row[1], 'correo': row[2]} for row in rows]
    cur.close()
    conn.close()
    return estudiantes