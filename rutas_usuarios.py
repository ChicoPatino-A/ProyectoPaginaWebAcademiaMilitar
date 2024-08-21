from flask import Blueprint, render_template, request
from basedatos_config import base_datos
from argon2 import PasswordHasher, exceptions

usuarios_bp = Blueprint('usuario_rutas', __name__)

# Crear instancia de PasswordHasher de Argon2
ph = PasswordHasher()

@usuarios_bp.route('/guardarAdministrador', methods=['POST'])
def guardarAdministrador():
    correo = request.form['correo']
    contrasena = request.form['contrasena']
    
    # Hashear la contraseña antes de guardarla
    contrasena_hashed = ph.hash(contrasena)
    
    base_datos.crear_usuario(correo, contrasena_hashed)
    return render_template('administracion.html', aviso="¡El usuario se cargó exitosamente!")

@usuarios_bp.route('/login', methods=['POST'])
def login():
    correo = request.form['correo']
    contrasena = request.form['contrasena']
    
    # Obtener el usuario de la base de datos
    usuario = base_datos.obtener_usuario_por_correo(correo)
    
    if usuario:
        # Verificar la contraseña ingresada contra el hash almacenado
        try:
            if ph.verify(usuario[2], contrasena):
                return render_template('administracion.html')
        except exceptions.VerifyMismatchError:
            pass  # Si la contraseña no coincide, simplemente pasamos a devolver un error
            
    return render_template('iniciarsesion.html', aviso="¡El usuario no existe o la contraseña es incorrecta!")

@usuarios_bp.route('/crearAdministrador')
def crearAdministrador():
    return render_template('administrador/crearadministrador.html')

@usuarios_bp.route('/administracion')
def administracion():
    return render_template('administracion.html')

@usuarios_bp.route('/editarAdministrador')
def editarAdministrador():
    administradores = base_datos.obtener_usuarios()
    return render_template('administrador/editarAdministrador.html', administradores=administradores)

@usuarios_bp.route('/modificarAdministrador/<int:id>', methods=['GET','POST'])
def modificarAdministrador(id):
    administrador = base_datos.obtener_usuario_por_id(id)
    return render_template('administrador/modificarAdministrador.html', administrador=administrador)

@usuarios_bp.route('/modificarAdministrador_enBaseDatos', methods=['POST'])
def modificarAdministrador_enBaseDatos():
    id = request.form['id']
    correo = request.form['correo']
    contrasena = request.form['contrasena']
    
    # Hashear la nueva contraseña antes de guardarla
    contrasena_hashed = ph.hash(contrasena)
    
    base_datos.modificar_usuario(id, correo, contrasena_hashed)
    return render_template('administracion.html', aviso="¡El usuario se modificó exitosamente!")

@usuarios_bp.route('/eliminarAdministrador')
def eliminarAdministrador():
    administradores = base_datos.obtener_usuarios()
    return render_template('administrador/eliminarAdministrador.html', administradores=administradores)

@usuarios_bp.route('/eliminar_administrador_de_baseDatos/<int:id>', methods=['POST'])
def eliminar_administrador_de_baseDatos(id):
    base_datos.eliminar_administrador(id)
    administradores = base_datos.obtener_usuarios()
    return render_template('administrador/eliminarAdministrador.html', aviso="Administrador eliminado exitosamente.", administradores=administradores)
