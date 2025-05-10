from flask import Blueprint, jsonify
from controllers.estudiante_controller import obtener_estudiantes

estudiantes_bp = Blueprint('estudiantes_bp', __name__)

@estudiantes_bp.route('/api/estudiantes')
def estudiantes():
    estudiantes = obtener_estudiantes()
    return jsonify(estudiantes)