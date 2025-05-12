from utils.db import get_db_connection

def obtener_cursos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id_curso, nombre, descripcion, duracion_horas, id_instructor FROM cursos;')
    rows = cur.fetchall()
    cursos = [
        {
            'id': row[0],
            'nombre': row[1],
            'descripcion': row[2],
            'duracion_horas': row[3],
            'id_instructor': row[4]
        }
        for row in rows
    ]
    cur.close()
    conn.close()
    return cursos