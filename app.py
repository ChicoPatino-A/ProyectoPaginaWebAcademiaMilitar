"""
# Modulos
# Creacion de la app con flask
# Configuración de la base de datos
# Inicialización de la base de datos
# Inicializa Firebase
# Rutas Basicas del NavBar
# Ruta para crear Cuenta
# Ruta para Hacer Login
# Ruta para crear administrador
# Rutas para promociones
# Funcion para subir Video
# Rutas para videos
# Funcion para subir Imagen
# Rutas para imagenes
"""

# Modulos
from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
from modelos.BaseDeDatos import BaseDeDatos
import firebase_admin
from firebase_admin import credentials, storage

# Creacion de la app con flask
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


# Inicializa Firebase
def initialize_firebase(json_key_path, storage_bucket):
    if not firebase_admin._apps:
        cred = credentials.Certificate(json_key_path)
        firebase_admin.initialize_app(cred, {'storageBucket': storage_bucket})

# Rutas Basicas del NavBar

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/principal')
def principal():
    return render_template('index.html')

@app.route('/contacto') # Ruta que obtiene la palabra /contacto
def contacto(): # abre la funcion contacto
    return render_template('contacto.html') # se dirige automaticamente a contacto.html
 
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


# Ruta para crear Cuenta

@app.route('/crearCuenta', methods=['POST'])
def crearCuenta():
    correo = request.form['correo']
    contrasena = request.form['contrasena']

    base_datos.crear_usuario(correo, contrasena)
    return render_template('administracion.html', aviso = "¡El usuario se cargo exitosamente!")

# Ruta para Hacer Login

@app.route('/login', methods=['POST'])
def login():
    correo = request.form['correo'] # obtiene el correo del formulario
    contrasena = request.form['contrasena'] # obtiene la contraseña del formulario
    # el usuario se obtiene de la BD por medio de una funcion "obtener_usuario" donde los
    # parametros son: correo y contraseña 
    usuario = base_datos.obtener_usuario(correo, contrasena)

    if usuario:  # si el usuario existe
        return render_template('administracion.html') # viajo a la plantilla administracion.html
    else: # caso contrario voy a iniciarsesion, junto con un aviso

        return render_template('iniciarsesion.html',  aviso = "¡El usuario no existe")

# Ruta para crear administrador

@app.route('/crearAdministrador')
def crearAdministrador():
    return render_template('crearadministrador.html')

# Ruta para eliminar administrador

@app.route('/eliminarAdministrador')
def eliminarAdministrador():
    return render_template('eliminarAdministrador.html')


# Ruta para editar administrador

@app.route('/editarAdministrador')
def editarAdministrador():
    return render_template('editarAdministrador.html')

#  Rutas para Promociones
# 1 - guardarPromocion
# 2 - crearPromocion
# 3 - promociones/{id} -> para acceder a alguna promocion
# 4 - eliminarPromocion
# 5 - editarPromocion

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
 
@app.route('/crearPromocion')
def crearPromocion():
    return render_template('crearpromocion.html')

@app.route('/promociones/<int:id>')
def mostrar_promocion(id):
    promocion = base_datos.obtener_promocion_por_id(id)
    imagenes = base_datos.obtener_imagenes_por_id_promocion(id)
    videos = base_datos.obtener_videos_por_id_promocion(id)
    
    if promocion:
        return render_template('promocion_detalle.html', promocion=promocion, imagenes=imagenes, videos = videos)
    else:
        return "Promoción no encontrada.", 404
    
@app.route('/eliminarPromocion')
def eliminarPromocion():
    return render_template('eliminarPromocion.html')

@app.route('/editarPromocion')
def editarPromocion():
    return render_template('editarPromocion.html')

# Funcion para subir Video:
def subir_video(local_path):
    bucket = storage.bucket()
    blob = bucket.blob(os.path.basename(local_path))
    blob.upload_from_filename(local_path)
    blob.make_public()
    return blob.public_url

# Rutas para Videos:
# 1 - Subir Video
# 2 - Guardar Video
# 3 - Eliminar Video
# 4 - Editar Video

@app.route('/subirVideo')
def subirVideo():
    promociones = base_datos.obtener_promociones()
    return render_template('subirVideo.html',promociones = promociones)

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
        print("Id de la promocion es: ",id_promocion)
        base_datos.guardar_video(titulo, resena, url_video, id_promocion)

        os.remove(local_path)
        return render_template('administracion.html', aviso = "¡El video se subió exitosamente!")
    else:
        return "Error al subir el video", 500

@app.route('/eliminarVideo')
def eliminarVideo():
    return render_template('eliminarVideo.html')

@app.route('/editarVideo')
def editarVideo():
    return render_template('editarVideo.html')

# Funcion para subir imagen

# Función para subir imagen a Firebase
def subir_imagen(file_path):
    bucket = storage.bucket()
    blob = bucket.blob(os.path.basename(file_path))
    blob.upload_from_filename(file_path)
    blob.make_public()
    return blob.public_url


# Rutas para las imagenes: 
# 1 - Subir Imagen
# 2 - Guardar Imagen
# 3 - Eliminar Imagen
# 4 - Editar Imagen

@app.route('/subirImagen')
def subirImagen():
    promociones = base_datos.obtener_promociones()
    return render_template('subirImagen.html', promociones = promociones)

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

@app.route('/eliminarImagen')
def eliminarImagen():
    return render_template('eliminarImagen.html')

@app.route('/editarImagen')
def editarImagen():
    return render_template('editarImagen.html')


# Funcion main de arranque del programa
if __name__ == '__main__':
    app.run(debug=True, host='192.168.43.69', port=5000)

