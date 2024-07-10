# app.py

from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
from modelos.BaseDeDatos import BaseDeDatos
import firebase_admin
from firebase_admin import credentials, storage

app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    'user': 'root',         
    'password': '',     
    'host': 'localhost',           
    'database': 'basededatosacademiamilitar'
}

# Inicialización de la base de datos
base_datos = BaseDeDatos(db_config)

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

@app.route('/promociones')
def promociones():
    promociones = base_datos.obtener_promociones()
    return render_template('promociones.html', promociones=promociones)

@app.route('/login', methods=['POST'])
def login():
    correo = request.form['correo']
    contrasena = request.form['contrasena']

    user = base_datos.obtener_usuario(correo, contrasena)

    if user:
        return render_template('administracion.html')
    else:
        return "Este usuario no existe."

@app.route('/crearPromocion')
def crearPromocion():
    return render_template('crearpromocion.html')

@app.route('/crearAdministrador')
def crearAdministrador():
    return render_template('crearadministrador.html')

@app.route('/subirVideo')
def subirVideo():
    promociones = base_datos.obtener_promociones()
    return render_template('subirVideo.html',promociones = promociones)

@app.route('/subirImagen')
def subirImagen():
    promociones = base_datos.obtener_promociones()
    return render_template('subirImagen.html', promociones = promociones)

@app.route('/crearCuenta', methods=['POST'])
def crearCuenta():
    correo = request.form['correo']
    contrasena = request.form['contrasena']

    base_datos.crear_usuario(correo, contrasena)
    return render_template('administracion.html', aviso = "¡El usuario se cargo exitosamente!")

# Inicializa Firebase
def initialize_firebase(json_key_path, storage_bucket):
    cred = credentials.Certificate(json_key_path)
    firebase_admin.initialize_app(cred, {'storageBucket': storage_bucket})

# Función para subir imagen a Firebase
def subir_imagen(file_path):
    bucket = storage.bucket()
    blob = bucket.blob(os.path.basename(file_path))
    blob.upload_from_filename(file_path)
    blob.make_public()
    return blob.public_url

@app.route('/guardarPromocion', methods=['POST'])
def guardarPromocion():
    numero_promocion = request.form['numeroPromocion']

    UPLOAD_FOLDER = 'static/images'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    json_key_path = 'C://Users//aclog//Desktop//ProyectoFinal//Codigo//academiadelogistica-4a432-firebase-adminsdk-j0rgu-442fbffdb6.json'
    storage_bucket = 'academiadelogistica-4a432.appspot.com'

    initialize_firebase(json_key_path, storage_bucket)

    if 'imagenPromocion' not in request.files:
        return "No se encontró la imagen", 400

    file = request.files['imagenPromocion']
    if file.filename == '':
        return "No se seleccionó ninguna imagen", 400

    if file:
        filename = secure_filename(file.filename)
        local_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(local_path)
        
        url_imagen = subir_imagen(local_path)
        base_datos.guardar_promocion(numero_promocion, url_imagen)

        os.remove(local_path)
        return render_template('administracion.html', aviso = "¡La promocion se cargo exitosamente!")
    else:
        return "Error al subir la imagen", 500
    

@app.route('/guardarImagen', methods=['POST'])
def guardarImagen():
    titulo = request.form['tituloImagen']
    resena = request.form['resenaImagen']
    numeroDePromocion = request.form['numeroDePromocion']
    UPLOAD_FOLDER = 'static/images' 
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    json_key_path = 'C://Users//aclog//Desktop//ProyectoFinal//Codigo//academiadelogistica-4a432-firebase-adminsdk-j0rgu-442fbffdb6.json'
    storage_bucket = 'academiadelogistica-4a432.appspot.com'

    initialize_firebase(json_key_path, storage_bucket)

    if 'imagenCargada' not in request.files:
        return "No se encontró la imagen", 400

    file = request.files['imagenCargada']
    if file.filename == '':
        return "No se seleccionó ninguna imagen", 400

    if file:
        filename = secure_filename(file.filename)
        local_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(local_path)
        
        url_imagen = subir_imagen(local_path)
        id_promocion = base_datos.obtener_id_promocion_por_numero(numeroDePromocion)
        base_datos.guardar_imagen(titulo, resena,url_imagen,id_promocion)

        os.remove(local_path)
        return render_template('administracion.html', aviso = "¡La imagen se subio exitosamente!")
    else:
        return "Error al subir la imagen", 500

def subir_video(local_path):
    bucket = storage.bucket()
    blob = bucket.blob(os.path.basename(local_path))
    blob.upload_from_filename(local_path)
    return blob.public_url

@app.route('/guardarVideo', methods=['POST'])
def guardarVideo():
    titulo = request.form['tituloVideo']
    resena = request.form['resenaVideo']
    numeroDePromocion = request.form['numeroDePromocion']
    UPLOAD_FOLDER = 'static/videos' 
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    json_key_path = 'C://Users//aclog//Desktop//ProyectoFinal//Codigo//academiadelogistica-4a432-firebase-adminsdk-j0rgu-442fbffdb6.json'
    storage_bucket = 'academiadelogistica-4a432.appspot.com'

    initialize_firebase(json_key_path, storage_bucket)

    if 'videoCargado' not in request.files:
        return "No se encontró el video", 400

    file = request.files['videoCargado']
    if file.filename == '':
        return "No se seleccionó ningún video", 400

    if file:
        filename = secure_filename(file.filename)
        local_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(local_path)
        
        url_video = subir_video(local_path)
        id_promocion = base_datos.obtener_id_promocion_por_numero(numeroDePromocion)
        base_datos.guardar_video(titulo, resena, url_video, id_promocion)

        os.remove(local_path)
        return render_template('administracion.html', aviso = "¡El video se subió exitosamente!")
    else:
        return "Error al subir el video", 500

@app.route('/promociones/<int:id>')
def mostrar_promocion(id):
    promocion = base_datos.obtener_promocion_por_id(id)
    imagenes = base_datos.obtener_imagenes_por_id_promocion(id)
    print(promocion)
    print("Imagenes = ", imagenes)
    if promocion:
        return render_template('promocion_detalle.html', promocion=promocion, imagenes=imagenes)
    else:
        return "Promoción no encontrada.", 404

if __name__ == '__main__':
    app.run(debug=True, host='10.108.4.35', port=5000)

