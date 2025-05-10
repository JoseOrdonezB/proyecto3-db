from flask import Blueprint, jsonify
from utils.db import get_db_connection

estudiantes_bp = Blueprint('estudiantes', __name__)

@estudiantes_bp.route('/api/estudiantes')
def estudiantes():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id_estudiante, nombre, correo, fecha_nacimiento FROM estudiantes;')
    rows = cur.fetchall()
    estudiantes = [{'id': row[0], 'nombre': row[1], 'correo': row[2], 'fecha_nacimiento': row[3]} for row in rows]
    cur.close()
    conn.close()
    return jsonify({'estudiantes': estudiantes})