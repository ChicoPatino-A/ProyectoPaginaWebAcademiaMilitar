import mysql.connector

class BaseDeDatos:
    def __init__(self, config):
        self.config = config
    
    def conectar(self):
        return mysql.connector.connect(**self.config)
    
    def obtener_promociones(self):
        conn = self.conectar()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT id, numero_promocion, url_imagen FROM promociones"
        cursor.execute(query)
        promociones = cursor.fetchall()

        cursor.close()
        conn.close()
        return promociones

    def obtener_usuario(self, correo, contrasena):
        conn = self.conectar()
        cursor = conn.cursor()

        query = "SELECT * FROM usuarios WHERE email=%s AND password=%s"
        cursor.execute(query, (correo, contrasena))
        user = cursor.fetchone()

        cursor.close()
        conn.close()
        return user

    def crear_usuario(self, correo, contrasena):
        conn = self.conectar()
        cursor = conn.cursor()

        query = "INSERT INTO usuarios(email, password) VALUES (%s, %s);"
        cursor.execute(query, (correo, contrasena))

        conn.commit()
        cursor.close()
        conn.close()

    def guardar_promocion(self, numero_promocion, url_imagen):
        conn = self.conectar()
        cursor = conn.cursor()

        query = "INSERT INTO promociones (numero_promocion, url_imagen) VALUES (%s, %s);"
        cursor.execute(query, (numero_promocion, url_imagen))

        conn.commit()
        cursor.close()
        conn.close()

    def obtener_promocion_por_id(self, id):
        conn = self.conectar()
        cursor = conn.cursor()
        query = "SELECT * FROM promociones WHERE id = %s"
        cursor.execute(query, (id,))
        promocion = cursor.fetchone()
        return promocion


