from flask import Blueprint, request, jsonify
from controllers.reporte_controller import obtener_avance_por_curso

reportes_bp = Blueprint('reportes_bp', __name__)

@reportes_bp.route('/api/reportes/avance')
def reporte_avance():
    curso_id = request.args.get('curso_id')
    avance = obtener_avance_por_curso(curso_id)
    return jsonify(avance)