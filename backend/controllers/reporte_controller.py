from utils.db import get_db_connection

# 1. Avance de estudiantes por curso
def obtener_reporte_avance(curso_id=None, porcentaje_min=0, porcentaje_max=100, fecha_inicio=None, fecha_fin=None):
    conn = get_db_connection()
    cur = conn.cursor()
    query = """
        SELECT e.nombre AS estudiante, c.nombre AS curso,
               p.porcentaje_completado, p.calificacion_final, p.fecha_actualizacion
        FROM progreso p
        JOIN inscripciones i ON p.id_inscripcion = i.id_inscripcion
        JOIN estudiantes e ON i.id_estudiante = e.id_estudiante
        JOIN cursos c ON i.id_curso = c.id_curso
        WHERE p.porcentaje_completado BETWEEN %s AND %s
    """
    params = [porcentaje_min, porcentaje_max]
    if curso_id:
        query += " AND i.id_curso = %s"
        params.append(curso_id)
    if fecha_inicio:
        query += " AND p.fecha_actualizacion >= %s"
        params.append(fecha_inicio)
    if fecha_fin:
        query += " AND p.fecha_actualizacion <= %s"
        params.append(fecha_fin)
    query += " ORDER BY p.fecha_actualizacion DESC"
    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "estudiante": row[0],
            "curso": row[1],
            "porcentaje_completado": float(row[2]),
            "calificacion_final": float(row[3]) if row[3] else None,
            "fecha_actualizacion": row[4].isoformat() if row[4] else None
        } for row in rows
    ]

# 2. Ranking de estudiantes

def obtener_reporte_ranking(curso_id=None, calificacion_min=0, fecha_inicio=None, fecha_fin=None, top_n=10):
    conn = get_db_connection()
    cur = conn.cursor()
    query = """
        SELECT e.nombre, c.nombre, p.calificacion_final
        FROM progreso p
        JOIN inscripciones i ON p.id_inscripcion = i.id_inscripcion
        JOIN estudiantes e ON i.id_estudiante = e.id_estudiante
        JOIN cursos c ON i.id_curso = c.id_curso
        WHERE p.calificacion_final >= %s
    """
    params = [calificacion_min]
    if curso_id:
        query += " AND i.id_curso = %s"
        params.append(curso_id)
    if fecha_inicio:
        query += " AND i.fecha_inscripcion >= %s"
        params.append(fecha_inicio)
    if fecha_fin:
        query += " AND i.fecha_inscripcion <= %s"
        params.append(fecha_fin)
    query += " ORDER BY p.calificacion_final DESC LIMIT %s"
    params.append(top_n)
    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {"estudiante": row[0], "curso": row[1], "calificacion_final": float(row[2])} for row in rows
    ]

# 3. Evaluaciones entregadas

def obtener_reporte_entregas(curso_id=None, fecha_inicio=None, fecha_fin=None, puntaje_min=0, puntaje_max=100):
    conn = get_db_connection()
    cur = conn.cursor()
    query = """
        SELECT e.nombre, ev.titulo, en.fecha_entrega, en.puntaje_obtenido
        FROM entregas en
        JOIN evaluaciones ev ON en.id_evaluacion = ev.id_evaluacion
        JOIN estudiantes e ON en.id_estudiante = e.id_estudiante
        JOIN lecciones l ON ev.id_leccion = l.id_leccion
        JOIN cursos c ON l.id_curso = c.id_curso
        WHERE en.puntaje_obtenido BETWEEN %s AND %s
    """
    params = [puntaje_min, puntaje_max]
    if curso_id:
        query += " AND c.id_curso = %s"
        params.append(curso_id)
    if fecha_inicio:
        query += " AND en.fecha_entrega >= %s"
        params.append(fecha_inicio)
    if fecha_fin:
        query += " AND en.fecha_entrega <= %s"
        params.append(fecha_fin)
    query += " ORDER BY en.fecha_entrega DESC"
    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "estudiante": row[0],
            "evaluacion": row[1],
            "fecha_entrega": row[2].isoformat() if row[2] else None,
            "puntaje_obtenido": float(row[3])
        } for row in rows
    ]

# 4. Inscripciones por periodo

def obtener_reporte_inscripciones(fecha_inicio=None, fecha_fin=None, curso_id=None, instructor_id=None):
    conn = get_db_connection()
    cur = conn.cursor()
    query = """
        SELECT e.nombre, c.nombre, i.fecha_inscripcion, ins.nombre
        FROM inscripciones i
        JOIN estudiantes e ON i.id_estudiante = e.id_estudiante
        JOIN cursos c ON i.id_curso = c.id_curso
        JOIN instructores ins ON c.id_instructor = ins.id_instructor
        WHERE 1=1
    """
    params = []
    if fecha_inicio:
        query += " AND i.fecha_inscripcion >= %s"
        params.append(fecha_inicio)
    if fecha_fin:
        query += " AND i.fecha_inscripcion <= %s"
        params.append(fecha_fin)
    if curso_id:
        query += " AND c.id_curso = %s"
        params.append(curso_id)
    if instructor_id:
        query += " AND ins.id_instructor = %s"
        params.append(instructor_id)
    query += " ORDER BY i.fecha_inscripcion DESC"
    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "estudiante": row[0],
            "curso": row[1],
            "fecha_inscripcion": row[2].isoformat() if row[2] else None,
            "instructor": row[3]
        } for row in rows
    ]

# 5. Cursos por categoría y duración

def obtener_reporte_cursos(id_categoria=None, duracion_min=0, duracion_max=100, instructor_id=None, nombre_like=None):
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
        SELECT c.nombre, cat.nombre_categoria, c.duracion_horas, ins.nombre
        FROM cursos c
        JOIN curso_categoria cc ON c.id_curso = cc.id_curso
        JOIN categorias_curso cat ON cc.id_categoria = cat.id_categoria
        JOIN instructores ins ON c.id_instructor = ins.id_instructor
        WHERE c.duracion_horas BETWEEN %s AND %s
    """
    params = [duracion_min, duracion_max]

    if id_categoria is not None:
        query += " AND cat.id_categoria = %s"
        params.append(id_categoria)

    if instructor_id is not None:
        query += " AND ins.id_instructor = %s"
        params.append(instructor_id)

    if nombre_like:
        query += " AND c.nombre ILIKE %s"
        params.append(f"%{nombre_like}%")

    query += " ORDER BY c.nombre"

    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "curso": row[0],
            "categoria": row[1],
            "duracion_horas": row[2],
            "instructor": row[3]
        } for row in rows
    ]
