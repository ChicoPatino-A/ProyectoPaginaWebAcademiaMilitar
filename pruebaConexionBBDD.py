import MySQLdb

def check_connection():
    try:
        # Conectarse a la base de datos
        db = MySQLdb.connect(
            host="localhost",
            user="root",
            passwd="",
            db="basededatosacademiamilitar"
        )
        print("Conexión exitosa a la base de datos.")
        db.close()
    except MySQLdb.Error as e:
        print(f"Error al conectar a la base de datos: {e}")

if __name__ == "__main__":
    check_connection()
