
import os
from firebase_admin import credentials, storage
from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename
from app_config import app
from basedatos_config import base_datos
from firebase_config import initialize_firebase

imagenes_bp = Blueprint('imagen_rutas', __name__)

@imagenes_bp.route('/subirImagen')
def subirImagen():
    promociones = base_datos.obtener_promociones()
    return render_template('imagenes/subirImagen.html', promociones=promociones)

@imagenes_bp.route('/guardarImagen', methods=['POST'])
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
        base_datos.guardar_imagen(titulo, resena, url_imagen, id_promocion)
        os.remove(local_path)
        return render_template('administracion.html', aviso="¡La imagen se subió exitosamente!")
    else:
        return "Error al subir la imagen", 500

@imagenes_bp.route('/eliminarImagen')
def eliminarImagen():
    imagenes = base_datos.obtener_imagenes()
    promociones = base_datos.obtener_promociones()
    return render_template('imagenes/eliminarImagenes.html', imagenes=imagenes, promociones=promociones)

@imagenes_bp.route('/eliminar_imagen_de_baseDatos/<int:id>', methods=['POST'])
def eliminar_imagen_de_baseDatos(id):
    base_datos.eliminar_imagen(id)
    imagenes = base_datos.obtener_imagenes()
    promociones = base_datos.obtener_promociones()
    return render_template('imagenes/eliminarImagenes.html', aviso="Imagen eliminada exitosamente.", imagenes=imagenes, promociones=promociones)

@imagenes_bp.route('/editarImagen')
def editarImagen():
    imagenes = base_datos.obtener_imagenes()
    promociones = base_datos.obtener_promociones()
    return render_template('imagenes/editarImagen.html', imagenes=imagenes, promociones=promociones)

@imagenes_bp.route('/modificarImagen/<int:id>', methods=['GET','POST'])
def modificarImagen(id):
    imagen = base_datos.obtener_imagen_por_id(id)
    return render_template('imagenes/modificarImagen.html', imagen = imagen)

@imagenes_bp.route('/modificarImagen_enBaseDatos', methods=['POST'])
def modificarImagen_enBaseDatos():
    id = request.form['id']
    titulo = request.form['titulo']
    comentario = request.form['comentario']
    base_datos.modificar_imagen(id, titulo, comentario)
    return render_template('administracion.html', aviso="¡La imagen se modifico exitosamente!")


# Función para subir imagen a Firebase
def subir_imagen(file_path):
    bucket = storage.bucket()
    blob = bucket.blob(os.path.basename(file_path))
    blob.upload_from_filename(file_path)
    blob.make_public()
    return blob.public_url
