from flask import Flask, render_template
from flask_cors import CORS
from routes.estudiantes import estudiantes_bp
from routes.reportes import reportes_bp
from routes.instructores import instructores_bp
from routes.cursos import cursos_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(estudiantes_bp)
app.register_blueprint(reportes_bp)
app.register_blueprint(instructores_bp)
app.register_blueprint(cursos_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reportes')
def reportes():
    return render_template('reportes.html')

@app.route('/estudiantes')
def estudiantes():
    return render_template('estudiantes.html')

@app.route('/instructores')
def instructores():
    return render_template('instructores.html')

@app.route('/cursos')
def cursos():
    return render_template('cursos.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)