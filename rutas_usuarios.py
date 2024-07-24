# rutas_usuarios.py
from flask import Blueprint, render_template, request
from basedatos_config import base_datos


usuarios_bp = Blueprint('usuario_rutas', __name__)

@usuarios_bp.route('/guardarAdministrador', methods=['POST'])
def guardarAdministrador():
    correo = request.form['correo']
    contrasena = request.form['contrasena']
    base_datos.crear_usuario(correo, contrasena)
    return render_template('administracion.html', aviso="¡El usuario se cargó exitosamente!")

@usuarios_bp.route('/login', methods=['POST'])
def login():
    correo = request.form['correo']
    contrasena = request.form['contrasena']
    usuario = base_datos.obtener_usuario(correo, contrasena)
    if usuario:
        return render_template('administracion.html')
    else:
        return render_template('iniciarsesion.html', aviso="¡El usuario no existe!")

@usuarios_bp.route('/crearAdministrador')
def crearAdministrador():
    return render_template('administrador/crearadministrador.html')

@usuarios_bp.route('/administracion')
def administracion():
    return render_template('administracion.html')

@usuarios_bp.route('/editarAdministrador')
def editarAdministrador():
    administradores = base_datos.obtener_usuarios()
    return render_template('editarAdministrador.html', administradores=administradores)

@usuarios_bp.route('/eliminarAdministrador')
def eliminarAdministrador():
    administradores = base_datos.obtener_usuarios()
    return render_template('administrador/eliminarAdministrador.html', administradores=administradores)

@usuarios_bp.route('/eliminar_administrador_de_baseDatos/<int:id>', methods=['POST'])
def eliminar_administrador_de_baseDatos(id):
    base_datos.eliminar_administrador(id)
    administradores = base_datos.obtener_usuarios()
    return render_template('administrador/eliminarAdministrador.html', aviso="Administrador eliminado exitosamente.", administradores=administradores)
