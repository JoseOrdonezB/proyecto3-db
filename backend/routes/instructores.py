from flask import Blueprint, jsonify
from controllers.instructor_controller import obtener_instructores

instructores_bp = Blueprint('instructores_bp', __name__)

@instructores_bp.route('/api/instructores')
def instructores():
    instructores = obtener_instructores()
    return jsonify(instructores)