from utils.db import get_db_connection

def obtener_avance_por_curso(curso_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT e.nombre, p.porcentaje_completado
        FROM progreso p
        JOIN inscripciones i ON p.id_inscripcion = i.id_inscripcion
        JOIN estudiantes e ON i.id_estudiante = e.id_estudiante
        WHERE i.id_curso = %s
    ''', (curso_id,))
    rows = cur.fetchall()
    avance = [{'nombre': row[0], 'porcentaje': row[1]} for row in rows]
    cur.close()
    conn.close()
    return avance