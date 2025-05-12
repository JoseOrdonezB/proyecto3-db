from flask import Blueprint, jsonify
from controllers.curso_controller import obtener_cursos

cursos_bp = Blueprint('cursos_bp', __name__)

@cursos_bp.route('/api/cursos')
def cursos():
    cursos = obtener_cursos()
    return jsonify(cursos)