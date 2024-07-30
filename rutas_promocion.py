# rutas_promocion.py
import os
from firebase_admin import credentials, storage
from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename
from app_config import app
from basedatos_config import base_datos
from firebase_config import initialize_firebase

promociones_bp = Blueprint('promocion_rutas', __name__)

def subir_imagen(file_path):
    bucket = storage.bucket()
    blob = bucket.blob(os.path.basename(file_path))
    blob.upload_from_filename(file_path)
    blob.make_public()
    return blob.public_url

@promociones_bp.route('/promociones')
def promociones():
    promociones = base_datos.obtener_promociones()
    return render_template('promociones/promociones.html', promociones=promociones)

@promociones_bp.route('/guardarPromocion', methods=['POST'])
def guardarPromocion():
    numero_promocion = request.form['numeroPromocion']
    UPLOAD_FOLDER = 'static/images'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    json_key_path = 'C://Users//aclog//Desktop//ProyectoFinal//Codigo//academiadelogistica-4a432-firebase-adminsdk-j0rgu-442fbffdb6.json'
    storage_bucket = 'academiadelogistica-4a432.appspot.com'
    initialize_firebase(json_key_path, storage_bucket)

    if 'imagenPromocion' not in request.files:
        return "No se encontró la imagen", 400

    archivo_imagen = request.files['imagenPromocion']
    if archivo_imagen.filename == '':
        return "No se seleccionó ninguna imagen", 400

    if archivo_imagen:
        nombre_archivo_codificado = secure_filename(archivo_imagen.filename)
        local_path = os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo_codificado)
        archivo_imagen.save(local_path)
        
        url_imagen = subir_imagen(local_path)
        base_datos.guardar_promocion(numero_promocion, url_imagen)
        os.remove(local_path)
        return render_template('administracion.html', aviso="¡La promoción se cargó exitosamente!")
    else:
        return "Error al subir la imagen", 500

@promociones_bp.route('/crearPromocion')
def crearPromocion():
    return render_template('promociones/crearpromocion.html')

@promociones_bp.route('/promociones/<int:id>')
def mostrar_promocion(id):
    promocion = base_datos.obtener_promocion_por_id(id)
    imagenes = base_datos.obtener_imagenes_por_id_promocion(id)
    videos = base_datos.obtener_videos_por_id_promocion(id)
    if promocion:
        return render_template('promociones/promocion_detalle.html', promocion=promocion, imagenes=imagenes, videos=videos)
    else:
        return "Promoción no encontrada.", 404

@promociones_bp.route('/eliminarPromocion')
def eliminarPromocion():
    promociones = base_datos.obtener_promociones()
    return render_template('promociones/eliminarPromocion.html', promociones=promociones)

@promociones_bp.route('/eliminar_promocion_de_baseDatos/<int:id>', methods=['POST'])
def eliminar_promocion_de_baseDatos(id):
    base_datos.eliminar_promocion(id)
    promociones = base_datos.obtener_promociones()
    return render_template('promociones/eliminarPromocion.html', aviso="Promoción eliminada exitosamente.", promociones=promociones)

@promociones_bp.route('/editarPromocion')
def editarPromocion():
    promociones = base_datos.obtener_promociones()
    return render_template('promociones/editarPromocion.html', promociones=promociones)
