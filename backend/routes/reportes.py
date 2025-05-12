from flask import Blueprint, request, jsonify
from controllers.reporte_controller import (
    obtener_reporte_avance,
    obtener_reporte_ranking,
    obtener_reporte_entregas,
    obtener_reporte_inscripciones,
    obtener_reporte_cursos
)

reportes_bp = Blueprint('reportes_bp', __name__)

# 1. Avance de estudiantes por curso
@reportes_bp.route('/api/reportes/avance')
def reporte_avance():
    curso_id = request.args.get('curso_id')
    porcentaje_min = float(request.args.get('porcentaje_min', 0))
    porcentaje_max = float(request.args.get('porcentaje_max', 100))
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    datos = obtener_reporte_avance(curso_id, porcentaje_min, porcentaje_max, fecha_inicio, fecha_fin)
    return jsonify(datos)

# 2. Ranking de estudiantes
@reportes_bp.route('/api/reportes/ranking')
def reporte_ranking():
    curso_id = request.args.get('curso_id')
    calificacion_min = float(request.args.get('calificacion_min', 0))
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    top_n = int(request.args.get('top_n', 10))

    datos = obtener_reporte_ranking(curso_id, calificacion_min, fecha_inicio, fecha_fin, top_n)
    return jsonify(datos)

# 3. Evaluaciones entregadas
@reportes_bp.route('/api/reportes/entregas')
def reporte_entregas():
    curso_id = request.args.get('curso_id')
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    puntaje_min = float(request.args.get('puntaje_min', 0))
    puntaje_max = float(request.args.get('puntaje_max', 100))

    datos = obtener_reporte_entregas(curso_id, fecha_inicio, fecha_fin, puntaje_min, puntaje_max)
    return jsonify(datos)

# 4. Inscripciones por periodo
@reportes_bp.route('/api/reportes/inscripciones')
def reporte_inscripciones():
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    curso_id = request.args.get('curso_id')
    instructor_id = request.args.get('instructor_id')

    datos = obtener_reporte_inscripciones(fecha_inicio, fecha_fin, curso_id, instructor_id)
    return jsonify(datos)

# 5. Cursos por categoría y duración
@reportes_bp.route('/api/reportes/cursos')
def reporte_cursos():
    id_categoria = request.args.get('id_categoria')
    duracion_min = int(request.args.get('duracion_min', 0))
    duracion_max = int(request.args.get('duracion_max', 100))
    instructor_id = request.args.get('instructor_id')
    nombre_like = request.args.get('nombre_like')

    datos = obtener_reporte_cursos(id_categoria, duracion_min, duracion_max, instructor_id, nombre_like)
    return jsonify(datos)
