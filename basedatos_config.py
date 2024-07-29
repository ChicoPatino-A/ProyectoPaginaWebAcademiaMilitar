
# from modelos.BaseDeDatos import BaseDeDatos
from modelos.BaseDeDatos import BaseDeDatos

# Configuración de la base de datos
db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'basededatosacademiamilitar'
}

# Inicialización de la base de datos
base_datos = BaseDeDatos(db_config)