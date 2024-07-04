from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import firebase_admin
from firebase_admin import credentials, storage
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    'user': 'root',          # Reemplaza con tu usuario de la base de datos
    'password': '',     # Reemplaza con tu contraseña de la base de datos
    'host': 'localhost',           # Reemplaza si tu host es diferente
    'database': 'basededatosacademiamilitar' # Nombre de tu base de datos
}

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
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    query = "SELECT id, numero_promocion, url_imagen FROM promociones"
    cursor.execute(query)
    promociones = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('promociones.html', promociones=promociones)

@app.route('/login', methods=['POST'])
def login():
    # Guardo la informacion del formulario en las variables correo y contrasena
    correo = request.form['correo']
    contrasena = request.form['contrasena']


    # Conectar a la base de datos
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Consultar la base de datos
    query = "SELECT * FROM usuarios WHERE email=%s AND password=%s"
    cursor.execute(query, (correo, contrasena))
    user = cursor.fetchone() # si encuentra al menos un usuario lo guarda en la varaible "user"
    # si el usuario no existe usuario vale "NULL".
    cursor.close()
    conn.close()

    if user: # preguntando si user EXISTE. 
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
    return render_template('subirVideo.html')

@app.route('/subirImagen')
def subirImagen():
    return render_template('subirImagen.html')

@app.route('/crearCuenta',  methods=['POST'])
def crearCuenta():
        # Guardo la informacion del formulario en las variables correo y contrasena
    correo = request.form['correo']
    contrasena = request.form['contrasena']


    # Conectar a la base de datos
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Insertar en la base de datos
    query = "INSERT INTO usuarios(email, password) VALUES (%s, %s);"
    cursor.execute(query, (correo, contrasena))
    
    conn.commit()
    cursor.close()
    conn.close()

    return "registro exitoso"

# Inicializa Firebase
def initialize_firebase(json_key_path, storage_bucket):
    cred = credentials.Certificate(json_key_path)
    firebase_admin.initialize_app(cred, {
        'storageBucket': storage_bucket
    })

# Función para subir imagen a Firebase
def subir_imagen(file_path):
    bucket = storage.bucket()
    blob = bucket.blob(os.path.basename(file_path))
    blob.upload_from_filename(file_path)
    blob.make_public()
    return blob.public_url

@app.route('/guardarPromocion', methods=['POST'])
def guardarPromocion():
    # Número de la promoción
    numero_promocion = request.form['numeroPromocion']
    
    # Ruta donde se guardará la imagen temporalmente
    UPLOAD_FOLDER = 'static/images'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    json_key_path = 'C://Users//aclog//Desktop//ProyectoFinal//Codigo//academiadelogistica-4a432-firebase-adminsdk-j0rgu-442fbffdb6.json'
    storage_bucket = 'academiadelogistica-4a432.appspot.com'

    # Inicializa Firebase
    initialize_firebase(json_key_path, storage_bucket)
    
    # Manejo de archivo de imagen
    if 'imagenPromocion' not in request.files:
        return "No se encontró la imagen", 400

    file = request.files['imagenPromocion']
    if file.filename == '':
        return "No se seleccionó ninguna imagen", 400

    if file:
        filename = secure_filename(file.filename)
        local_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(local_path)
        
        # Subir imagen a Firebase
        url_imagen = subir_imagen(local_path)

        # Conectar a la base de datos
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Insertar datos en la base de datos
        query = "INSERT INTO promociones (numero_promocion, url_imagen) VALUES (%s, %s);"
        cursor.execute(query, (numero_promocion, url_imagen))

        conn.commit()
        cursor.close()
        conn.close()

        # Eliminar archivo temporal local
        os.remove(local_path)

        return "Registro exitoso"
    else:
        return "Error al subir la imagen", 500

    
if __name__ == '__main__':
    app.run(debug=True, host='192.168.43.69', port=5000)

#192.168.43.69
#10.108.4.35