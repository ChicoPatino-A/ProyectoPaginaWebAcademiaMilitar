# rutas_videos.py
import os
from firebase_admin import credentials, storage
from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename
from app_config import app
from basedatos_config import base_datos
from firebase_config import initialize_firebase

videos_bp = Blueprint('video_rutas', __name__)

@videos_bp.route('/subirVideo')
def subirVideo():
    promociones = base_datos.obtener_promociones()
    return render_template('videos/subirVideo.html', promociones=promociones)

@videos_bp.route('/guardarVideo', methods=['POST'])
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
        return render_template('administracion.html', aviso="¡El video se subió exitosamente!")
    else:
        return "Error al subir el video", 500

@videos_bp.route('/eliminarVideo')
def eliminarVideo():
    videos = base_datos.obtener_videos()
    promociones = base_datos.obtener_promociones()
    return render_template('videos/eliminarVideos.html', videos=videos, promociones=promociones)

@videos_bp.route('/eliminar_video_de_baseDatos/<int:id>', methods=['POST'])
def eliminar_video_de_baseDatos(id):
    base_datos.eliminar_video(id)
    videos = base_datos.obtener_videos()
    promociones = base_datos.obtener_promociones()
    return render_template('videos/eliminarVideos.html', aviso="Video eliminado exitosamente.", videos=videos, promociones=promociones)

@videos_bp.route('/editarVideo')
def editarVideo():
    videos = base_datos.obtener_videos()
    promociones = base_datos.obtener_promociones()
    return render_template('videos/editarVideo.html', videos=videos, promociones=promociones)

@videos_bp.route('/modificarVideo/<int:id>', methods=['GET','POST'])
def modificarVideo(id):
    video = base_datos.obtener_video_por_id(id)
    return render_template('videos/modificarVideo.html', video = video)

@videos_bp.route('/modificarVideo_enBaseDatos', methods=['POST'])
def modificarVideo_enBaseDatos():
    id = request.form['id']
    titulo = request.form['titulo']
    comentario = request.form['comentario']
    base_datos.modificar_video(id, titulo, comentario)
    return render_template('administracion.html', aviso="¡El video se modifico correctamente!")

def subir_video(local_path):
    bucket = storage.bucket()
    blob = bucket.blob(os.path.basename(local_path))
    blob.upload_from_filename(local_path)
    blob.make_public()
    return blob.public_url
