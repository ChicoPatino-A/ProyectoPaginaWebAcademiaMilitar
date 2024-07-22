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

@app.route('/promociones')  # ruta que obtiene la palabra /promociones
def promociones():  # abre la funcion promociones
    promociones = base_datos.obtener_promociones()  # promociones lo obtiene de la BD por medio de la funcion "obtener_promociones"
    return render_template('promociones.html', promociones=promociones) # se dIrige automaticamente a promociones.html, enviandole las promociones de la BD


# Ruta para crear Cuenta

@app.route('/crearCuenta', methods=['POST'])    # ruta que obtiene la palabra /crearCuenta al crear administrador. (almacenan o guardan informacion)
def crearCuenta():  # abre la funcion crearCuenta
    correo = request.form['correo']
    contrasena = request.form['contrasena']

    base_datos.crear_usuario(correo, contrasena)    # crea el usuario en la BD con los parametros: correo y contraseña
    return render_template('administracion.html', aviso = "¡El usuario se cargo exitosamente!") # se dirige automaticamente a la plantilla administracion.html

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


@app.route('/administracion')
def administracion():
    return render_template('administracion.html')

@app.route('/editarAdministrador')
def editarAdministrador():
    administradores = base_datos.obtener_usuarios()
    return render_template('editarAdministrador.html', administradores = administradores)

# Ruta para eliminar administrador

@app.route('/eliminarAdministrador')
def eliminarAdministrador():
    administradores = base_datos.obtener_usuarios()
    return render_template('eliminarAdministrador.html', administradores = administradores)



# Ruta para editar administrador

@app.route('/eliminar_administrador_de_baseDatos/<int:id>', methods=['POST'])
def eliminar_administrador_de_baseDatos(id):
    base_datos.eliminar_administrador(id)
    administradores = base_datos.obtener_usuarios()
    return render_template('eliminarAdministrador.html', aviso = "administrador eliminado exitosamente.", administradores = administradores)

#  Rutas para Promociones
# 1 - guardarPromocion
# 2 - crearPromocion
# 3 - promociones/{id} -> para acceder a alguna promocion
# 4 - eliminarPromocion
# 5 - editarPromocion

@app.route('/guardarPromocion', methods=['POST'])   # ruta que obtiene la palabra /guardarPromocion y me dirige a la plantilla crearPromocion.html
def guardarPromocion(): # abre la funcion en la plantilla crearPromocion.html
    numero_promocion = request.form['numeroPromocion']  # obtiene el numero de promocion del formulario

    UPLOAD_FOLDER = 'static/images'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    json_key_path = 'C://Users//aclog//Desktop//ProyectoFinal//Codigo//academiadelogistica-4a432-firebase-adminsdk-j0rgu-442fbffdb6.json'
    storage_bucket = 'academiadelogistica-4a432.appspot.com'

    initialize_firebase(json_key_path, storage_bucket)

    if 'imagenPromocion' not in request.files:  # si la imagen no esta en los archivos subidos del formulario
        return "No se encontró la imagen", 400  # me devuelve un aviso

    archivo_imagen = request.files['imagenPromocion'] #  guardo el archivo en la variable archivo_imagen
    if archivo_imagen.filename == '':   # si el nombre resulta vacio (no hay archivo)
        return "No se seleccionó ninguna imagen", 400   # me devuelve un error

    if archivo_imagen:
        nombre_archivo_codificado = secure_filename(archivo_imagen.filename)    #   secure_filename es como ponerle un nombre seguro momentaneamente a la imagen, lo codifica y lo guarda en esa variable
        local_path = os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo_codificado)
        archivo_imagen.save(local_path)
        
        url_imagen = subir_imagen(local_path)
        base_datos.guardar_promocion(numero_promocion, url_imagen) # "guardar_promocion" lo obtiene de la BD con los parametros: numero_promocion, url_imagen

        os.remove(local_path)
        return render_template('administracion.html', aviso = "¡La promocion se cargo exitosamente!")   # añadida la promocion abre automaticamente la plantilla administracion.html con un aviso
    else:
        return "Error al subir la imagen", 500
 
@app.route('/crearPromocion')
def crearPromocion():
    return render_template('crearpromocion.html')

@app.route('/promociones/<int:id>')
def mostrar_promocion(id):  # abre la funcion mostrar_promociones a traves del parametro id de la BD
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
    bucket = storage.bucket()   # proceso de almacenamiento en mi bucket
    blob = bucket.blob(os.path.basename(local_path))
    blob.upload_from_filename(local_path)
    blob.make_public()
    return blob.public_url  # me devuelve la url donde esta alojada la imagen para almacenarla en la BD

# Rutas para Videos:
# 1 - Subir Video
# 2 - Guardar Video
# 3 - Eliminar Video
# 4 - Editar Video

@app.route('/subirVideo')
def subirVideo():
    promociones = base_datos.obtener_promociones()  # obtiene el video de la promocion que corresponda a traves de la funcion  "obtener_promociones" de la BD
    return render_template('subirVideo.html', promociones = promociones)

@app.route('/guardarVideo', methods=['POST'])   # abre la ruta con la palabra /guardarVideo que conecta con la plantilla subirVideo.html
def guardarVideo(): # abre la funcion guardarVideo
    titulo = request.form['tituloVideo']    # obtiene el titulo del formulario
    resena = request.form['resenaVideo']    # obtiene la resena del formulario
    numeroDePromocion = request.form['numeroDePromocion']   # obtiene el numeroDePromocion del formulario
    UPLOAD_FOLDER = 'static/videos' 
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    json_key_path = 'C://Users//aclog//Desktop//ProyectoFinal//Codigo//academiadelogistica-4a432-firebase-adminsdk-j0rgu-442fbffdb6.json'
    storage_bucket = 'academiadelogistica-4a432.appspot.com'

    initialize_firebase(json_key_path, storage_bucket)

    if 'videoCargado' not in request.files: # si el video no se encuentra me mostrara un aviso
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

        os.remove(local_path)   # elimina la ruta que se creo en el 1er paso, una vez la tiene almacena en la tabla video de la BD
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

@app.route('/guardarImagen', methods=['POST'])  # abre la ruta con la palabra /guardarimagen que conecta con la plantilla subirImagen.html
def guardarImagen():
    titulo = request.form['tituloImagen']
    resena = request.form['resenaImagen']
    numeroDePromocion = request.form['numeroDePromocion']
    UPLOAD_FOLDER = 'static/images' 
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    json_key_path = 'C://Users//aclog//Desktop//ProyectoFinal//Codigo//academiadelogistica-4a432-firebase-adminsdk-j0rgu-442fbffdb6.json'
    storage_bucket = 'academiadelogistica-4a432.appspot.com'

    #   inicializo farebase pasandole como parametro las claves y el lugar donde voy almacenar los archivos
    initialize_firebase(json_key_path, storage_bucket)  # inicializar farebase es como mostrar las credenciales a un guardia para decirle donde voy a guardar mis archivos
    
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

