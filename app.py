# app.py
from flask import render_template
from app_config import app

# Rutas Básicas del NavBar
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/principal')
def principal():
    return render_template('index.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/acercade')
def acercade():
    return render_template('acercade.html')

@app.route('/iniciarsesion')
def iniciarsesion():
    return render_template('iniciarsesion.html')

# Importar las rutas desde otros archivos
from rutas_usuarios import usuarios_bp
from rutas_promocion import promociones_bp
from rutas_videos import videos_bp
from rutas_imagenes import imagenes_bp

# Registrar los blueprints
app.register_blueprint(usuarios_bp)
app.register_blueprint(promociones_bp)
app.register_blueprint(videos_bp)
app.register_blueprint(imagenes_bp)

# Función main de arranque del programa
if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.114', port=5000)
