from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

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
    return '¡Bienvenida, estoy en Casa!'

@app.route('/johana')
def johana():
    return '¡Bienvenida Johana!'

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
    return render_template('promociones.html')

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
        return "Sí, hemos encontrado este usuario."
    else:
        return "Este usuario no existe."

if __name__ == '__main__':
    app.run(debug=True, host='192.168.43.69', port=5000)
