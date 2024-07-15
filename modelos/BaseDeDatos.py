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
    
    def obtener_imagenes_por_id_promocion(self, id):
        conn = self.conectar()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT titulo, comentario, url_imagen FROM imagenes WHERE id_promocion = %s"
        cursor.execute(query,(id,))
        imagenes_de_la_promocion = cursor.fetchall()
        print(imagenes_de_la_promocion)
        cursor.close()
        conn.close()
        return imagenes_de_la_promocion
    
    def obtener_videos_por_id_promocion(self, id):
        conn = self.conectar()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT titulo, comentario, url_video FROM videos WHERE id_promocion = %s"
        cursor.execute(query,(id,))
        videos_de_la_promocion = cursor.fetchall()
        print(videos_de_la_promocion)
        cursor.close()
        conn.close()
        return videos_de_la_promocion

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

    def obtener_id_promocion_por_numero(self,numeroDePromocion):
            conn = self.conectar()
            cursor = conn.cursor()
            query = "SELECT id FROM promociones WHERE numero_promocion = %s"
            cursor.execute(query, (numeroDePromocion,))
            id = cursor.fetchone()
            print(id)
            return id
    

    def guardar_imagen(self,titulo,comentario, url_imagen, tupla_promocion ):
            id_promocion = tupla_promocion[0]
            conn = self.conectar()
            cursor = conn.cursor()

            query = "INSERT INTO imagenes (titulo,comentario, url_imagen, id_promocion) VALUES (%s, %s,%s, %s);"
            cursor.execute(query, (titulo,comentario, url_imagen, id_promocion,))

            conn.commit()
            cursor.close()
            conn.close()
    def guardar_video(self,titulo,comentario, url_video, tupla_promocion ):
            print("Tupla_promocion es:", tupla_promocion)
            id_promocion = tupla_promocion[0]
            conn = self.conectar()
            cursor = conn.cursor()

            query = "INSERT INTO videos (titulo,comentario, url_video, id_promocion) VALUES (%s, %s,%s, %s);"
            cursor.execute(query, (titulo,comentario, url_video, id_promocion,))

            conn.commit()
            cursor.close()
            conn.close()

    def obtener_promocion_por_id(self, id):
        conn = self.conectar()
        cursor = conn.cursor()
        query = "SELECT * FROM promociones WHERE id = %s"
        cursor.execute(query, (id,))
        promocion = cursor.fetchone()
        print(promocion)
        return promocion


