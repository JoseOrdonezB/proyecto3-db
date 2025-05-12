from utils.db import get_db_connection

def obtener_instructores():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id_instructor, nombre, correo, especialidad FROM instructores;')
    rows = cur.fetchall()
    instructores = [
        {
            'id': row[0],
            'nombre': row[1],
            'correo': row[2],
            'especialidad': row[3]
        }
        for row in rows
    ]
    cur.close()
    conn.close()
    return instructores